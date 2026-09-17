"""Independent closure audit of expanded analysis outputs and paired selections."""
import json
from collections import Counter
import numpy as np
import pyarrow.parquet as pq
from sos_deep.artifacts import ROOT,read_csv,save_csv,verify_audit,freeze,finish
from sos_embed.storage import file_sha,write_json,run_lock

BASE=ROOT/'data/robustness_v2';OUT=BASE/'final_audit'
REQUIRED=['subfields_native','subfield_controls','regions_native','temporal_review','family_traits',
          'medicine_composition','centroid_scales','paired_neighbor_scales','control_review_v2',
          'structural_review_v3','provenance','input_comparisons','input_recipes','input_stability100','input_review']


def check_commits(folder):
    counts=Counter()
    for path in sorted(folder.rglob('commit.json')):
        c=json.loads(path.read_text())
        for name,digest in c.get('files',{}).items():
            assert file_sha(path.parent/name)==digest,(path,name);counts['committed_files']+=1
        if 'neighbors_sha256' in c:
            assert file_sha(path.parent/'neighbors.npy')==c['neighbors_sha256'];counts['neighbor_arrays']+=1
        counts['commits']+=1
    for path in sorted(folder.glob('*.commit.json')):
        c=json.loads(path.read_text())
        assert file_sha(path.with_name(path.name.replace('.commit.json','.npz')))==c['sha256']
        counts['centroid_arrays']+=1
    return counts


def paired_selection_audit(meta):
    field=meta['field_id'].to_numpy();sf=meta['subfield_id'].to_numpy().astype(str)
    period=meta['period_start'].to_numpy();p=BASE/'paired_neighbor_scales'
    q=np.load(p/'query_ids.npy');c=np.load(p/'candidate_ids.npy');count=np.load(p/'shared_counts.npy',mmap_mode='r')
    assert q.shape==(217,50) and c.shape==(10,217,2,256) and count.shape==(10,217,2,50,45,3)
    records={(r['subfield_id'],int(r['repeat']),r['scope'],int(r['k'])):r for r in read_csv(p/'groups.csv')}
    names=np.unique(sf[q],axis=0)
    assert all(len(set(sf[a]))==1 for a in q)
    cases=0
    for rep in range(10):
        for gi in range(217):
            a,b=c[rep,gi];query=q[gi]
            assert len(set(a))==len(set(b))==256
            assert set(query)<=set(a) and set(query)<=set(b)
            assert np.array_equal(np.sort(period[a]),np.sort(period[b]))
            assert np.all(sf[a]==sf[query[0]]) and np.all(field[b]==field[query[0]])
            for si,scope in enumerate(['subfield','field']):
                for ki,k in enumerate([10,25,50]):
                    actual=float(count[rep,gi,si,:,:,ki].mean()/k)
                    saved=float(records[sf[query[0]],rep,scope,k]['mean_overlap'])
                    assert abs(actual-saved)<1e-12
            cases+=1
    return {'paired_query_sets':len(q),'query_rows':len(np.unique(q)),
            'repeated_paired_candidate_sets':cases,'raw_neighbor_counts_reproduce_all_group_means':True}


def composition_selection_audit(meta):
    field=meta['field_id'].to_numpy();sf=meta['subfield_id'].to_numpy().astype(str);period=meta['period_start'].to_numpy()
    p=BASE/'medicine_composition';coverage={int(r['field_id']):r for r in read_csv(p/'coverage.csv')}
    checked=0
    for f in range(11,37):
        eligible=coverage[f]['subfield_ids'].split('|')
        for rep in range(10):
            for condition in ['observed_eligible_composition','equal_subfield_composition']:
                ids=np.load(p/'groups'/str(f)/str(rep)/condition/'row_indices.npy')
                assert len(ids)==len(set(ids))==2048 and np.all(field[ids]==f)
                assert set(sf[ids])<=set(eligible)
                for year,n in zip([2000,2005,2010,2015,2020],[410,410,410,409,409]):
                    subset=ids[period[ids]==year];assert len(subset)==n
                    if condition=='equal_subfield_composition':
                        counts=[int((sf[subset]==group).sum()) for group in eligible]
                        assert max(counts)-min(counts)<=1
                checked+=1
    return {'composition_selections':checked,'same_dates_sizes_and_eligible_subfields_verified':True}


def main():
    with run_lock(OUT):
        results=[]
        for name in REQUIRED:
            folder=BASE/name;a=verify_audit(folder)
            manifest=json.loads((folder/'manifest.json').read_text())
            for file,digest in manifest['source_files'].items():
                assert file_sha(ROOT/file)==digest,(name,file,'current')
                assert file_sha(folder/'source_snapshot'/file)==digest,(name,file,'saved')
            for file,digest in manifest.get('parent_files',{}).items():
                assert file_sha(ROOT/file)==digest,(name,file,'parent')
            counts=check_commits(folder)
            results.append({'component':name,'audit_sha256':file_sha(folder/'audit.json'),
                'manifest_sha256':file_sha(folder/'manifest.json'),'all_complete':True,
                'commits':counts['commits'],'committed_files':counts['committed_files'],
                'centroid_arrays':counts['centroid_arrays'],'neighbor_arrays':counts['neighbor_arrays']})
            print('CLOSURE AUDIT',name,'PASS',flush=True)
        freeze(OUT,['sos_deep/audit_closure.py','sos_deep/artifacts.py'],
               [f'data/robustness_v2/{n}/audit.json' for n in REQUIRED],
               {'required_components':REQUIRED,'scientific_sources_and_raw_commits_checked':True,
                'numerical_checks':'Independently reconstruct selected candidate identities, dates, sizes and neighbor means'})
        meta=pq.read_table(ROOT/'data/analysis_ready_v1/metadata.parquet')
        assert len(meta)==500000 and len(set(meta['work_id'].to_pylist()))==500000
        inp=pq.read_table(BASE/'inputs/native_input.parquet');old=pq.read_table(ROOT/'data/checklist_v1/inputs/native_input.parquet')
        assert len(inp)==52000 and set(old['row_index'].to_pylist())<set(inp['row_index'].to_pylist())
        c=Counter(zip(inp['field_id'].to_pylist(),inp['period_start'].to_pylist()))
        assert len(c)==130 and set(c.values())=={400}
        nbs=paired_selection_audit(meta);medicine=composition_selection_audit(meta)
        table=pq.read_table(BASE/'regions_native/paper_agreement.parquet',columns=['row_index','work_id'])
        assert len(table)==500000 and table['work_id'].to_pylist()==meta['work_id'].to_pylist()
        save_csv(OUT/'component_verification.csv',results)
        write_json(OUT/'summary.json',{'all_complete':True,'components':len(results),
            'input_rows':52000,'nested_old_rows':26000,'input_cells':130,'rows_per_cell':400,
            'all500k_paper_ids_preserved':True,'source_hashes_and_saved_copies_match':True,
            **nbs,**medicine,'prior_failed_exporters_excluded':['structural_review','structural_review_v2'],
            'superseded_control_summary':'control_review; use control_review_v2 to separate MiniLM self-comparison'})
        finish(OUT,all_required_components_verified=True,paired_selection_checks_pass=True)
        print('EXPANDED EXPERIMENTAL CLOSURE AUDITED',flush=True)


if __name__=='__main__':main()
