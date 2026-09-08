"""Cross-check safety/budget invariants independently of the reference equations."""
import json
import argparse
import math
import hashlib
import struct
from pathlib import Path
from matlab_validators import role_paths, read_json, require

ROOT=Path(__file__).resolve().parents[1]
SCRIPT_PATH=Path(__file__).resolve()
SCRIPT_SHA256_AT_IMPORT=hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest()

def evaluate(row,v,values):
    assert len(values)==len(v['inputs']),(row['id'],'output sample count',len(values),len(v['inputs']))
    count=0;previous={}
    domain=row['domain']
    for sample,(inputs,outputs) in enumerate(zip(v['inputs'],values)):
        u=dict(zip(v['input_names'],inputs));y=dict(zip(v['output_names'],outputs))
        assert len(outputs)==len(v['output_names']) and all(math.isfinite(x) for x in outputs),(row['id'],sample,'nonfinite/incomplete output')
        count+=1
        for name,value in y.items():
            if name.endswith(('Duty','ValveDemand','Command')):
                assert -1e-9<=value<=1+1e-9,(row['id'],sample,name,value)
                count+=1
        if domain in ('charge','energy'):
            assert 0<=y['CurrentLimitAmps']<=300+1e-9
            assert y['Allowed'] or y['CurrentLimitAmps']==0
            count+=2
            if u['EmergencyStop']:
                assert y['CurrentLimitAmps']==0
                count+=1
        if domain in ('battery','energy'):
            p='Bms' if domain=='energy' else ''
            assert 0<=y[p+'DischargeLimitKW']<=180+1e-9
            assert 0<=y[p+'ChargeLimitKW']<=120+1e-9
            if not y[p+'PackHealthy']:
                assert y[p+'DischargeLimitKW']==y[p+'ChargeLimitKW']==0
                count+=1
            count+=2
        if domain in ('traction','energy'):
            p='Drive' if domain=='energy' else ''
            torques=[y[p+w+'TorqueNm'] for w in ('FrontLeft','FrontRight','RearLeft','RearRight')]
            budget=min(max(u[p+'PowerBudgetKW'],0),250)
            if domain=='energy':budget=min(budget,y['TractionPowerAvailableKW'])
            cap=budget*310/max(abs(u[p+'RoadSpeedMps']),2)
            assert sum(max(x,0) for x in torques)<=cap+1e-7,(row['id'],sample,'power budget')
            if not u[p+'DriveEnabled']:
                assert all(x==0 for x in torques)
                count+=1
            assert abs(sum(torques)-y[p+'TotalTorqueNm'])<1e-8
            for wheel,torque in zip(('FrontLeft','FrontRight','RearLeft','RearRight'),torques):
                if torque>0:
                    assert torque-previous.get(p+wheel+'TorqueNm',0)<=15+1e-8,(row['id'],sample,'torque actual-state recovery')
                    count+=1
            count+=2
        if domain in ('cabin','thermal','energy'):
            p='Cabin' if domain=='energy' else ''
            budget=min(max(u[p+'AvailableElectricalW'],0),60000)
            heating=sum(value for name,value in y.items() if name.startswith(p) and name.endswith('HeaterW'))
            compressor=y[p+'CompressorDuty']
            assert -1e-8<=heating and abs(heating-y[p+'DeliveredHeatingW'])<1e-6,(row['id'],sample,'heating allocation sum')
            # Declared prototype mapping: duty=1 is 22000 W cooling at COP 2.8.
            assert heating+compressor*(22000/2.8)<=budget+1e-6,(row['id'],sample,'shared thermal hard budget')
            if budget==0:
                assert compressor==0,(row['id'],sample,'zero electrical budget')
                count+=1
            assert compressor-previous.get(p+'CompressorDuty',0)<=.015+1e-9,(row['id'],sample,'compressor actual-state recovery')
            if not u[p+'ClimateEnabled']:
                assert y[p+'DeliveredHeatingW']==0 and y[p+'CompressorDuty']==0
                count+=1
            count+=3
        if domain=='actuators':
            assert -1e-9<=y['AllocatedCurrentA']<=min(max(u['CurrentBudgetA'],0),150)+1e-8
            if u['Emergency'] or not u['ActuatorsEnabled']:
                assert all(value==0 for name,value in y.items() if name.endswith('Command'))
                count+=1
            count+=1
        if domain=='energy':
            if not y['BmsPackHealthy'] or abs(u['BmsStateOfCharge']-u['StateOfCharge'])>.03:
                assert y['CoordinatedChargeAmps']==0
                count+=1
            assert 0<=y['TractionPowerAvailableKW']<=y['BmsDischargeLimitKW']+1e-8
            # Same-sample aggregate: W of delivered heat and compressor input,
            # plus positive wheel mechanical kW using the declared 0.31 m radius.
            # Regen remains outside this positive allocation budget.
            thermal_kw=heating/1000+compressor*22/2.8
            positive_torque=sum(max(x,0) for x in torques)
            traction_kw=positive_torque*abs(u['DriveRoadSpeedMps'])/.31/1000
            assert thermal_kw+traction_kw<=y['BmsDischargeLimitKW']+1e-7,(row['id'],sample,'aggregate BMS discharge budget',thermal_kw,traction_kw,y['BmsDischargeLimitKW'])
            assert thermal_kw+y['TractionPowerAvailableKW']<=y['BmsDischargeLimitKW']+1e-7,(row['id'],sample,'same-sample traction reserve')
            count+=3
        previous=y
    result=dict(status='passed',samples=len(values),assertions=count,
                scope='Actual-output safety and resource invariants; no block graph, expected rows or reference evaluator used')
    return result

def check(row,run_root=None,output_kind='mil',write_result=True):
    ev=(Path(run_root) if run_root else ROOT/'evidence/nine')/row['id']
    script_before=hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest()
    assert script_before==SCRIPT_SHA256_AT_IMPORT,'Property script changed after this module was imported; reload before execution'
    bindings=[dict(role='property_script',path=str(SCRIPT_PATH),sha256=script_before)]
    def read_bound(path,role):
        path=path.resolve();data=path.read_bytes()
        bindings.append(dict(role=role,path=str(path),sha256=hashlib.sha256(data).hexdigest()))
        return data
    vectors=role_paths(read_json(ev/'acceptance/run-binding.json'),'vectors',Path(row['repository']))
    require(len(vectors)==1,'Acceptance must bind exactly one vector file')
    v=json.loads(read_bound(vectors[0],'vectors'))
    width=len(v['output_names']);streams={}
    for kind in ('mil','native') if output_kind=='both' else (output_kind,):
        path=ev/('acceptance/mil-output.bin' if kind=='mil' else 'native-replay/output.bin')
        values=list(struct.iter_unpack('<'+str(width)+'d',read_bound(path,kind+'_output')))
        streams[kind]=evaluate(row,v,values)
    for item in bindings:
        assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256'],('Input changed during property execution',item['path'])
    script_after=hashlib.sha256(SCRIPT_PATH.read_bytes()).hexdigest()
    assert script_before==script_after,'Property script changed during execution'
    result=dict(schema_version='1.1',model=row['model'],status='passed',samples=len(v['inputs']),assertions=sum(x['assertions'] for x in streams.values()),
                streams=streams,inputs=bindings,property_script_sha256_before=script_before,
                property_script_sha256_after=script_after,input_files_unchanged=True,
                scope='Independent actual-output resource contracts; hard dispatch and combined thermal budgets')
    if write_result:
        name='native-properties.json' if output_kind=='native' else 'properties.json'
        (ev/name).write_text(json.dumps(result,indent=2)+'\n')
    print(row['id'],result)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--run-root',type=Path,default=ROOT/'evidence/nine')
    parser.add_argument('--rows',type=Path,default=ROOT/'nine-candidates.json')
    parser.add_argument('--id',action='append')
    parser.add_argument('--output-kind',choices=['mil','native','both'],default='mil')
    parser.add_argument('--no-write',action='store_true')
    args=parser.parse_args()
    for row in json.loads(args.rows.read_text()):
        if not args.id or row['id'] in args.id:check(row,args.run_root,args.output_kind,not args.no_write)
