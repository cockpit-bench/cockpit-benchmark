"""Read-only inventories supporting the scoped parameter/reuse adjudications.

These functions derive coordinates and graph comparisons, never semantic scores.
They read source files only; no MATLAB callbacks or candidate code are executed.
"""
import collections
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

from suites import encoded, sha, require


def workbook_rows(path):
    """Read the first existing XLSX sheet, preserving cell addresses and empty cells."""
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as archive:
        shared=[]
        if 'xl/sharedStrings.xml' in archive.namelist():
            shared=[''.join(node.itertext()) for node in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        rows=[]
        for row in ET.fromstring(archive.read('xl/worksheets/sheet1.xml')).findall('.//s:row',ns):
            values={}
            for cell in row.findall('s:c',ns):
                element=cell.find('s:v',ns);value='' if element is None else element.text
                if cell.get('t')=='s':value=shared[int(value)]
                elif cell.get('t')=='inlineStr':value=''.join(cell.find('s:is',ns).itertext())
                column=re.match('[A-Z]+',cell.attrib['r']).group()
                values[column]=value
            rows.append((int(row.attrib['r']),values))
    headers=rows[0][1]
    return [{'worksheet_row':number,**{header:values.get(column,'') for column,header in headers.items()}} for number,values in rows[1:]]


def model_systems(path):
    with zipfile.ZipFile(path) as archive:
        return {name:ET.fromstring(archive.read(name)) for name in archive.namelist()
                if name.startswith('simulink/systems/') and name.endswith('.xml')}


def model_blocks(path):
    systems=model_systems(path);result=[]
    def walk(member,prefix):
        for block in systems[member].findall('Block'):
            name=block.attrib['Name'];full=prefix+'/'+name if prefix else name
            params={p.attrib['Name']:p.text or '' for p in block.findall('P')}
            result.append({'member':member,'sid':block.attrib['SID'],'path':full,'name':name,'type':block.attrib['BlockType'],'parameters':params})
            child=block.find('System')
            if child is not None and 'Ref' in child.attrib:walk('simulink/systems/'+child.attrib['Ref']+'.xml',full)
    walk('simulink/systems/system_root.xml','')
    return result


CALIBRATION_FIELDS={'Constant':['Value'],'Gain':['Gain'],'Saturate':['LowerLimit','UpperLimit'],
                    'UnitDelay':['InitialCondition'],'Switch':['Threshold']}
STRUCTURAL_TYPES={'Inport','Outport','RelationalOperator','Sum','Logic','SubSystem','MinMax',
                  'Product','ModelReference','DataTypeConversion','Abs'}

def parameter_inventory(repo):
    repo=Path(repo);graph=json.loads((repo/'Model/model.json').read_text())
    rows=workbook_rows(repo/'Documentation/Calibration.xlsx');table={row['Parameter']:row for row in rows}
    require(len(table)==len(rows),'Duplicate calibration row')
    models=['Model/'+graph['model']+'.slx']+['Model/'+r['model']+'.slx' for r in graph['model_references']]
    actual={name:[] for name in table};excluded=[];unmanaged=[];model_inventory=[];reference_arguments=[]
    for model in models:
        blocks=model_blocks(repo/model)
        types=collections.Counter(b['type'] for b in blocks)
        require(set(types)<=set(CALIBRATION_FIELDS)|STRUCTURAL_TYPES,'Unreviewed production block type; calibration scope must be extended explicitly')
        model_inventory.append({'path':model,'sha256':sha((repo/model).read_bytes()),'block_count':len(blocks),'block_types':dict(sorted(types.items()))})
        for member,system in model_systems(repo/model).items():
            for block in system.findall("Block[@BlockType='ModelReference']"):
                names=[x.text for x in block.findall("Array[@PropName='ParameterArgumentNames']/String")]
                values=[x.text for x in block.findall("Array[@PropName='ParameterArgumentValues']/String")]
                flags=block.find("P[@Name='UsingDefaultArgumentValue']").text.split(',')
                spec=next(r for r in graph['model_references'] if r['subsystem']==block.attrib['Name'])
                require(names==values and sorted(names)==sorted(spec['parameters']) and len(flags)==len(names) and set(flags)=={'0'},'Reference arguments bypass calibration variables')
                reference_arguments.append({'model':model,'member':member,'sid':block.attrib['SID'],'parameters':names,'expressions':values,'uses_default_values':False})
        for block in blocks:
            for field in CALIBRATION_FIELDS.get(block['type'],[]):
                expression=block['parameters'].get(field)
                if expression is None:
                    # All executable numeric slots must be explicit, except a Switch threshold
                    # that does not participate in the selected boolean criterion.
                    if block['type']=='Switch' and block['parameters'].get('Criteria')=='u2 ~= 0':continue
                    unmanaged.append({'model':model,**block,'field':field,'expression':'<inherited default>'});continue
                record={'model':model,'member':block['member'],'sid':block['sid'],'block_path':block['path'],'field':field,'expression':expression}
                if expression in table:actual[expression].append(record)
                elif block['type']=='Switch' and block['parameters'].get('Criteria')=='u2 ~= 0':excluded.append({**record,'reason':'Inactive threshold of the boolean u2 ~= 0 selection operator'})
                elif expression in {'true','false'}:excluded.append({**record,'reason':'Fixed boolean truth value, not an adjustable physical calibration'})
                else:unmanaged.append(record)
            sample_time=block['parameters'].get('SampleTime')
            if sample_time is not None:
                excluded.append({'model':model,'member':block['member'],'sid':block['sid'],'block_path':block['path'],'field':'SampleTime','expression':sample_time,'reason':'Execution timing is centrally defined by Model/model.json period and the reconstruction/configuration code; it is not one of the 201 calibration-table parameters'})
    expected=set(graph['parameters'])
    require(set(table)==expected,'Table differs from declared graph parameters')
    result=[]
    for name,row in sorted(table.items()):
        consumers=[]
        for node in graph['nodes']:
            for field,expression in node['parameters'].items():
                if re.search(r'(?<![A-Za-z0-9_])'+re.escape(name)+r'(?![A-Za-z0-9_])',str(expression)):
                    consumers.append(node['id']+'.'+field)
        require(row['Consumers']=='; '.join(consumers) and consumers,'Declared consumers differ: '+name)
        require(actual[name],'No production SLX parameter consumption: '+name)
        require(float(row['Value'])==float(graph['parameters'][name]),'Table/graph value differs: '+name)
        require(row['DataType']=='double' and row['Unit'] and row['Group'],'Missing type/unit/group: '+name)
        mapped=[]
        for use in actual[name]:
            prefix='' if use['model']==models[0] else next(r['subsystem']+'/' for r in graph['model_references'] if use['model']=='Model/'+r['model']+'.slx')
            mapped.append(prefix+use['block_path']+'.'+use['field'])
        require(sorted(mapped)==sorted(consumers),'SLX and graph consumer sets differ: '+name)
        result.append({'name':name,'worksheet_row':row['worksheet_row'],'value':float(row['Value']),'data_type':row['DataType'],'unit':row['Unit'],'group':row['Group'],'declared_consumers':consumers,'actual_consumers':actual[name]})
    return {'schema':'parameter-scope-audit-v1','models':model_inventory,'managed_parameter_count':len(result),
            'parameters':result,'unmanaged_calibration_slots':unmanaged,'excluded_slots':excluded,
            'model_reference_arguments':reference_arguments,
            'scope_basis':'Enumerate every block in both production root/reference models before matching table rows. Constant values, gains, saturation limits, delays and active switch thresholds are calibration slots. Remaining reviewed types are port/routing/structural or fixed algebraic/boolean operators; their port counts, signs, comparison direction, conversion type and model-reference configuration define structure rather than tunable physical calibration. Unknown block types are rejected.',
            'separate_timing_configuration':{'path':'Model/model.json','json_pointer':'/period','value':graph['period'],'unit':'s'},
            'limits':'Inventory and expression/value consistency only. Unit semantics, physical-purpose plausibility, exclusion rationale and score are explicit human review. One native perturbation is not full parameter sensitivity coverage.'}


def graph_signature(system):
    """Normalize only local IDs/layout/labels; retain block types, ports and edges."""
    blocks=system.findall('Block');ids={b.attrib['SID']:i for i,b in enumerate(blocks)}
    def endpoint(value):
        sid,port=value.split('#',1);return [ids[sid],port]
    edges=[]
    for line in system.findall('Line'):
        src=line.find("P[@Name='Src']").text
        for dst in line.iter('P'):
            if dst.get('Name')=='Dst':edges.append([endpoint(src),endpoint(dst.text)])
    return {'block_types':[b.attrib['BlockType'] for b in blocks],
            'ports':[b.find('PortCounts').attrib if b.find('PortCounts') is not None else {} for b in blocks],
            'edges':sorted(edges)}


def reuse_inventory(repo):
    repo=Path(repo);path='BatteryContactorController.slx';systems=model_systems(repo/path)
    groups=[]
    for member,system in sorted(systems.items()):
        for block in system.findall('Block'):
            if not block.attrib['Name'].endswith('_Fault_State'):continue
            child='simulink/systems/'+block.find('System').attrib['Ref']+'.xml';body=systems[child]
            parameters=[];wrappers=[]
            for inner in body.findall('Block'):
                p={x.get('Name'):x.text for x in inner.findall('P')}
                if inner.attrib['BlockType'] in {'Constant','RelationalOperator'}:
                    parameters.append({'sid':inner.attrib['SID'],'name':inner.attrib['Name'],'type':inner.attrib['BlockType'],**{key:p[key] for key in ['Value','Operator'] if key in p}})
                if inner.find('System') is not None:
                    wrapped='simulink/systems/'+inner.find('System').attrib['Ref']+'.xml'
                    linked=[]
                    for nested in systems[wrapped].findall('Block'):
                        ps={x.get('Name'):x.text for x in nested.findall('P')}
                        if ps.get('SourceBlock')=='BMSLib/Debouncer':linked.append({'member':wrapped,'sid':nested.attrib['SID'],'name':nested.attrib['Name'],'source_block':ps['SourceBlock']})
                    wrappers.append({'member':wrapped,'signature':graph_signature(systems[wrapped]),'links':linked,
                        'constant_expressions':[x.text for x in systems[wrapped].findall("Block[@BlockType='Constant']/P[@Name='Value']")]})
            groups.append({'model':path,'parent_member':member,'sid':block.attrib['SID'],'name':block.attrib['Name'],'member':child,
                           'signature':graph_signature(body),'parameters':parameters,'wrappers':wrappers})
    require(len(groups)==4,'Expected four reviewed monitoring subgraphs')
    same=all(g['signature']==groups[0]['signature'] for g in groups)
    wrappers=[w for g in groups for w in g['wrappers']]
    return {'schema':'reuse-subgraph-audit-v1','model_sha256':sha((repo/path).read_bytes()),'groups':groups,
            'group_topology_identical':same,'wrapper_topology_identical':all(w['signature']==wrappers[0]['signature'] for w in wrappers),
            'debouncer_link_count':sum(len(w['links']) for w in wrappers),
            'limits':'Topology equality is not itself a duplication verdict. Threshold direction, units, calibration, state independence and intentional safety separation must be reviewed before deciding whether a shared definition is appropriate.'}
