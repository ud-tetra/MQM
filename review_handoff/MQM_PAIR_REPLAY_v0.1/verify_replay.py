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

EXPECTED_HASHES = {
    "mqm_symbolic_malignant_pair_replay_v01.cpp":"e146dcce1a0f084f9b31e574c633aef23bad0ef2c434cb3cdcec10739f4ef241",
    "mqm_full_stochastic_tail_v01.cpp":"fbae1385dc18c555eaa985d38a57b2cd74a5b6b7b736066eb1f5b174558d1b91",
    "mqm_pair_classifier_crosscheck_v01.cpp":"f3f1f9b8d64757f96f571e911e2e3f71af3465bfd3dbcad77f73f5eb30214858",
}
hashes={}
for name,want in EXPECTED_HASHES.items():
    got=sha256(ROOT/name); hashes[name]=got
    if got != want:
        raise SystemExit(f"HASH_MISMATCH {name}: {got} != {want}")

metrics=["Y","HOLD","QUARANTINE","L_AND_ACCEPT","ACCEPT_DW1","Y_CLEAN"]
fields=["f0","sp_num15","sq","sl","pp_num225","pq_num15","pl_num15","qq","ql","ll"]

for proto in ("1+0","2+1","3+1"):
    exp=expected["protocols"][proto]
    if primary["protocols"][proto]["locations"] != exp["locations"]:
        raise SystemExit(f"PRIMARY_LOCATION_MISMATCH {proto}")
    if primary["protocols"][proto]["raw_aggregates"] != exp["raw_aggregates"]:
        raise SystemExit(f"PRIMARY_RAW_MISMATCH {proto}")
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
                raise SystemExit(
                    f"INDEPENDENT_RAW_MISMATCH {proto} {metric} {field}: "
                    f"{norm[field]} != {want}"
                )

receipt={
    "status":"PASS_EXTERNAL_RUNTIME_REPLAY",
    "scope":"External CI runtime reproduction of two same-agent implementations; not independent scientific review.",
    "source_hashes":hashes,
    "primary_output_sha256":sha256(sys.argv[1]),
    "independent_output_sha256":sha256(sys.argv[2]),
    "protocols":["1+0","2+1","3+1"],
    "metrics":metrics,
    "raw_aggregate_mismatches":0,
}
pathlib.Path("EXTERNAL_REPLAY_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
