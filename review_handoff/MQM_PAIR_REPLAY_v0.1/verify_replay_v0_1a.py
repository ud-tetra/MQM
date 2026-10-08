#!/usr/bin/env python3
import hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
expected = json.loads((ROOT / "EXPECTED_RAW_AGGREGATES.json").read_text())
primary = json.loads(pathlib.Path(sys.argv[1]).read_text())
independent = json.loads(pathlib.Path(sys.argv[2]).read_text())

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

metrics=["Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN"]
fields=["f0","sp_num15","sq","sl","pp_num225","pq_num15","pl_num15","qq","ql","ll"]
mismatches=[]

for proto in ("1+0","2+1","3+1"):
    exp=expected["protocols"][proto]
    if primary["protocols"][proto]["locations"] != exp["locations"]:
        mismatches.append(["PRIMARY_LOCATION",proto])
    if primary["protocols"][proto]["raw_aggregates"] != exp["raw_aggregates"]:
        mismatches.append(["PRIMARY_RAW",proto])
    ir=independent["protocols"][proto]["raw"]
    for metric in metrics:
        src=ir[metric]
        norm={
            "f0":round(src["f0"]),
            "sp_num15":round(src["sp"]*15),
            "sq":round(src["sq"]),
            "sl":round(src["sl"]),
            "pp_num225":round(src["spp"]*225),
            "pq_num15":round(src["spq"]*15),
            "pl_num15":round(src["spl"]*15),
            "qq":round(src["sqq"]),
            "ql":round(src["sql"]),
            "ll":round(src["sll"]),
        }
        for field in fields:
            want=exp["raw_aggregates"][metric][field]
            if norm[field] != want:
                mismatches.append(["INDEPENDENT_RAW",proto,metric,field,norm[field],want])

receipt={
    "status":"PASS_EXTERNAL_RUNTIME_REPLAY" if not mismatches else "FAIL_EXTERNAL_RUNTIME_REPLAY",
    "scope":"GitHub-hosted external runtime reproduction of two same-agent implementations; not independent scientific review.",
    "package_sha256":{
      name:sha256(ROOT/name) for name in [
        "mqm_symbolic_malignant_pair_replay_v01.cpp",
        "mqm_full_stochastic_tail_v01.cpp",
        "mqm_pair_classifier_crosscheck_v01.cpp",
        "EXPECTED_RAW_AGGREGATES.json",
      ]
    },
    "primary_output_sha256":sha256(sys.argv[1]),
    "independent_output_sha256":sha256(sys.argv[2]),
    "protocols":["1+0","2+1","3+1"],
    "metrics":metrics,
    "raw_aggregate_mismatches":len(mismatches),
    "mismatches":mismatches,
}
pathlib.Path("EXTERNAL_REPLAY_RECEIPT_v0.1a.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
if mismatches:
    raise SystemExit(1)
