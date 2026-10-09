#!/usr/bin/env python3
import json, math
Cv=0.9570935821134408
rows=[]
for P in range(1,9):
    bv=math.ceil(4/P)
    bd=math.ceil(7/P)
    den=6*bd-4*bv
    rows.append({
      "parallel_capacity":P,
      "v128_batches_per_step":bv,
      "D6_batches_per_step":bd,
      "equal_batch_duration_break_even_us":None if den<=0 else 12.2/den
    })
out={
 "version":"0.1",
 "status":"EXACT_MOVE_DECISION_THRESHOLD_TABLE",
 "physical_promotion":0,
 "equal_batch_parallelism_table":rows,
 "equal_loss_break_even":1-Cv**(1/26),
 "equal_loss_break_even_percent":100*(1-Cv**(1/26)),
 "candidate_specific_time":"v128 faster iff 12.2 + 4*tau_v < 6*tau_D6",
 "candidate_specific_loss":"v128 preferred iff 0.9570935821134408*(1-ell_v)^16 > (1-ell_D6)^42",
 "ideal_Magnus":"D6 lower for eta<3.7227278096555585; v128 lower for eta>3.7227278096555585",
 "required_MOVE_record_fields":[
   "candidate_id","step_id","moved_role_ids","start_xyz_um","end_xyz_um",
   "route_length_um","duration_ns","parallel_group","parallel_move_count",
   "retained_state_channel","phase_shift_rad","dephasing_or_contrast","atom_loss",
   "heating_or_recapture","spectator_error","route_interaction_error",
   "loss_false_negative","loss_false_positive","raw_trials","uncertainty",
   "operating_point_id","backend_id","calibration_start_utc","calibration_end_utc"
 ],
 "public_source_closure":"OPEN",
 "scope":"decision/calibration contract, not hardware result"
}
print(json.dumps(out,indent=2,sort_keys=True))
