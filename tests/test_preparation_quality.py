import unittest

from sos_prepare.quality import language_state, reasons_for, thirds, digest, normalized


class QualityRules(unittest.TestCase):
    def setUp(self):
        self.policy = dict(english_flag_score=.8,non_english_score=.9,segment_score=.8,
                           ambiguous_language='keep_flagged',boilerplate_abstracts={},reviewed_records={})

    def test_bilingual_abstract_is_not_excluded_by_full_text_score(self):
        segments = [dict(language='ko',score=.99),dict(language='ko',score=.99),dict(language='en',score=.99)]
        d = language_state('ko',.96,segments,self.policy)
        self.assertFalse(d['language_clear_non_english'])
        self.assertTrue(d['language_ambiguous'])
        self.assertTrue(d['possible_mixed_language'])

    def test_consistent_non_english_and_borderline_are_separate(self):
        segments = [dict(language='es',score=.95)]*3
        self.assertTrue(language_state('es',.91,segments,self.policy)['language_clear_non_english'])
        self.assertFalse(language_state('es',.89,segments,self.policy)['language_clear_non_english'])
        self.assertFalse(language_state('es',.99,segments[:2],self.policy)['language_clear_non_english'])

    def test_unicode_chunks_cover_input(self):
        t = '这是中文。文章内容。另一部分。'
        self.assertEqual(''.join(thirds(t)),t)
        self.assertTrue(all(thirds(t)))

    def test_retraction_topic_is_not_a_withdrawal_label(self):
        r = dict(work_id='W1',title='Retracted tympanic membranes',abstract='real text',text_sha256='x')
        d = dict(language_clear_non_english=False,language_ambiguous=False)
        self.assertEqual(reasons_for(r,d,self.policy),[])
        r['title'] = 'WITHDRAWN: Example'
        self.assertIn('explicit_withdrawn_or_retracted_label',reasons_for(r,d,self.policy))

    def test_boilerplate_rule_is_full_text_not_prefix(self):
        abstract = 'Generic journal description.'
        self.policy['boilerplate_abstracts'][digest(normalized(abstract))] = dict(reason='journal')
        r = dict(work_id='W1',title='Example',abstract=abstract,text_sha256='x')
        d = dict(language_clear_non_english=False,language_ambiguous=False)
        self.assertTrue(reasons_for(r,d,self.policy))
        r['abstract'] += ' In contrast, this study examines its history.'
        self.assertEqual(reasons_for(r,d,self.policy),[])

    def test_review_cannot_silently_apply_to_changed_text(self):
        self.policy['reviewed_records']['W1'] = dict(text_sha256='old',action='exclude',reason='notice')
        r = dict(work_id='W1',title='Example',abstract='real text',text_sha256='new')
        with self.assertRaises(ValueError):
            reasons_for(r,dict(language_clear_non_english=False,language_ambiguous=False),self.policy)

    def test_ambiguous_policy_must_be_chosen(self):
        self.policy['ambiguous_language'] = 'pending'
        r = dict(work_id='W1',title='Example',abstract='real text',text_sha256='x')
        with self.assertRaises(ValueError):
            reasons_for(r,dict(language_clear_non_english=False,language_ambiguous=True),self.policy)

    def test_newly_downloaded_webpage_is_rejected_without_prelisted_hash(self):
        r = dict(work_id='W1972646318', title='From Molecules to Crystal Engineering',
                 abstract='ADVERTISEMENT RETURN TO ISSUEPREVArticleNEXT A new paper LEARN ABOUT THESE METRICS ExportRISCitation',
                 text_sha256='new-text-not-in-catalogue')
        d = dict(language_clear_non_english=False,language_ambiguous=False)
        self.assertIn('non_abstract:acs_webpage_instead_of_abstract',reasons_for(r,d,self.policy))
        r['abstract'] = 'Advertisement dissemination in social networks. This study develops a model and evaluates its results.'
        self.assertEqual(reasons_for(r,d,self.policy),[])


if __name__ == '__main__':
    unittest.main()
