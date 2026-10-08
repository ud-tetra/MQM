#!/usr/bin/env python3
import json, math

DATA=list(range(1,9)); SYN=9; FLAG=10; LIVE=set(range(1,11))
CHECKS=[
 ("B1","IIIXXZZI",[4,5,6,7]),
 ("B2","IIIZZYYI",[4,5,6,7]),
 ("B3","IIIYIYZZ",[4,6,7,8]),
 ("B4","XXXXYYIX",[4,5,6,1,2,3,8]),
]
EDGES=[("E12",(1,2)),("E13",(1,3)),("E18",(1,8)),("E23",(2,3)),("E28",(2,8)),("E38",(3,8))]

def sel_ry(target,theta):
    target=sorted(target); spectator=sorted(LIVE-set(target))
    # Chronological sequence. For every spectator:
    # Rz(-pi) GR_y(theta/2) Rz(pi) GR_y(theta/2) = I
    # after right-to-left operator ordering; targets receive Ry(theta).
    return [
      {"gate":"GR","theta":theta/2,"phi":math.pi/2,"scope":"all_live"},
      {"gate":"RZ","theta":math.pi,"qubits":spectator,"role":"spectator_echo"},
      {"gate":"GR","theta":theta/2,"phi":math.pi/2,"scope":"all_live"},
      {"gate":"RZ","theta":-math.pi,"qubits":spectator,"role":"spectator_echo_inverse"},
    ]

def center(name,p,order):
    X=[i+1 for i,c in enumerate(p) if c=="X"]
    Y=[i+1 for i,c in enumerate(p) if c=="Y"]
    T=sorted(set(X+Y+[SYN,FLAG]))
    S=sorted(LIVE-set(T))
    ordinary=sorted(set(X+[SYN,FLAG]))
    ops=[
      {"gate":"RESET","qubits":[SYN,FLAG],"states":["0","0"]},
      {"gate":"RZ","qubits":ordinary,"theta":math.pi,"role":"pre_H_phase"},
      {"gate":"RZ","qubits":Y,"theta":math.pi/2,"role":"pre_Y_phase"},
      *sel_ry(T,math.pi/2),
    ]
    cz=[]
    for k,d in enumerate(order,1):
        cz.append({"gate":"CZ","qubits":[d,SYN],"role":"data_syndrome","data_interaction_index":k})
        if k in (1,3):
            cz.append({"gate":"CZ","qubits":[FLAG,SYN],"role":"flag_syndrome","after_data_interaction":k})
    ops += cz
    ops += sel_ry(T,-math.pi/2)
    ops += [
      {"gate":"RZ","qubits":ordinary,"theta":math.pi,"role":"post_H_phase"},
      {"gate":"RZ","qubits":Y,"theta":-math.pi/2,"role":"post_Y_phase"},
      {"gate":"NDSSR_Z","qubits":[SYN,FLAG],"logical_bases":["Z","X_after_compiled_H"]},
    ]
    return {
      "name":name,"pauli":p,"data_order":order,"X_data":X,"Y_data":Y,
      "selective_H_target":T,"spectators":S,"ops":ops
    }

def edge(name,e):
    T=[SYN]; S=sorted(LIVE-set(T))
    ops=[
      {"gate":"RESET","qubits":[SYN],"states":["0"]},
      {"gate":"RZ","qubits":[SYN],"theta":math.pi,"role":"pre_H_phase"},
      *sel_ry(T,math.pi/2),
      {"gate":"CZ","qubits":[e[0],SYN],"role":"edge_parity"},
      {"gate":"CZ","qubits":[e[1],SYN],"role":"edge_parity"},
      *sel_ry(T,-math.pi/2),
      {"gate":"RZ","qubits":[SYN],"theta":math.pi,"role":"post_H_phase"},
      {"gate":"NDSSR_Z","qubits":[SYN],"logical_bases":["Z"]},
    ]
    return {"name":name,"edge":list(e),"selective_H_target":T,"spectators":S,"ops":ops}

checks=[center(*x) for x in CHECKS]+[edge(*x) for x in EDGES]

def count_requests(c):
    out={"GR":0,"CZ":0,"RZ_address_requests":0,"RZ_time_slices":0,"RESET_site_requests":0,"NDSSR_site_requests":0}
    for op in c["ops"]:
        g=op["gate"]
        if g=="GR": out["GR"]+=1
        elif g=="CZ": out["CZ"]+=1
        elif g=="RZ":
            n=len(op.get("qubits",[]))
            if n:
                out["RZ_address_requests"]+=n
                out["RZ_time_slices"]+=1
        elif g=="RESET": out["RESET_site_requests"]+=len(op["qubits"])
        elif g=="NDSSR_Z": out["NDSSR_site_requests"]+=len(op["qubits"])
    return out

per={c["name"]:count_requests(c) for c in checks}
tot={k:sum(x[k] for x in per.values()) for k in next(iter(per.values()))}
assert tot=={
 "GR":40,"CZ":39,"RZ_address_requests":346,"RZ_time_slices":60,
 "RESET_site_requests":14,"NDSSR_site_requests":14
},tot

obj={
 "version":"0.1",
 "status":"EXACT_NATIVE_GATE_ALGEBRA_COMPILE__ROUTING_TIMING_OPEN",
 "active_register":{"data":[1,2,3,4,5,6,7,8],"syndrome":9,"flag":10,"live_qubits":10},
 "assumptions":[
  "Only these 10 live qubits require compensation under GR, or all external live spectators are independently compiler-decoupled.",
  "Every requested CZ pair is made connected by a separate routing/motion layer; route, duration, and transport noise are not synthesized here.",
  "Local RZ requests are exact site-address requests. RZ_time_slices assume arbitrary same-time parallel local addressing only as a layer-count diagnostic; hardware concurrency is not asserted.",
  "RESET and NDSSR are typed macros pending a source-complete mid-circuit reset/timing contract."
 ],
 "native_primitives":["GR(theta,phi)","RZ_i(theta)","CZ_ij","RESET_i","NDSSR_Z_i"],
 "identities":{
  "selective_Ry_T_theta":"GR_y(theta/2); RZ_spectators(pi); GR_y(theta/2); RZ_spectators(-pi) => Ry_T(theta) tensor I_spectators",
  "H_pre_ordinary":"RZ(pi) then Ry(pi/2) = -i H",
  "Y_pre":"RZ(pi/2) then Ry(pi/2) = -i H Sdag",
  "H_post":"Ry(-pi/2) then RZ(pi) = -i H",
  "Y_post":"Ry(-pi/2) then RZ(-pi/2) = S H",
  "parity_chain":"product CNOT(control->syndrome) = H_syndrome [product CZ(control,syndrome)] H_syndrome"
 },
 "checks":checks,
 "counts_per_check":per,
 "round_totals":tot,
 "routing_requirements":{
  "CZ_requests":39,
  "interaction_graph":"star-like syndrome-to-data/flag requests preserving the frozen check order",
  "status":"OPEN_PHYSICAL_ROUTE",
  "reason":"Public Sqale sources establish dynamic all-to-all connectivity/atom motion but do not provide a source-bound move sequence, concurrency contract, or timing for this MQM job."
 },
 "physical_promotion":0
}
print(json.dumps(obj,indent=2))
