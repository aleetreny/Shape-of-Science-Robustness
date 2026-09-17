import csv,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pyarrow as pa
import sos_deep.input_analysis52 as flow
from sos_embed.storage import file_sha

class KnownInputFlow(unittest.TestCase):
    def test_identical_inputs_preserve_shape_neighbors_and_resume(self):
        rng=np.random.default_rng(118)
        data={m:rng.normal(size=(60,8+i)).astype(np.float32) for i,m in enumerate(flow.MODELS)}
        arrays={(m,c):data[m] for m,c in flow.NAMES}
        meta=pa.table({'row_index':np.arange(10000,10060),'period_start':np.repeat([2000,2005,2010,2015,2020],12)})
        design={**flow.D,'per_cell':12,'stability':{**flow.D['stability'],'repeats':2,'subset_per_period':6}}
        with tempfile.TemporaryDirectory() as td,patch.object(flow,'OUT',Path(td)),patch.object(flow,'D',design):
            flow.field_run(11,np.arange(60),meta,arrays)
            folder=Path(td)/'fields/11';commit=json.loads((folder/'commit.json').read_text())
            self.assertEqual(commit['independent_neighbor_queries'],300)
            with (folder/'neighbors.csv').open() as source:nn=list(csv.DictReader(source))
            self.assertEqual(len(nn),495)
            self.assertTrue(all(float(r['mean_overlap'])==1 for r in nn if r['kind']=='input'))
            with (folder/'effects.csv').open() as source:effects=list(csv.DictReader(source))
            self.assertTrue(all(abs(float(r['input_change_from_full']))<1e-10 for r in effects))
            before={p.name:file_sha(p) for p in folder.iterdir()}
            flow.field_run(11,np.arange(60),meta,arrays)
            self.assertEqual(before,{p.name:file_sha(p) for p in folder.iterdir()})
if __name__=='__main__':unittest.main()
