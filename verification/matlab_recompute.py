"""Separate contract recomputation; does not import primary scorer or target roles.
Semantic facts remain reviewed inputs: arithmetic independence is not independent semantic review.
"""
import json,re
from pathlib import Path

def build_independence(dependencies):
 """Repository boundary; missing dependency classification is unknown, never zero."""
 if not isinstance(dependencies,list):return None
 if not dependencies:return 3
 scores=[]
 for dep in dependencies:
  if not isinstance(dep,dict):return None
  keys=['version_managed','release_baseline','version_locked','interface_component']
  if any(type(dep.get(k)) is not bool for k in keys):return None
  if all(dep[k] for k in keys[:3]):scores.append(3)
  elif dep['interface_component']:scores.append(2)
  elif dep.get('delivery') in {'precompiled','protected_model'}:scores.append(1)
  elif dep.get('delivery')=='source':scores.append(0)
  else:return None
 return min(scores)

def recompute(f):
 o=f['semantic_observations'];r={}
 conditions={
 'hierarchy':[(3,o['hierarchy']=='uniform_single_responsibility'),(2,o['hierarchy']=='clear_uneven'),(1,o['hierarchy']=='coarse')],
 'reuse':[(3,o['reuse']=='linked_encapsulation'),(2,o['reuse']=='encapsulated_without_duplicate'),(1,o['reuse']=='duplicate')],
 'interface':[(3,o['interface']=='controlled'),(2,o['interface']=='explicit_complete'),(1,o['interface']=='incomplete')],
 'dataflow':[(3,o['routing']=='consistent'),(2,o['routing']=='mostly_clear'),(1,o['routing']=='partial')],
 'naming':[(5,o['naming']=='accurate'),(3,o['naming']=='mostly_meaningful'),(1,o['naming']=='partial')],
 'directory':[(5,o['directory']=='separated'),(3,o['directory']=='reasonable'),(1,o['directory']=='partial')],
 'model_version':[(3,o['history']=='complete'),(2,o['history']=='dated_major'),(1,o['history']=='partial')],
 'parameter_management':[(5,o['parameters']=='central_accurate'),(3,o['parameters']=='external_classified'),(1,o['parameters']=='partial')]}
 for leaf,predicates in conditions.items():r[leaf]=next((v for v,ok in predicates if ok),0)
 t=f['source_tests'];cv=t['decision'];ratio=cv[0]/cv[1] if cv and cv[1] else -1
 r['unit_test']=5 if t['present'] and t['all_passed'] and ratio>=.8 else 3 if t['present'] and ratio>=.5 else 1 if t['present'] else 0
 r['build_independence']=build_independence(f.get('external_business_dependencies'))
 v=f['version'];parts=v.split('_')[0].split('.');r['version_independence']=3 if len(parts)==3 and all(x.isdecimal() for x in parts) else 1 if v.startswith('R') and v[1:].isdecimal() else 0
 # Derive branch predicates from actual refs rather than the primary release descriptors.
 branches=f['branches']
 if branches==['main']:r['release_branches']=10;r['device_specificity']=10
 elif all(x.startswith('platform/VCU-') for x in branches) and len(branches)==2:r['release_branches']=8;r['device_specificity']=8
 elif len(branches)==1 and re.fullmatch(r'C\d{3}-SOP',branches[0]):r['release_branches']=3;r['device_specificity']=0
 else:raise ValueError('Unreviewed branch topology')
 return r

if __name__=='__main__':
 import argparse
 root=Path(__file__).resolve().parents[1]
 parser=argparse.ArgumentParser();parser.add_argument('--suite-root',type=Path,default=root/'suite-fix3');parser.add_argument('--evidence-root',type=Path,default=root/'evidence/final-fix3');args=parser.parse_args()
 standard=json.loads((args.suite_root/'STANDARD_SCORES.json').read_text());diff=[];count=0
 for row in standard['repos']:
  f=json.loads((args.evidence_root/row['id']/'facts.json').read_text());actual=recompute(f)
  for leaf,want in row['scores'].items():
   count+=1
   if actual[leaf]!=want:diff.append({'id':row['id'],'leaf':leaf,'expected':want,'actual':actual[leaf]})
 assert count==117 and not diff,(count,diff)
 (args.evidence_root/'recompute.json').write_text(json.dumps({'status':'passed','leaves':count,'differences':diff,'scope':'Independent code and branch derivation; shared explicit semantic observations'},indent=2)+'\n')
 print(count,'leaves, zero differences')
