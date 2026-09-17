import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pyarrow as pa
from sos_deep import input_analysis52 as primary
from sos_deep import input_recipes52 as recipes


class RecipeInputControl(unittest.TestCase):
    def test_only_shuffled_title_changes_its_recipe_input_effect(self):
        rng=np.random.default_rng(613)
        meta=pa.table({'row_index':np.arange(200,dtype=np.int64),
                       'period_start':np.repeat([2000,2005,2010,2015,2020],40)})
        bases={m:rng.normal(size=(200,9)) for m in primary.MODELS}
        native={(m,c):bases[m] for m,c in primary.NAMES}
        arrays={(m,recipes.D['poolings'][m],c):v for (m,c),v in native.items()}
        for m,p,c in recipes.VARIANTS[30:]:
            # Rotation changes coordinates but must preserve relations and neighbors.
            q=np.linalg.qr(np.random.default_rng(100+primary.MODELS.index(m)).normal(size=(9,9)))[0]
            arrays[m,p,c]=bases[m]@q
        arrays['bert','sep','title']=arrays['bert','sep','title'][rng.permutation(200)]
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            design={**primary.D,'per_cell':40,'stability':{**primary.D['stability'],'subset_per_period':20,'repeats':2}}
            with patch.object(primary,'D',design),patch.object(recipes,'D',design),patch.object(primary,'OUT',folder/'primary'),patch.object(recipes,'PRIMARY',folder/'primary'),patch.object(recipes,'OUT',folder/'recipes'):
                primary.field_run(11,np.arange(200),meta,native)
                recipes.field_run(11,np.arange(200),meta,arrays)
                with (folder/'recipes/fields/11/effects.csv').open() as f:rows=list(csv.DictReader(f))
                self.assertEqual(len(rows),240)
                for r in rows:
                    loss=float(r['input_change_from_full'])
                    if r['model']=='bert' and r['recipe']=='sep' and r['input_condition']=='title':
                        self.assertGreater(loss,.5)
                    else:self.assertAlmostEqual(loss,0,places=10)
                commit=(folder/'recipes/fields/11/commit.json').read_bytes()
                recipes.field_run(11,np.arange(200),meta,arrays)
                self.assertEqual(commit,(folder/'recipes/fields/11/commit.json').read_bytes())


if __name__=='__main__':unittest.main()
