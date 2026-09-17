"""Conservative, deterministic text checks, separate from model experiments."""
import hashlib
import json
from pathlib import Path
import re
import sqlite3


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def normalized(text):
    return ' '.join(text.split())


def thirds(text):
    # Character slices also work for scripts that do not separate words by spaces.
    text = normalized(text)
    return [text[len(text)*i//3:len(text)*(i+1)//3] for i in range(3)]


NOTICE = re.compile(r'^(?:retracted|withdrawn|retraction|erratum|corrigendum|editorial|expression of concern)\b|^(?:correction|author correction|publisher correction)\s*(?:to\b|:)', re.I)
WITHDRAWN = re.compile(r'^\s*(?:\[\s*)?(?:withdrawn|retracted)\s*(?:\]|:)', re.I)
ACCESS = re.compile(r'\b(?:access denied|enable javascript|verify (?:that )?you are (?:a )?human|checking your browser|cookies are disabled)\b', re.I)


def language_state(label, score, segments, policy):
    ambiguous = label != 'en' or score < policy['english_flag_score']
    consistent = (label != 'en' and score >= policy['non_english_score']
                  and len(segments) == 3
                  and all(x['language'] == label and x['score'] >= policy['segment_score'] for x in segments))
    return {'language_clear_non_english': consistent, 'language_ambiguous': ambiguous and not consistent,
            'possible_mixed_language': bool(segments) and len({x['language'] for x in segments}) > 1}


def content_signature(abstract):
    a=normalized(abstract).casefold()
    if a.startswith(('advertisement return to issue','advertisement return to book')) and 'learn about these metrics' in a and 'exportriscitation' in a:
        return 'acs_webpage_instead_of_abstract'
    if a.startswith('log in or register subscribe') and 'wolters kluwer health' in a and 'advanced search' in a:
        return 'publisher_navigation_instead_of_abstract'
    if a.startswith('the quality of this reproduction is dependent') and 'reproduction' in a and ('umi' in a or 'microfilm' in a):
        return 'reproduction_front_matter_instead_of_abstract'
    if a.startswith(('this article has been removed:','this article has been withdrawn at the request','this article has been retracted:')):
        return 'withdrawal_notice_instead_of_abstract'
    if a.startswith(('advertisement:','advertisement,')) and ('ieee' in a or 'techrxiv' in a):
        return 'explicit_ieee_advertisement'
    if a.startswith('conference proceedings front matter may contain'):
        return 'conference_front_matter'
    if a.startswith('instructions to authors of the brazilian journal of family and community medicine'):
        return 'author_submission_instructions'
    return None


def reasons_for(record, diagnosis, policy):
    """The caller must explicitly provide the approved ambiguity policy."""
    reasons = []
    full_hash = digest(normalized(record['abstract']))
    if full_hash in policy['boilerplate_abstracts']:
        reasons.append('non_abstract:' + policy['boilerplate_abstracts'][full_hash]['reason'])
    elif signature := content_signature(record['abstract']):
        # Apply the same structures to unseen replacement pages, not just the initial catalogue.
        reasons.append('non_abstract:' + signature)
    if WITHDRAWN.search(record['title']):
        reasons.append('explicit_withdrawn_or_retracted_label')
    review = policy.get('reviewed_records', {}).get(record['work_id'])
    if review:
        if review['text_sha256'] != record['text_sha256']:
            raise ValueError('Reviewed text changed; manual finding must be reviewed again')
        if review['action'] == 'exclude':
            reasons.append('reviewed:' + review['reason'])
    if diagnosis['language_clear_non_english']:
        reasons.append('clear_non_english_abstract')
    elif policy['ambiguous_language'] == 'exclude' and diagnosis['language_ambiguous']:
        reasons.append('ambiguous_abstract_language')
    elif policy['ambiguous_language'] not in ('keep_flagged', 'exclude'):
        raise ValueError('Language ambiguity policy must be explicitly set before selection')
    return reasons


class Quality:
    def __init__(self, root, policy_path, model_path, previous_language=None):
        import fasttext
        self.policy_path = Path(policy_path)
        self.policy = json.loads(self.policy_path.read_text())
        self.db = sqlite3.connect(Path(root)/'quality.sqlite', timeout=30)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS quality(text_sha256 TEXT PRIMARY KEY, diagnosis TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);''')
        with Path(model_path).open('rb') as handle:
            self.model_sha = hashlib.file_digest(handle, 'sha256').hexdigest()
        identity = json.dumps(dict(model_sha=self.model_sha, script_sha=digest(Path(__file__).read_text()),
                                   thresholds={k:self.policy[k] for k in ('english_flag_score','non_english_score','segment_score')}),sort_keys=True)
        old = self.db.execute("SELECT value FROM meta WHERE key='identity'").fetchone()
        if old and old[0] != identity:
            raise ValueError('Quality implementation/model changed: do not mix cached predictions')
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO meta VALUES(?,?)',('identity',identity))
        self.previous = {}
        if previous_language:
            old_db = sqlite3.connect(Path(previous_language).resolve().as_uri()+'?mode=ro',uri=True)
            self.previous = {r[0]:(r[1],r[2],r[3],r[4]) for r in old_db.execute(
                'SELECT text_sha,title_language,title_score,abstract_language,abstract_score FROM predictions')}
            old_db.close()
        self.model = fasttext.load_model(str(model_path))

    def close(self):
        self.db.close()

    def diagnose_many(self, records):
        results = {}
        unknown = {}
        for r in records:
            sha = r['text_sha256']
            if sha in results or sha in unknown:
                continue
            row = self.db.execute('SELECT diagnosis FROM quality WHERE text_sha256=?',(sha,)).fetchone()
            if row:
                results[sha] = json.loads(row[0])
            else:
                unknown[sha] = r
        fresh = [r for sha,r in unknown.items() if sha not in self.previous]
        if fresh:
            tl,ts = self.model.predict([normalized(r['title']) for r in fresh],k=1)
            al,ass = self.model.predict([normalized(r['abstract']) for r in fresh],k=1)
            for r,t,s,a,b in zip(fresh,tl,ts,al,ass):
                self.previous[r['text_sha256']] = (t[0].removeprefix('__label__'),float(s[0]),a[0].removeprefix('__label__'),float(b[0]))
        segment_records = [r for sha,r in unknown.items() if self.previous[sha][2] != 'en']
        segment_predictions = {}
        if segment_records:
            labels,scores = self.model.predict([p for r in segment_records for p in thirds(r['abstract'])],k=1)
            for i,r in enumerate(segment_records):
                segment_predictions[r['text_sha256']] = [dict(language=labels[j][0].removeprefix('__label__'),score=float(scores[j][0])) for j in range(i*3,i*3+3)]
        with self.db:
            for sha,r in unknown.items():
                title_label,title_score,label,score = self.previous[sha]
                segments = segment_predictions.get(sha,[])
                d = dict(title_language=title_label,title_score=title_score,abstract_language=label,abstract_score=score,
                         segments=segments,**language_state(label,score,segments,self.policy),
                         possible_notice=bool(NOTICE.search(r['title'])),possible_access_message=bool(ACCESS.search(r['abstract'])),
                         abstract_50_79=r['abstract_word_count']<80,abstract_over_2000=r['abstract_word_count']>2000)
                # Cached diagnosis depends on text, never on cohort or work ID.
                self.db.execute('INSERT INTO quality VALUES(?,?)',(sha,json.dumps(d,ensure_ascii=False,sort_keys=True)))
                results[sha] = d
        return results
