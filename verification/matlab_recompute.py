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

def unit_test(t):
 """Score reviewed valid tests; unknown pass evidence cannot establish a tier.

 ``present`` retains the existing meaning of valid tests with suitable method.
 Existing bound all-passed records establish a majority without invented counts.
 Partial runs require explicit passed/total counts to establish a majority.
 """
 if not isinstance(t,dict) or any(type(t.get(k)) is not bool for k in ('present','all_passed')):
  raise ValueError('Missing or invalid test status')
 cv=t.get('decision');ratio=None
 if cv is not None:
  if not isinstance(cv,(list,tuple)) or len(cv)!=2 or any(type(n) is not int for n in cv) or not 0<=cv[0]<=cv[1]:
   raise ValueError('Invalid decision coverage counts')
  if cv[1]:ratio=cv[0]/cv[1]
 passed=t.get('passed');total=t.get('total')
 if passed is not None or total is not None:
  if type(passed) is not int or type(total) is not int or not 0<=passed<=total:
   raise ValueError('Invalid test pass counts')
  if t['all_passed']!=(total>0 and passed==total):raise ValueError('Test status conflicts with pass counts')
  if t['present'] and total==0:raise ValueError('Valid tests require a nonzero test count')
 if not t['present']:
  if t['all_passed'] or (total is not None and total>0) or (cv is not None and cv[1]>0):
   raise ValueError('Absent tests conflict with execution evidence')
  return 0
 if ratio is None or ratio<.5:return 1
 if t['all_passed']:return 5 if ratio>=.8 else 3
 if total is None:return None
 return 3 if passed*2>total else 1

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
 if o['parameters'] is None:r['parameter_management']=None
 r['unit_test']=unit_test(f['source_tests'])
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
