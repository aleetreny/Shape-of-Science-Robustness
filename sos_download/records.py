"""Population rules and deterministic allocation, independent of network/storage."""
import hashlib
import heapq
import json
import re

WORDS = re.compile(r'\b\w+\b')
WORK_ID = re.compile(r'W[0-9]+\Z')


def short_id(value):
    return value.rstrip('/').rsplit('/', 1)[-1] if isinstance(value, str) else None


def reconstruct_abstract(index):
    # Same structural checks as the reference TFM's src/abstracts.py, in read-only reference.
    if not isinstance(index, dict) or not index:
        return None
    positions = {}
    for word, indexes in index.items():
        if not isinstance(word, str) or not isinstance(indexes, list):
            return None
        for position in indexes:
            if type(position) is not int or position < 0 or position in positions:
                return None
            positions[position] = word
    if not positions or len(positions) != max(positions) + 1:
        return None
    return ' '.join(positions[i] for i in range(len(positions)))


def text_hash(title, abstract):
    return hashlib.sha256((title + '\n\n' + abstract).encode('utf-8')).hexdigest()


def normalize_work(work, config):
    if not isinstance(work, dict):
        return None, 'record_type'
    wid = short_id(work.get('id'))
    if not wid or not WORK_ID.fullmatch(wid):
        return None, 'work_id'
    year = work.get('publication_year')
    if type(year) is not int or not config['year_min'] <= year <= config['year_max']:
        return None, 'year'
    if work.get('language') != 'en':
        return None, 'language'
    if work.get('type') not in {'article', 'review', 'conference-paper'}:
        return None, 'type'
    if work.get('is_retracted') is not False:
        return None, 'retracted'
    if work.get('is_paratext') is not False:
        return None, 'paratext'
    title = work.get('title')
    if not isinstance(title, str) or not title.strip():
        return None, 'title'
    abstract = reconstruct_abstract(work.get('abstract_inverted_index'))
    if abstract is None:
        return None, 'abstract_index'
    count = len(WORDS.findall(abstract))
    if count < config['min_abstract_words']:
        return None, 'short_abstract'
    topic = work.get('primary_topic') or {}
    if not isinstance(topic, dict):
        return None, 'field'
    field = topic.get('field') or {}
    try:
        field_id = int(short_id(field.get('id')))
    except (ValueError, TypeError, AttributeError):
        return None, 'field'
    if field_id not in config['field_ids']:
        return None, 'field'
    period = 2000 + (year - 2000) // 5 * 5
    if period not in config['period_starts']:
        return None, 'period'
    doi = work.get('doi')
    if isinstance(doi, str):
        doi = re.sub(r'^https?://(?:dx\.)?doi\.org/', '', doi.strip(), flags=re.I).lower() or None
    else:
        doi = None
    result = dict(work_id=wid, doi=doi, title=title, abstract=abstract,
                  publication_year=year, publication_date=work.get('publication_date'),
                  type=work['type'], language='en', field_id=field_id,
                  field_display_name=field.get('display_name'), period_start=period,
                  primary_topic_id=short_id(topic.get('id')),
                  primary_topic_display_name=topic.get('display_name'),
                  primary_topic_json=json.dumps(topic, ensure_ascii=False, sort_keys=True),
                  topics_json=json.dumps(work.get('topics') or [], ensure_ascii=False, sort_keys=True),
                  abstract_word_count=count, title_word_count=len(WORDS.findall(title)),
                  abstract_50_79=count < 80, text_sha256=text_hash(title, abstract),
                  openalex_updated_date=work.get('updated_date'), cited_by_count=work.get('cited_by_count'))
    for level in ('subfield', 'domain'):
        entity = topic.get(level) or {}
        result[level + '_id'] = short_id(entity.get('id')) if isinstance(entity, dict) else None
        result[level + '_display_name'] = entity.get('display_name') if isinstance(entity, dict) else None
    return result, None


def allocate_extra(counts, total, exhausted=()):
    blocked = set(exhausted)
    allocations = {key: 0 for key in counts}
    heap = [(count, *key) for key, count in counts.items() if key not in blocked]
    heapq.heapify(heap)
    if total and not heap:
        raise ValueError('No eligible cells remain for the supplement')
    for _ in range(total):
        count, field, period = heapq.heappop(heap)
        allocations[(field, period)] += 1
        heapq.heappush(heap, (count + 1, field, period))
    return allocations
