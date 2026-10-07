# Sqale Gate 2 — minimal fluorescence calibration packet v0.1

**Purpose:** replace the declared imaging assumptions in the MQM dual-view simulator with Sqale-calibrated quantities.

**Physical promotion:** 0  
**Ask type:** calibration data / one analysis pass, not a partnership and not a new device proposal.

## Publicly known

From the public Sqale architecture paper:
- optical tweezer spacing is 6 micrometres;
- the platform has individual optical addressing, non-destructive readout, and mid-circuit atom rearrangement;
- fluorescence images are shown before/after a moved block;
- normal post-processing detects atom loss by absence at an expected site;
- public loss correction infers the missing measurement/codeword value;
- the authors explicitly state that one additional bit flip can cause a loss miscorrection.

From the Sep. 2026 30-logical-qubit report:
- 80 atoms are grouped into ten eight-atom blocks;
- `[[8,3,3]]` is used for preparation and `[[8,3,2]]` downstream;
- single-atom loss is corrected in software by reconstructing a missing X-basis outcome;
- the company identifies real-time control and mid-circuit measurement as future priorities.

These public sources do **not** publish the full camera PSF, photon-count distributions, correlated drift covariance, or cross-view common-mode failure required for a hardware-level dual-view certificate.

## Minimal requested calibration quantities

### 1. One-frame localization model
For occupied and empty sites:
- detected photon-count histogram or sufficient summary;
- background count distribution;
- effective localization/centroid covariance or measured PSF;
- site-to-site variation if non-negligible.

### 2. Correlated geometric drift
Per fluorescence frame or short sequence:
- translation covariance;
- shear covariance;
- scale covariance;
- rotation covariance;
- temporal correlation between consecutive frames.

### 3. Camera health / common-mode failure
Frequency and signature of:
- blank frames;
- saturation;
- focus/exposure excursion;
- row/scan registration failure;
- control/trigger misalignment.

A bad frame must be representable as `HOLD`, not physical atom loss.

### 4. 3D / second-view feasibility — first go/no-go
One of:
- a genuinely independent second optical view with calibrated relative axis; or
- another existing observation that supplies equivalent depth/site discrimination.

If no independent second view or equivalent 3D observation exists on Sqale, the current MQM dual-view certificate is **not an integration candidate** for this machine.

### 5. Timing
- exposure duration;
- processing latency;
- time between the two receipts;
- maximum atom motion during that interval;
- whether both views correspond to one common admission epoch.

### 6. Calibration frames
Smallest useful data package:
- no-loss frames;
- one deliberately missing atom at each site, q1…q8;
- several drifted/repeated frames per state;
- bad-camera/control examples if available.

No quantum circuit is required for this calibration packet.

## Frozen certificate output

```text
SITE_CERTIFICATE {
  block_id,
  epoch,
  site_id_3d,
  view_A_health,
  view_B_health,
  likelihood_present,
  likelihood_absent,
  drift_fit,
  confidence_gap,
  fused_state = PRESENT | ABSENT | AMBIGUOUS,
  action = PASS | HOLD | REIMAGE | LOSS_PATH
}
```

## Frozen acceptance metric

Re-run the already frozen simulator with the calibrated Sqale distributions.

Compare:
- wrong certificate rate;
- `AMBIGUOUS/HOLD` fraction;
- false loss;
- missed loss;
- false duplication/merge.

The dual-view path advances only if the calibrated result remains operationally better than the existing "missing atom -> reconstruct or discard" workflow after imaging latency is counted.

## Stop rule

If Sqale has no second independent view/equivalent depth observation, or if calibrated imaging noise destroys the dual-view advantage at acceptable latency, stop Gate 2 for Sqale.

Do not solve that failure by proposing a new camera in the first approach.
