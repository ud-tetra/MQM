#!/usr/bin/env python3
"""Exact GF(2) replay for the MQM subsystem-8 gauge-core noise-alignment audit.

Sources:
  - release/branches.json (subsystem-8 stabilizers, gauge generators, logicals,
    ideal-center decoder lookup)
  - locked native-3D geometry mapping:
      T_C   = {1,2,3,8}
      T_plus= {5,6,7,8}
      T_minus={4,6,7,8}
    Physical labels are 1-based; release Pauli strings are 0-based positions.

No floating point is used. Pauli phases are quotiented, matching release scope.
"""

from __future__ import annotations
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRANCHES = ROOT / "release" / "branches.json"

PHYS = {
    "T_C": (1, 2, 3, 8),
    "T_plus": (5, 6, 7, 8),
    "T_minus": (4, 6, 7, 8),
}
CODE = {k: tuple(i - 1 for i in v) for k, v in PHYS.items()}

def pv(s: str) -> int:
    n = len(s)
    x = z = 0
    for i, ch in enumerate(s):
        if ch in "XY":
            x |= 1 << i
        if ch in "ZY":
            z |= 1 << i
    return x | (z << n)

def split(v: int, n: int) -> tuple[int, int]:
    mask = (1 << n) - 1
    return v & mask, (v >> n) & mask

def parity(x: int) -> int:
    return x.bit_count() & 1

def symp(a: int, b: int, n: int) -> int:
    ax, az = split(a, n)
    bx, bz = split(b, n)
    return parity((ax & bz)) ^ parity((az & bx))

def syndrome(v: int, stabs: list[int], n: int) -> tuple[int, ...]:
    return tuple(symp(v, s, n) for s in stabs)

def span_set(basis: list[int]) -> set[int]:
    out = {0}
    for b in basis:
        out |= {x ^ b for x in tuple(out)}
    return out

def logical_class(v: int, gauge_span: set[int], lx: int, lz: int) -> str:
    tests = (
        ("I", 0),
        ("X", lx),
        ("Z", lz),
        ("Y", lx ^ lz),
    )
    for name, l in tests:
        if v ^ l in gauge_span:
            return name
    raise AssertionError("residual not in logical normalizer quotient")

def supported_pauli(chars: tuple[str, ...], support: tuple[int, ...], n: int) -> int:
    s = ["I"] * n
    for i, ch in zip(support, chars):
        s[i] = ch
    return pv("".join(s))

def full_support_counts(
    support: tuple[int, ...],
    n: int,
    stabs: list[int],
    decoder: dict[tuple[int, ...], int],
    gauge_span: set[int],
    lx: int,
    lz: int,
) -> Counter:
    c = Counter()
    for chars in itertools.product("IXYZ", repeat=len(support)):
        e = supported_pauli(chars, support, n)
        s = syndrome(e, stabs, n)
        r = e ^ decoder[s]
        c[logical_class(r, gauge_span, lx, lz)] += 1
    return c

def pair_counts(
    pair_kind: str,
    n: int,
    core: set[int],
    stabs: list[int],
    decoder: dict[tuple[int, ...], int],
    gauge_span: set[int],
    lx: int,
    lz: int,
) -> dict[str, Counter]:
    out = {"GG": Counter(), "GS": Counter(), "SS": Counter()}
    paulis = ("XYZ", "XYZ") if pair_kind == "all" else (("X", "Y"), ("X", "Y"))
    for i, j in itertools.combinations(range(n), 2):
        loc = "GG" if i in core and j in core else "SS" if i not in core and j not in core else "GS"
        for a in paulis[0]:
            for b in paulis[1]:
                s = ["I"] * n
                s[i], s[j] = a, b
                e = pv("".join(s))
                syn = syndrome(e, stabs, n)
                r = e ^ decoder[syn]
                out[loc][logical_class(r, gauge_span, lx, lz)] += 1
    return out

def main() -> None:
    branches = json.loads(BRANCHES.read_text())
    branch = next(b for b in branches if b["id"] == "subsystem-8")
    n = branch["n_data"]

    stabs = [pv(s) for s in branch["generators"]["center"]]
    gauges = [pv(s) for s in branch["generators"]["gauge"]]
    lx = pv(branch["logicals"]["X"])
    lz = pv(branch["logicals"]["Z"])
    decoder = {tuple(map(int, k)): pv(v) for k, v in branch["decoder"]["lookup"].items()}
    gauge_span = span_set(gauges)

    # Decoder self-consistency.
    for syn, corr in decoder.items():
        assert syndrome(corr, stabs, n) == syn

    core = set(CODE["T_C"])

    # Direct 256-pattern core replay.
    core_counts = full_support_counts(CODE["T_C"], n, stabs, decoder, gauge_span, lx, lz)
    assert core_counts == Counter({"I": 256})

    # Exact syndrome/coset distribution.
    core_syn = Counter()
    for chars in itertools.product("IXYZ", repeat=4):
        e = supported_pauli(chars, CODE["T_C"], n)
        core_syn["".join(map(str, syndrome(e, stabs, n)))] += 1
    assert core_syn == Counter({"0000": 64, "0001": 64, "0110": 64, "0111": 64})

    # Uniqueness over all C(8,4)=70 four-site subsets.
    subset_counts = {}
    fully_benign = []
    for support in itertools.combinations(range(n), 4):
        c = full_support_counts(support, n, stabs, decoder, gauge_span, lx, lz)
        subset_counts["".join(str(i + 1) for i in support)] = dict(c)
        if c == Counter({"I": 256}):
            fully_benign.append(tuple(i + 1 for i in support))
    assert fully_benign == [PHYS["T_C"]]

    # Named tetrahedra.
    named = {
        name: dict(full_support_counts(sup, n, stabs, decoder, gauge_span, lx, lz))
        for name, sup in CODE.items()
    }
    assert named["T_plus"] == {"I": 64, "X": 64, "Y": 64, "Z": 64}
    assert named["T_minus"] == {"I": 64, "X": 64, "Y": 64, "Z": 64}

    # Pair classifications.
    all_pairs = pair_counts("all", n, core, stabs, decoder, gauge_span, lx, lz)
    amp_pairs = pair_counts("amp", n, core, stabs, decoder, gauge_span, lx, lz)

    result = {
        "status": "EXACT_CONSTRUCTOR_REPLAY",
        "physical_tetrahedra_1based": {k: list(v) for k, v in PHYS.items()},
        "code_tetrahedra_0based": {k: list(v) for k, v in CODE.items()},
        "factorization": {
            "core_pauli_basis": "4^4=256=2^8",
            "core_gauge_kernel": "64=2^6",
            "core_quotient": "4=2^2",
            "four_site_subsets": "C(8,4)=70=2*5*7",
        },
        "core_syndromes": dict(core_syn),
        "fully_benign_four_site_subsets_1based": [list(x) for x in fully_benign],
        "named_tetrahedron_logical_classes": named,
        "weight2_pair_classes": {k: dict(v) for k, v in all_pairs.items()},
        "two_lowering_pauli_component_classes": {k: dict(v) for k, v in amp_pairs.items()},
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
