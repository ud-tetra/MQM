# MQM Gate 1 pre-loss gauge-history audit v0.1 — LOCK / PARTIAL REOPEN + UNIVERSAL NO-GO

**Physical promotion:** 0

## Question

Can the direct Sqale Gate-1 loss path be reopened by keeping a fresh pre-loss MQM gauge receipt, then measuring only gauge operators supported on the seven surviving atoms after one atom is lost?

Declared error set:

\[
\{I\}
\cup
\{\text{one arbitrary Pauli on one surviving site}\}.
\]

The known erased site is supplied to the decoder.

## Exact result

The answer depends on which physical site was lost.

### Lost sites 1, 2, 3 — PARTIAL REOPEN

The candidate errors form 14 inequivalent classes modulo the MQM gauge group plus arbitrary Pauli action on the erased site.

Therefore three binary receipt bits are impossible:

\[
2^3=8<14.
\]

Four bits are information-theoretically minimal.

For each of lost sites 1–3, an explicit set of **four pairwise commuting, survivor-supported MQM gauge operators** was found that gives zero recovery ambiguity.

One valid set for loss site 1 is:

```text
IXZIZXZY
IXZYZZIX
IIIZZYYI
IIIXXZZI
```

Loss site 2:

```text
IIIYYXXI
IIIXZIXZ
XIXXYYIX
XIXZYIZY
```

Loss site 3:

```text
IXIYXIYX
IIIYIYZZ
IXIIZXZX
IXIZYIZY
```

Each set:
- lies in the MQM gauge group;
- acts trivially on the erased physical site;
- is pairwise commuting;
- distinguishes the declared candidate classes sufficiently for recovery modulo erased-site gauge freedom.

Thus, **if a fresh pre-loss eigenvalue frame for the appropriate four checks exists**, a loss on sites 1–3 can in principle be followed by a survivor-only four-bit temporal gauge receipt.

This is a partial architectural reopening, not yet a hardware win.

### Lost sites 4–8 — stronger NO-GO

For these sites, even the **entire survivor-supported MQM gauge group** is insufficient.

Results:

- loss sites 4–7: 15 full-gauge signature bins, with 3 logically ambiguous bins;
- loss site 8: 16 full-gauge signature bins, with 6 logically ambiguous bins.

Example for loss site 4:

```text
X5
Y6
```

have identical commutation signatures against every survivor-supported gauge observable, while their difference

```text
IIIIXYII
```

is a nontrivial logical class modulo the erased-site gauge group.

Corresponding witnesses exist for every loss site 4–8.

Therefore no amount of **classical pre-loss gauge-eigenvalue bookkeeping plus post-loss measurement of the survivor gauge algebra** can universally distinguish a new arbitrary survivor Pauli that occurs after the loss.

This is stronger than the earlier central-stabilizer no-go.

## Timing consequence

A pre-loss history can only help with information that existed before that history was recorded.

If the model allows one additional arbitrary Pauli fault **after** the atom loss, the lost-site 4–8 ambiguity survives.

Therefore a universal Gate-1 repair requires at least one of:

1. an ancilla/history carrier that interacted with the missing site before disappearance and remains readable after the loss;
2. a restricted fault-timing/noise model excluding arbitrary post-loss survivor faults before recovery;
3. physical replacement followed by a proven recovery/code-switching circuit;
4. another measurement family outside the survivor-supported MQM gauge algebra.

## Gate ruling

\[
\boxed{
\text{sites 1–3: PARTIAL REOPEN candidate}
}
\]

\[
\boxed{
\text{sites 4–8: survivor-gauge-history NO-GO}
}
\]

A universal Sqale reproduction ask remains frozen.

## Highest-value follow-up

Do **not** build eight different heavy gauge histories yet.

First ask whether Sqale can expose:
- the physical loss time window;
- whether a fault can be bounded to occur before/after a stored receipt;
- any pre-loss ancilla/measurement record already present in their compiled block schedule.

If their hardware record naturally supplies a pre-loss receipt, re-evaluate against its actual location and timing. Otherwise Gate 1 remains frozen.
