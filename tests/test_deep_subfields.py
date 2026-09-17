import csv,json,tempfile,unittest
from pathlib import Path
import numpy as np
from sos_deep.subfields_native import run_group
from sos_embed.storage import file_sha


class SubfieldComparisons(unittest.TestCase):
    def run_known(self,n,folder):
        rng=np.random.default_rng(822)
        x=rng.normal(size=(n,7)).astype(np.float64)
        q=np.linalg.qr(rng.normal(size=(7,7)))[0]
        arrays={'one/mean':x,'two/cls':x@q}
        ids=np.arange(700,700+n)
        get=lambda name,chosen:arrays[name][np.asarray(chosen)-700]
        return run_group('1100',ids,get,folder,names=list(arrays)),ids,get,arrays
    def test_rotations_preserve_three_shape_measures_and_exact_neighbors(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);c,ids,get,arrays=self.run_known(80,p)
            with (p/'shape.csv').open() as f:shape=list(csv.DictReader(f))
            for k in ['cka_debiased','procrustes_similarity','rsa_spearman']:
                self.assertAlmostEqual(float(shape[0][k]),1.,places=10)
            with (p/'neighbors.csv').open() as f:neighbors=list(csv.DictReader(f))
            self.assertTrue(all(float(r['mean_overlap'])==1 and r['status']=='computed' for r in neighbors))
            self.assertEqual(c['independent_neighbor_queries'],20)
            before={p.name:file_sha(p) for p in Path(tmp).iterdir()}
            run_group('1100',ids,get,p,names=list(arrays))
            self.assertEqual(before,{p.name:file_sha(p) for p in Path(tmp).iterdir()})
    def test_small_groups_are_missing_not_zero_and_full_lists_are_trivial(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            c,_,_,_=self.run_known(3,p/'tiny')
            self.assertEqual(c['shape_status'],'fewer_than_four_rows')
            with (p/'tiny/neighbors.csv').open() as f:rows=list(csv.DictReader(f))
            self.assertTrue(all(r['mean_overlap']=='' and r['status']=='too_few_candidates' for r in rows))
            self.run_known(11,p/'trivial')
            with (p/'trivial/neighbors.csv').open() as f:rows=list(csv.DictReader(f))
            self.assertEqual(rows[0]['status'],'trivial_all_other_papers')
            self.assertEqual(rows[0]['chance_adjusted'],'')


if __name__=='__main__':unittest.main()
