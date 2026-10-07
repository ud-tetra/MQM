from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import mqm_core_x_fault_simulator_v0_1 as sim

INVALID={(1,1,0),(1,0,1),(0,1,1)}

@dataclass(frozen=True)
class RecoveryResult:
    status:str
    data:tuple
    rounds:int
    correction_attempts:int
    trace:tuple
    reason:str

def toggle(data,q1):
    d=list(data); d[q1-1]^=1; return tuple(d)

def run_recovery(
    initial=(0,0,0,0),
    *,
    extraction_fault_round:Optional[int]=None,
    extraction_fault:Optional[sim.XFault]=None,
    correction_fault_attempt:Optional[int]=None,
    max_rounds:int=16,
):
    data=tuple(initial)
    previous=None
    trace=[]
    correction_attempts=0

    for round_index in range(max_rounds):
        fault=extraction_fault if extraction_fault_round==round_index else None
        data,syndrome=sim.round_once(data,fault)
        trace.append({
            "round":round_index,
            "data_after_round":data,
            "syndrome":syndrome,
            "fault":None if fault is None else fault.__dict__,
        })

        if previous!=syndrome:
            previous=syndrome
            continue

        if syndrome in INVALID:
            return RecoveryResult(
                "ESCALATE_OUTSIDE_CORE_X",data,round_index+1,
                correction_attempts,tuple(trace),
                "STABLE_UNDECLARED_WEIGHT2_SYNDROME"
            )

        if syndrome not in sim.VALID:
            previous=None
            continue

        correction=sim.VALID[syndrome]
        if correction is None:
            # Important: because an X fault can arise after its final sampled
            # interaction in the confirming round, this certifies only the
            # <=1-X correctable envelope under the declared one-fault model.
            return RecoveryResult(
                "CERTIFIED_CORE_X1_BOUNDARY",data,round_index+1,
                correction_attempts,tuple(trace),
                "TWO_CONSECUTIVE_ZERO_SYNDROME_OBSERVATIONS"
            )

        correction_attempts+=1
        data=toggle(data,correction)
        if correction_fault_attempt==correction_attempts:
            # Local correction X fault after intended X: net cancellation.
            data=toggle(data,correction)
            trace.append({
                "correction_attempt":correction_attempts,
                "commanded_X":correction,
                "local_X_fault_after_correction":True,
                "data_after_correction":data,
            })
        else:
            trace.append({
                "correction_attempt":correction_attempts,
                "commanded_X":correction,
                "local_X_fault_after_correction":False,
                "data_after_correction":data,
            })
        previous=None

    return RecoveryResult(
        "NO_CONSENSUS_TIMEOUT",data,max_rounds,correction_attempts,
        tuple(trace),"RESOURCE_CAP_REACHED"
    )

def five_repetition_syndrome(error_vertices):
    E=set(error_vertices)
    return tuple(1 if ((1 in E) ^ (j in E)) else 0 for j in (2,3,4,5))
