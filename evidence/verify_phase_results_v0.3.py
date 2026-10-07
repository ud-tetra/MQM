"""Replay selected supplied MQM models. No hardware execution or claim promotion.

Source modules are byte-identical copies identified in SOURCE_PROVENANCE.json.
Only this driver is new. Phase 48's 40 fault labels include duplicated effects;
the results count labeled cases, not independent physical fault mechanisms.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations, product
import sys
import json
import math

sys.path.insert(0, str(Path(__file__).parent / 'phase_sources'))
import mqm_core_x_fault_simulator_v0_1 as s4
import mqm_core_x_fail_closed_controller_v0_1 as c4
import mqm_core_x5_fault_simulator_v0_1 as s5
import mqm_core_x5_recovery_controller_v0_1 as c5
import mqm_core_x5_pauli_hook_audit_v0_1 as ph
import mqm_core_x5_central_extension_v0_1 as x5
import mqm_x5_neutral_atom_dynamic_3d_motion_v0_1 as motion

def sweep(n, sim, controller, inputs, rounds):
    counts, residuals = Counter(), Counter()
    max_rounds = 0
    for data in inputs:
        for fault_round in rounds:
            for fault in sim.all_single_x_faults():
                result = controller.run_recovery(data, extraction_fault_round=fault_round, extraction_fault=fault)
                counts[result.status] += 1
                residuals[result.status + ':weight=' + str(sum(result.data))] += 1
                if result.status.startswith('CERTIFIED'):
                    assert sum(result.data) <= 1
                max_rounds = max(max_rounds, result.rounds)
    return {'cases':sum(counts.values()),'outcomes':dict(counts),'residuals':dict(residuals),'max_rounds':max_rounds}

def one_errors(n):
    return [tuple(int(i == q) for i in range(n)) for q in range(n)]

def verify():
    four_clean = sweep(4, s4, c4, [(0,)*4], range(2))
    four_input = sweep(4, s4, c4, one_errors(4), range(4))
    assert four_clean['cases'] == 60
    assert four_input['outcomes'] == {'CERTIFIED_CORE_X1_BOUNDARY':396, 'ESCALATE_OUTSIDE_CORE_X':84}
    five_clean = sweep(5, s5, c5, [(0,)*5], range(2))
    five_input = sweep(5, s5, c5, one_errors(5), range(4))
    assert five_clean['cases'] == 80 and five_input['cases'] == 800
    assert five_input['outcomes'] == {'CERTIFIED_CORE_X5_XFT1_BOUNDARY':800}
    assert five_input['residuals']['CERTIFIED_CORE_X5_XFT1_BOUNDARY:weight=1'] == 50
    words, syndromes = [], set()
    for w in range(3):
        for qs in combinations(range(5), w):
            d = tuple(int(i in qs) for i in range(5))
            r = c5.run_recovery(d)
            assert r.data == (0,)*5
            syn = tuple(d[0] ^ d[i] for i in range(1,5))
            assert syn not in syndromes
            syndromes.add(syn)
            words.append(d)
    assert len(words) == 16 and len(x5.vertex_face_matchings()) == 9
    correction_faults = []
    for d in one_errors(5):
        r = c5.run_recovery(d, correction_fault_attempt=1)
        assert r.data == (0,)*5
        correction_faults.append({'rounds':r.rounds,'residual_weight':sum(r.data)})
    no_go_count = 0
    for pair in combinations(range(5),2):
        for new in set(range(5)) - set(pair):
            data = tuple(int(i in pair or i == new) for i in range(5))
            r = c5.run_recovery(data)
            assert r.data == (1,)*5
            no_go_count += 1
    assert no_go_count == 30
    hooks = ph.enumerate_faults()
    hook_result = {'fault_cases':len(hooks),'data_weight_ge2':sum(r['data_weight']>=2 for r in hooks),
                   'phase_bearing':sum(r['data_Z_or_Y_weight']>0 for r in hooks)}
    assert hook_result == {'fault_cases':120,'data_weight_ge2':24,'phase_bearing':80}
    # 4-bit Z parity is safe on both repetition codewords iff its support is even.
    static_even = [v for v in product((0,1),repeat=4) if sum(v)%2 == 0]
    assert len(static_even) == 8
    # Check the supplied motion formulas on a declared sample grid, not hardware.
    checks = 0
    for delta in (.05,.1,.2,.3):
        for lam in (.1,.25,.5,.75):
            for vertex in range(1,5):
                m = motion.gate_pose_metrics(vertex,delta,lam)
                assert math.isclose(m['gate_center_distance'],m['gate_vertex_distance'],abs_tol=1e-12)
                assert math.isclose(m['shuttle_distance'],lam,abs_tol=1e-12)
                checks += 1
    a,b = motion.alternating_schedule_pair()
    oa,ob = motion.partner_order(a),motion.partner_order(b)
    assert all(oa[k][-1] == ob[k][0] and ob[k][-1] == oa[k][0] for k in oa)
    return {'physical_promotion':0,'measurement_ready':False,'phase46_clean':four_clean,
            'phase46_incoming_X':four_input,'phase48_clean':five_clean,'phase48_incoming_X':five_input,
            'X5_fault_free_patterns':len(words),'X5_face_matchings':9,'X5_correction_fault_cases':correction_faults,
            'X5_weight2_plus_new_X_logical_failure_witnesses':no_go_count,'X5_general_Pauli_hook_audit':hook_result,
            'safe_static_four_data_Z_parities':len(static_even),'phase52_motion_samples':checks,
            'alternating_partner_orders_no_extra_return':True,
            'scope':'Same-session finite-model replay; no independent replication, blind hardware test, or full Pauli fault-tolerance claim.'}

if __name__ == '__main__':
    print(json.dumps(verify(),indent=2))
