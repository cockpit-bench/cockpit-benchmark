"""Deterministic source-only census of the tracked, frozen reality cohort."""
import argparse, collections, hashlib, json, re, statistics, subprocess, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git(p,*args): return subprocess.check_output(['git','-C',str(p),*args],text=True,encoding='utf-8').strip()
def model_facts(path):
    with zipfile.ZipFile(path) as z:
        members=sorted(z.namelist()); systems={}
        for name in members:
            if re.fullmatch(r'simulink/systems/system_.*\.xml',name):
                systems[Path(name).stem]=ET.fromstring(z.read(name))
        blocks=[]; lines=[]; counts=collections.Counter(); subsystem_sizes=[]
        for key, system in systems.items():
            nodes=system.findall('Block'); subsystem_sizes.append({'system':key,'blocks':len(nodes)})
            for b in nodes:
                ps={v.get('Name'):v.text or '' for v in b.findall('P')}
                counts[b.get('BlockType')]+=1
                blocks.append({'system':key,'sid':b.get('SID'),'type':b.get('BlockType'),'name':b.get('Name'),
                               'parameters':ps,'child_system':b.find('System').get('Ref') if b.find('System') is not None else None,
                               'has_mask':b.find('Mask') is not None})
            for l in system.findall('Line'):
                ps={v.get('Name'):v.text or '' for v in l.findall('P')}
                lines.append({'system':key,'name':ps.get('Name',''),'source':ps.get('Src'),
                              'destinations':[p.text for p in l.findall('.//P[@Name="Dst"]')],
                              'points':ps.get('Points','')})
        defaults=[b for b in blocks if re.fullmatch(r'(?:In|Out)\d+',b['name'] or '')]
        params=[]
        for b in blocks:
            fields={'Constant':['Value'],'Gain':['Gain']}.get(b['type'],[])
            if b['type']=='Lookup_n-D':
                fields=sorted((k for k in b['parameters'] if re.fullmatch(r'BreakpointsForDimension\d+',k)),
                              key=lambda k:int(k.removeprefix('BreakpointsForDimension')))+['Table']
            for key in fields:
                value=b['parameters'].get(key)
                if value is not None:params.append({'sid':b['sid'],'system':b['system'],'block':b['name'],'field':key,'value':value,
                                                    'numeric_literal':bool(re.fullmatch(r'[\s\[\]0-9eE+.,;\-]+',value))})
        config={}
        for member in members:
            if re.fullmatch(r'simulink/configSet\d+\.xml',member):
                tree=ET.fromstring(z.read(member))
                config[member]={p.get('Name'):p.text for p in tree.iter('P') if p.get('Name') in
                 {'Solver','SolverName','SolverType','FixedStep','SystemTargetFile','TargetLang','HardwareBoard','ProdHWDeviceType','MaxStep'}}
        charts=[]
        for name in members:
            if name.startswith('simulink/stateflow/') and name.endswith('.xml'):
                tree=ET.fromstring(z.read(name))
                for value in tree.iter('P'):
                    if value.get('Name')=='script':charts.append({'member':name,'script':value.text or ''})
        return {'xml_members':members,'stateflow_scripts':charts,'system_xml_count':len(systems),'block_count':sum(counts.values()),
                'block_types':dict(sorted(counts.items())),'blocks':blocks,'lines':lines,'systems':subsystem_sizes,
                'default_ports':defaults,'default_port_count':len(defaults),'named_lines':sum(bool(x['name']) for x in lines),
                'parameter_slots':params,'config':config,'embedded_model_dictionary':'simulink/modelDictionary.xml' in members,
                'legacy_code_dictionary':any(x.endswith('/codeDictionary.xml') for x in members)}

def primary_model(row):
    """Select the executable module by name, never the first sorted library file."""
    matches=[(path,model) for path,model in row['models'].items() if Path(path).stem==row['name']]
    if len(matches)!=1:raise ValueError('Expected one named primary model: '+row['name'])
    return matches[0]

def source_path(source_root,row):
    """Accept the unified restore layout and the original cohort layout."""
    root=Path(source_root).resolve()
    choices=[root/row['name'],root/'new-energy-matlab'/row['name'],root/row['group']/row['name']]
    matches=[p for p in choices if (p/'.git').is_dir()]
    if len(matches)!=1:raise ValueError('Expected one restored source location: '+row['id'])
    if not matches[0].resolve().is_relative_to(root):raise ValueError('Source path escapes restore root')
    return matches[0]

def scan(manifest,source_root=None):
    result=[]
    for row in manifest['repositories']:
        repo=source_path(source_root,row) if source_root else Path(row['source_path'])
        files=git(repo,'-c','core.quotepath=false','ls-files').splitlines()
        binding={x:digest(repo/x) for x in files}; assert binding==row['files']
        head=git(repo,'rev-parse','HEAD'); assert head==row['head']
        models={x:model_facts(repo/x) for x in files if x.endswith('.slx')}
        result.append({'id':row['id'],'name':row['name'],'head':head,'tree':git(repo,'rev-parse','HEAD^{tree}'),
                       'files':binding,'extensions':dict(sorted(collections.Counter(Path(x).suffix for x in files).items())),
                       'models':models,'heads':[r.removeprefix('refs/heads/') for r in row['refs'] if r.startswith('refs/heads/')],
                       'tags':[r.removeprefix('refs/tags/') for r in row['refs'] if r.startswith('refs/tags/')],
                       'master_commits':int(git(repo,'rev-list','--count','master')),'tag_distinct_source_commits':row['tag_distinct_source_commits']})
    return {'schema':'ne-reality-census-1','cohort_id':manifest['cohort_id'],'repositories':result}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--manifest',required=True)
    parser.add_argument('--source-root');parser.add_argument('--output',required=True);args=parser.parse_args()
    result=scan(json.loads(Path(args.manifest).read_text(encoding='utf-8')),args.source_root)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for row in result['repositories']:
        _,m=primary_model(row);c=m['block_types']
        print(row['id'],m['block_count'],c.get('SubSystem',0),c.get('Inport',0),c.get('Outport',0),c.get('Reference',0),c.get('EnablePort',0))
