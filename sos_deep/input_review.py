"""Close the nested input pilot, recipe effects and all original alert keys."""
import json
from collections import defaultdict,Counter
import numpy as np
from scipy.stats import spearmanr
from sos_deep.artifacts import ROOT,read_csv,save_csv,verify_audit,freeze,finish
from sos_deep.control_review import stats
from sos_embed.storage import write_json,run_lock

BASE=ROOT/'data/robustness_v2';OUT=BASE/'input_review'
WORD={'bert','scibert','biobert','pubmedbert'}


def grouped(rows,keys,columns):
    groups=defaultdict(list)
    for r in rows:groups[tuple(r[k] for k in keys)].append(r)
    out=[]
    for key,rs in groups.items():
        for col in columns:
            values=[float(r[col]) for r in rs]
            out.append({**dict(zip(keys,key)),'measure':col,**stats(values),
                        'positive_count':sum(v>0 for v in values),'negative_count':sum(v<0 for v in values)})
    return out


def main():
    with run_lock(OUT):
        names=['input_comparisons','input_recipes','input_stability100']
        for name in names:verify_audit(BASE/name)
        audit=json.loads((ROOT/'research/robustness_2026-09-17/input_audit/audit_summary.json').read_text())
        assert audit['all_complete'] and audit['complete_conditions']==30
        freeze(OUT,['sos_deep/input_review.py','sos_deep/artifacts.py','sos_deep/control_review.py'],
               [f'data/robustness_v2/{n}/audit.json' for n in names]+
               ['research/robustness_2026-09-17/input_audit/audit_summary.json'],
               {'purpose':'R01 R02 R09 exact nested pilot and recipe/alert summary',
                'primary_recipe':'mean for four word BERTs','no_posthoc_recipe_selection':True})
        effect=read_csv(BASE/'input_comparisons/effects.csv')
        cols=['model_change_at_full','input_change_from_full','model_minus_input']
        save_csv(OUT/'input_effect_summary.csv',grouped(effect,['metric','input_condition'],cols))
        save_csv(OUT/'input_effect_by_model.csv',grouped(effect,['metric','input_condition','model'],cols))
        save_csv(OUT/'input_effect_by_field.csv',grouped(effect,['metric','input_condition','field_id'],cols))
        old=read_csv(ROOT/'data/checklist_v1/input_comparisons/effects.csv')
        oldat={(r['field_id'],r['metric'],r['model'],r['input_condition']):r for r in old}
        changes=[]
        for r in effect:
            ref=oldat[r['field_id'],r['metric'],r['model'],r['input_condition']]
            a=float(ref['model_minus_input']);b=float(r['model_minus_input'])
            changes.append({k:r[k] for k in ['field_id','metric','model','input_condition']}|
                {'effect26k':a,'effect52k':b,'difference':b-a,'sign_changed':bool(np.sign(a)!=np.sign(b))})
        save_csv(OUT/'nested_sample_effect_changes.csv',changes)
        recipe=read_csv(BASE/'input_recipes/effects.csv')
        save_csv(OUT/'recipe_effect_summary.csv',grouped(recipe,['recipe','metric','input_condition'],cols))
        base={(r['field_id'],r['metric'],r['model'],r['input_condition']):r for r in recipe if r['recipe']=='mean'}
        sensitivity=[]
        for r in recipe:
            if r['recipe']=='mean':continue
            ref=base[r['field_id'],r['metric'],r['model'],r['input_condition']]
            a=float(ref['model_minus_input']);b=float(r['model_minus_input'])
            sensitivity.append({k:r[k] for k in ['field_id','recipe','metric','model','input_condition']}|
                {'is_word_bert':r['model'] in WORD,'mean_effect':a,'alternative_effect':b,
                 'effect_change':b-a,'input_change_difference':float(r['input_change_from_full'])-float(ref['input_change_from_full']),
                 'model_change_difference':float(r['model_change_at_full'])-float(ref['model_change_at_full']),
                 'sign_changed':bool(np.sign(a)!=np.sign(b))})
        save_csv(OUT/'recipe_sensitivity_all_cases.csv',sensitivity)
        signs=[]
        for recipe_name in ['cls','sep']:
            for metric in ['cka','neighbors10','neighbors25','neighbors50']:
                for cond in ['title','abstract']:
                    for scope in ['all_ten','four_word_berts']:
                        rs=[r for r in sensitivity if r['recipe']==recipe_name and r['metric']==metric
                            and r['input_condition']==cond and (scope=='all_ten' or r['is_word_bert'])]
                        signs.append({'recipe':recipe_name,'metric':metric,'input_condition':cond,'scope':scope,
                                      'cases':len(rs),'sign_changes':sum(r['sign_changed'] for r in rs),
                                      'mean_effect_change':float(np.mean([r['effect_change'] for r in rs])),
                                      'max_absolute_effect_change':max(abs(r['effect_change']) for r in rs)})
        save_csv(OUT/'recipe_sign_changes.csv',signs)
        transitions=read_csv(BASE/'input_stability100/alert_transitions.csv');counts=[]
        for rep in ['20','100']:
            for scope in ['individual_models','area_means']:
                rs=[r for r in transitions if r['repeats']==rep and
                    ((r['model']=='mean_of_ten_fixed_models')==(scope=='area_means'))]
                c=Counter(r['transition'] for r in rs)
                counts.append({'repeats':int(rep),'scope':scope,'comparisons':len(rs),
                    'alerts26k':sum(r['alert26k']=='True' for r in rs),'alerts52k':sum(r['alert52k']=='True' for r in rs),
                    **{k:c[k] for k in ['persists','resolved','new','no_alert']},
                    'crosses_zero26k':sum(r['crosses_zero26k']=='True' for r in rs),
                    'crosses_zero52k':sum(r['crosses_zero52k']=='True' for r in rs)})
        assert counts[0]['alerts26k']==31
        save_csv(OUT/'alert_transition_counts.csv',counts)
        save_csv(OUT/'original31_tracking.csv',[r for r in transitions if r['original_31_alert']=='True'])
        current=[r for r in transitions if r['alert52k']=='True']
        if current:
            save_csv(OUT/'current52_alerts.csv',current)
        else:
            import csv
            with (OUT/'current52_alerts.csv').open('w') as f:
                csv.DictWriter(f,fieldnames=list(transitions[0])).writeheader()
        audits=[json.loads(p.read_text()) for p in (ROOT/'research/robustness_2026-09-17/input_audit').glob('*.json') if p.name!='audit_summary.json']
        assert len(audits)==30 and all(a['all_pass'] for a in audits)
        summary={'conditions':30,'model_article_input_rows':sum(a['rows'] for a in audits),
            'native_exact_reuse':sum(a['native_exact_reuse'] for a in audits),
            'pilot_exact_reuse':sum(a['pilot26k_exact_reuse'] for a in audits),
            'new_inference_rows':sum(a['new_inference_rows'] for a in audits),
            'alert_counts':counts,'recipe_primary_unchanged':True,
            'recipe_cases':len(sensitivity),'recipe_sign_counts':signs,
            'population_confidence_intervals':False}
        write_json(OUT/'summary.json',summary);finish(OUT,all_original_31_keys_retained=True,
                                                    all_30_input_conditions_audited=True)
        print('INPUT CLOSURE REVIEW COMPLETE',flush=True)


if __name__=='__main__':main()
