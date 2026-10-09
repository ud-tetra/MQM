#!/usr/bin/env python3
import json, math
slots=list(range(5)); chans=list(range(4))
short={1,4}; long={2,3}

# First five epochs.
base=[]
for t in range(5):
    row={"epoch":t,"spare":t,"assign":{}}
    for j in chans: row["assign"][j]=(t+j+1)%5
    assert sorted(row["assign"].values())==[s for s in slots if s!=t]
    base.append(row)

slot_spare=[0]*5; slot_active=[0]*5; slot_checks=[0]*5
channel_slot=[[0]*5 for _ in chans]
channel_short=[0]*4;channel_long=[0]*4
for row in base:
    slot_spare[row["spare"]]+=1;slot_checks[row["spare"]]+=1
    for c,s in row["assign"].items():
        slot_active[s]+=1;slot_checks[s]+=1;channel_slot[c][s]+=1
        sep=(s-row["spare"])%5
        if sep in short: channel_short[c]+=1
        else: channel_long[c]+=1
assert slot_spare==[1]*5 and slot_active==[4]*5 and slot_checks==[5]*5
assert all(x==[1]*5 for x in channel_slot)

# Ten-epoch supercycle: second five-cycle permutes channel offsets to balance short/long burden.
offset_sets=[[1,2,3,4],[2,1,4,3]]
supercycle=[]
for cyc,offs in enumerate(offset_sets):
    for t in range(5):
        e=cyc*5+t
        row={"epoch":e,"spare":t,"assign":{}}
        for c,off in enumerate(offs): row["assign"][c]=(t+off)%5
        assert sorted(row["assign"].values())==[s for s in slots if s!=t]
        supercycle.append(row)

ss=[0]*5;sa=[0]*5;sc=[0]*5
cs=[[0]*5 for _ in chans]; cshort=[0]*4;clong=[0]*4
for row in supercycle:
    ss[row["spare"]]+=1;sc[row["spare"]]+=1
    for c,s in row["assign"].items():
        sa[s]+=1;sc[s]+=1;cs[c][s]+=1
        sep=(s-row["spare"])%5
        if sep in short:cshort[c]+=1
        else:clong[c]+=1
assert ss==[2]*5 and sa==[8]*5 and sc==[10]*5
assert all(x==[2]*5 for x in cs)
assert cshort==[5]*4 and clong==[5]*4

mean_dist=(5*2+5*(1+math.sqrt(5)))/10
out={
 "version":"0.1",
 "status":"EXACT_D5_ROTATING_SPARE_SCHEDULE",
 "physical_promotion":0,
 "five_epoch_base":{
   "schedule":base,
   "slot_spare_counts":slot_spare,
   "slot_active_counts":slot_active,
   "slot_total_check_counts":slot_checks,
   "channel_slot_visit_matrix":channel_slot,
   "channel_short_counts":channel_short,
   "channel_long_counts":channel_long,
   "finding":"physical-slot spare/active/check burden and channel visits are exactly equalized over five epochs; replacement-distance burden is not yet equal across channel labels"
 },
 "ten_epoch_balanced_supercycle":{
   "schedule":supercycle,
   "slot_spare_counts":ss,
   "slot_active_counts":sa,
   "slot_total_check_counts":sc,
   "channel_slot_visit_matrix":cs,
   "channel_short_counts":cshort,
   "channel_long_counts":clong,
   "mean_replacement_distance_per_channel_exact":"(3+sqrt(5))/2",
   "mean_replacement_distance_per_channel":mean_dist,
   "finding":"both physical-slot exposure and logical-channel replacement-distance exposure are exactly equalized"
 },
 "homogeneous_iid_loss":{
   "invariance":"per-epoch outcome probabilities are unchanged by rotation because every epoch still has exactly four active slots and one spare with identical iid channel parameters",
   "benefit_scope":"rotation can only improve reliability if site-dependent drift/loss/crosstalk exists; that channel is OPEN"
 },
 "scope":"deterministic burden equalization schedule; not a hardware reliability result"
}
print(json.dumps(out,indent=2,sort_keys=True))
