"""Stratified paired input pilot, separate from every frozen production run."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import torch

from sos_embed.models import Encoder, pool, format_text
from sos_embed.runner import (CACHE, INPUT, META_COLUMNS, config, environment,
                              source_files, snapshot_sources, verify_assets)
from sos_embed.storage import Store, file_sha, object_sha, run_lock, utcnow, write_json
from sos_analysis.extra_embeddings import NativeBlocks

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/'config/checklist_v1.json'
OUT=ROOT/'data/checklist_v1/inputs'


def sources():
    names=['sos_followup/input_embeddings.py','sos_analysis/extra_embeddings.py',
           'config/checklist_v1.json','config/embeddings_v1.json']
    return {**source_files(),**{n:file_sha(ROOT/n) for n in names}}


def condition_text(row,condition):
    if condition not in ('title','abstract'):raise ValueError('Single field required')
    value=row[condition]
    if not isinstance(value,str) or not value.strip():raise ValueError('Empty selected field')
    return value


def prepare():
    d=json.loads(DESIGN.read_text())
    definition={'source_sha256':file_sha(INPUT),'design_sha256':file_sha(DESIGN),
                'seed':d['seed'],'per_cell':d['per_cell'],'rows':d['rows']}
    with run_lock(OUT):
        p=OUT/'input_manifest.json'
        if p.exists():
            m=json.loads(p.read_text());assert m['definition']==definition
            for name,digest in m['files'].items():assert file_sha(OUT/name)==digest,name
            return m
        table=pq.read_table(INPUT)
        cells={}
        for row in table.select(META_COLUMNS).to_pylist():
            rank=hashlib.sha256((d['seed']+row['work_id']).encode()).digest()
            cells.setdefault((row['field_id'],row['period_start']),[]).append((rank,row['row_index']))
        if len(cells)!=130 or min(map(len,cells.values()))<d['per_cell']:raise ValueError('Missing cell')
        ids=sorted(i for v in cells.values() for _,i in sorted(v)[:d['per_cell']])
        selected=table.take(pa.array(ids))
        assert len(selected)==d['rows'] and len(set(ids))==d['rows']
        pq.write_table(selected,OUT/'native_input.parquet',compression='zstd')
        counts=[]
        for (f,p),v in sorted(cells.items()):counts.append({'field_id':f,'period_start':p,'available':len(v),'selected':d['per_cell']})
        for condition in ['title','abstract']:
            rows=selected.to_pylist()
            for row in rows:
                text=condition_text(row,condition)
                row['source_text_sha256']=row['text_sha256']
                row['text_sha256']=hashlib.sha256(text.encode()).hexdigest()
                row['input_condition']=condition
            pq.write_table(pa.Table.from_pylist(rows),OUT/(condition+'_input.parquet'),compression='zstd')
        m={'definition':definition,'completed_at':utcnow(),'cells':counts,
           'files':{n:file_sha(OUT/n) for n in ['native_input.parquet','title_input.parquet','abstract_input.parquet']}}
        write_json(OUT/'input_manifest.json',m)
        return m


class LiteralEncoder(Encoder):
    """Same weights/forward/poolings; literal single field without empty separators."""
    def encode_literal(self, rows, condition, batch_size=16):
        start=time.monotonic()
        texts=[condition_text(r,condition) for r in rows]
        full=self.tokenizer(texts,truncation=False,padding=False,return_token_type_ids=False,verbose=False)['input_ids']
        outputs={p:[] for p in self.spec['poolings']};audit=[]
        with torch.inference_mode():
            for offset in range(0,len(texts),batch_size):
                chosen=texts[offset:offset+batch_size]
                batch=self.tokenizer(chosen,padding=True,truncation=True,max_length=self.spec['max_length'],
                      return_tensors='pt',return_token_type_ids=False,return_offsets_mapping=True)
                positions=batch.pop('offset_mapping').tolist()
                for j,(ids,mask,spans) in enumerate(zip(batch['input_ids'].tolist(),batch['attention_mask'].tolist(),positions)):
                    n=sum(mask);ids=ids[:n];text=chosen[j]
                    audit.append({'tokens_original':len(full[offset+j]),'tokens_used':n,
                          'truncated':len(full[offset+j])>self.spec['max_length'],
                          'formatted_text_sha256':hashlib.sha256(text.encode()).hexdigest(),
                          'token_ids_sha256':hashlib.sha256(struct.pack('<'+'I'*n,*ids)).hexdigest(),
                          'last_content_character':max(b for a,b in spans[:n]),'formatted_characters':len(text)})
                batch={k:v.to(self.device) for k,v in batch.items()}
                hidden=self.model(**batch).last_hidden_state
                for name in outputs:outputs[name].append(pool(hidden,batch['attention_mask'],name).cpu().numpy())
        if self.device=='mps':torch.mps.synchronize()
        return {k:np.concatenate(v).astype(np.float32,copy=False) for k,v in outputs.items()},audit,{'seconds':time.monotonic()-start,'rows':len(rows),'truncated_rows':sum(a['truncated'] for a in audit),'batch_size':batch_size}


def run_model(key, max_shards=None):
    inp=prepare();d=json.loads(DESIGN.read_text());spec=next(m for m in config()['models'] if m['key']==key)
    native=NativeBlocks(key);assets=verify_assets(spec)
    torch.set_num_threads(8);torch.manual_seed(20260917)
    encoder=None
    with run_lock(OUT/'locks'/key):
        for condition in ['title_abstract','title','abstract']:
            path=OUT/(('native' if condition=='title_abstract' else condition)+'_input.parquet')
            expected=pq.read_table(path,columns=META_COLUMNS)
            manifest={'schema_version':1,'scope':'input_pilot','model':spec,'condition':condition,
                      'rows':d['rows'],'dimension':spec['dimension'],'poolings':spec['poolings'],
                      'input_sha256':file_sha(path),'selection_manifest_sha256':file_sha(OUT/'input_manifest.json'),
                      'native_manifest_sha256':native.model['manifest_sha256'],'source_files':sources(),
                      'environment':environment(),'asset_records':assets,'dtype':'float32','device':'mps',
                      'batch_size':16,'shard_size':1024,'postprocessing':'none','seed':20260917}
            folder=OUT/condition/key;snapshot_sources(OUT,manifest['source_files'])
            store=Store(folder,manifest);state=store.scan(expected)
            if state['complete']:print(condition,key,'already complete',flush=True);continue
            if condition!='title_abstract' and encoder is None:encoder=LiteralEncoder(spec,CACHE,'mps')
            completed=0;offset=0
            for batch in pq.ParquetFile(path).iter_batches(batch_size=1024):
                end=offset+batch.num_rows
                if end<=state['rows']:offset=end;continue
                if offset<state['rows']:raise ValueError('Partial shard boundary')
                table=pa.Table.from_batches([batch]);rows=table.to_pylist();t=time.monotonic()
                if condition=='title_abstract':
                    vectors={p:[] for p in spec['poolings']};audits=[]
                    for r in rows:
                        original,vec=native.row(r['row_index'])
                        if any(original[k]!=r[k] for k in ['row_index','work_id','text_sha256']):raise ValueError('Native identity mismatch')
                        for p in vectors:vectors[p].append(vec[p].copy())
                        audits.append({k:original[k] for k in ['tokens_original','tokens_used','truncated','formatted_text_sha256','token_ids_sha256','last_content_character','formatted_characters']})
                    vectors={p:np.stack(x) for p,x in vectors.items()}
                    stats={'seconds':time.monotonic()-t,'rows':len(rows),'reused_rows':len(rows),'truncated_rows':sum(x['truncated'] for x in audits)}
                else:
                    vectors,audits,stats=encoder.encode_literal(rows,condition)
                    stats['reused_rows']=0
                meta=table.select(META_COLUMNS)
                if 'source_text_sha256' in table.column_names:meta=meta.append_column('source_text_sha256',table['source_text_sha256'])
                for k in audits[0]:meta=meta.append_column(k,pa.array([x[k] for x in audits]))
                store.commit(offset,meta,vectors,stats)
                write_json(folder/'progress.json',{'state':'running','rows':end,'target':d['rows'],'updated_at':utcnow(),'last_shard':stats})
                print(f'{key}/{condition}: {end:,}/{d["rows"]:,} — {len(rows)/max(stats["seconds"],.001):.1f} artículos/s',flush=True)
                offset=end;completed+=1
                if max_shards and completed>=max_shards:break
            result={**store.scan(expected),'updated_at':utcnow()}
            write_json(folder/'validation.json',result)
            write_json(folder/'progress.json',{**result,'state':'complete' if result['complete'] else 'paused'})
            if not result['complete']:return


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','model','all']);p.add_argument('--model');p.add_argument('--max-shards',type=int);a=p.parse_args()
    if a.action=='prepare':print(json.dumps(prepare()),flush=True)
    elif a.action=='model':run_model(a.model,a.max_shards)
    else:
        prepare()
        with run_lock(OUT/'queue'):
            for spec in config()['models']:
                subprocess.run([sys.executable,'-m','sos_followup.input_embeddings','model','--model',spec['key']],cwd=ROOT,check=True)
        print('ALL INPUT CONDITIONS COMPLETE',flush=True)

if __name__=='__main__':main()
