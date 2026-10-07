"""MQM 0.5: Stim round adapter for the supplied X-only controller.
Run from the extracted release: python artifacts/x5_envelope.py
Optional --write writes deterministic case records and expected output.
No random noise, hardware shots, phase protection, or memory threshold claim.
"""
import json
import sys
from pathlib import Path
from itertools import combinations, product
from collections import Counter
import stim
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'support'))
import x5_model as model
import x5_controller as controller


def round_circuit(data=(0,)*5, fault=None):
    c = stim.Circuit('R 0 1 2 3 4 5 6 7 8')
    for q,b in enumerate(data):
        if b: c.append('X', [q])
    if fault and fault.kind=='ANCILLA_X' and fault.layer==-1:
        c.append('X', [5+fault.target])
    for li,layer in enumerate(model.LAYERS):
        for oi,(q,a) in enumerate(layer):
            c.append('CX',[q,5+a])
            if fault and fault.layer==li and fault.op_index==oi:
                if fault.kind in {'DATA_X','CNOT_X_DATA','CNOT_X_BOTH'}: c.append('X',[q])
                if fault.kind in {'CNOT_X_ANC','CNOT_X_BOTH','ANCILLA_X'}: c.append('X',[5+a])
        c.append('TICK')
    if fault and fault.kind=='MEAS_FLIP': c.append('X',[5+fault.target])
    c.append('M',[5,6,7,8])
    return c


def stim_round(data=(0,)*5, fault=None):
    sim = stim.TableauSimulator()
    sim.do_circuit(round_circuit(data,fault))
    z = [sim.peek_z(q) for q in range(5)]
    assert all(v in (-1,1) for v in z)
    # peek_z is simulator introspection, never an experimental observation.
    return tuple(int(v==-1) for v in z), tuple(map(int,sim.current_measurement_record()))


def run(write=False):
    original=model.round_once
    faults=model.all_single_x_faults()
    round_cases=0
    # Compare the translated circuit with all 32 binary frames and 40 fault labels.
    for data in product((0,1),repeat=5):
        for fault in (None,)+faults:
            assert stim_round(data,fault)==original(data,fault)
            round_cases+=1
    cases=[]; failure_witnesses=[]; clean=[]
    try:
        model.round_once=stim_round
        for q in range(5):
            data=tuple(int(i==q) for i in range(5))
            for fault_round in range(4):
                for label,fault in enumerate(faults):
                    r=controller.run_recovery(data,extraction_fault_round=fault_round,extraction_fault=fault)
                    assert r.status=='CERTIFIED_CORE_X5_XFT1_BOUNDARY' and sum(r.data)<=1
                    cases.append({'input_X':q,'scheduled_fault_round':fault_round,'fault_label':label,'fault':fault.__dict__,
                      'fault_executed_before_release':any(x.get('fault') is not None for x in r.trace),
                      'rounds':r.rounds,'residual':list(r.data),'residual_weight':sum(r.data),'status':'released_weight_le_1'})
        for w in range(3):
            for qs in combinations(range(5),w):
                data=tuple(int(q in qs) for q in range(5));r=controller.run_recovery(data)
                assert r.data==(0,)*5
                clean.append({'input':list(data),'residual':list(r.data)})
        for pair in combinations(range(5),2):
            for q in sorted(set(range(5))-set(pair)):
                data=tuple(int(i in pair or i==q) for i in range(5));r=controller.run_recovery(data)
                assert r.data==(1,)*5
                failure_witnesses.append({'weight2_input':list(pair),'additional_X':q,'residual':list(r.data)})
    finally:
        model.round_once=original
    residuals=dict(sorted(Counter(str(c['residual_weight']) for c in cases).items()))
    assert len(cases)==800 and residuals=={'0':750,'1':50}
    assert len(clean)==16 and len(failure_witnesses)==30
    result={'release':'0.5','stim_version':stim.__version__,'round_translation_cases':round_cases,
      'fault_free_patterns':len(clean),'labeled_incoming_cases':len(cases),'residual_weight_counts':residuals,
      'weight2_plus_extra_X_failures':len(failure_witnesses),'fault_labels':len(faults),
      'scheduled_faults_not_executed_before_release':sum(not c['fault_executed_before_release'] for c in cases),
      'scope':'Deterministic X-only Pauli-frame conformance; ideal operations except named injections. No stochastic idle model, phase protection, hardware execution, or independent replication.'}
    if write:
        (ROOT/'expected/x5_envelope.json').write_text(json.dumps(result,indent=2)+'\n')
        (ROOT/'expected/x5_cases.json').write_text(json.dumps({'cases':cases,'fault_free':clean,'logical_failure_witnesses':failure_witnesses},indent=2)+'\n')
        (ROOT/'circuits/x5_round.stim').write_text('# One ideal extraction round; data initialized to logical zero. Not a memory experiment.\n'+str(round_circuit())+'\n')
    return result

if __name__=='__main__': print(json.dumps(run('--write' in sys.argv),indent=2))
