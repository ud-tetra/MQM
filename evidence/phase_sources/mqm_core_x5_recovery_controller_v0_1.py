from __future__ import annotations

"""
MQM Core-X5 stable-syndrome controller v0.1.

Scoped property tested:
- input X weight <= 1;
- at most one X-type extraction/correction fault in recovery interval;
- no general Pauli fault.

Boundary means output X weight <= 1 under that provenance envelope.
"""

from dataclasses import dataclass
from typing import Optional
import mqm_core_x5_fault_simulator_v0_1 as sim

@dataclass(frozen=True)
class RecoveryResult:
    status:str
    data:tuple
    rounds:int
    correction_attempts:int
    correction_X_count:int
    trace:tuple
    reason:str

def run_recovery(
    initial=(0,0,0,0,0),
    *,
    extraction_fault_round:Optional[int]=None,
    extraction_fault:Optional[sim.XFault]=None,
    correction_fault_attempt:Optional[int]=None,
    correction_fault_subindex:int=0,
    max_rounds:int=20,
):
    data=tuple(initial)
    previous=None
    trace=[]
    attempts=0
    correction_x_count=0

    for round_index in range(max_rounds):
        fault=extraction_fault if extraction_fault_round==round_index else None
        data,s=sim.round_once(data,fault)
        trace.append({
            "round":round_index,
            "data_after_round":data,
            "syndrome":s,
            "fault":None if fault is None else fault.__dict__,
        })

        if previous!=s:
            previous=s
            continue

        correction=sim.syndrome_to_correction(s)
        if correction=="INVALID":
            previous=None
            continue

        if correction==():
            return RecoveryResult(
                "CERTIFIED_CORE_X5_XFT1_BOUNDARY",
                data,round_index+1,attempts,correction_x_count,
                tuple(trace),
                "TWO_CONSECUTIVE_ZERO_SYNDROME_OBSERVATIONS"
            )

        attempts+=1
        d=list(data)
        for subindex,q in enumerate(correction):
            d[q]^=1
            correction_x_count+=1
            if correction_fault_attempt==attempts and subindex==correction_fault_subindex:
                # One local X fault after the addressed X correction cancels
                # this sub-operation.
                d[q]^=1
                trace.append({
                    "correction_attempt":attempts,
                    "subindex":subindex,
                    "qubit":q,
                    "local_X_fault_after_correction":True,
                })
        data=tuple(d)
        previous=None

    return RecoveryResult(
        "NO_CONSENSUS_TIMEOUT",data,max_rounds,attempts,
        correction_x_count,tuple(trace),"RESOURCE_CAP_REACHED"
    )
