# Discussion

## D.1 What the negative result means

The most important conclusion of this paper is the **negative
result itself**: the multi-task CNN + cross-domain transfer
hypothesis does not hold under the tested conditions. This is
**not** a verdict that the cross-domain transfer concept is
fundamentally flawed for agriculture; it is a verdict that the
specific implementation tested here — synthetic data + CPU + 8
epochs — does not work.

Three separable failures contributed:

1. **Synthetic labels with no seasonal dynamics.** The phenology
   pattern (low → peak → decline) was too simple for the
   network to learn from in 8 epochs; real Sentinel-2 has
   substantial sub-seasonal variability (e.g., flowering vs
   vegetative phases) that the CNN needs to disambiguate crop
   state.

2. **Insufficient training.** 8 epochs at batch size 1 is not
   enough for any non-trivial deep-learning result. Standard
   transfer-learning recipes use ≥ 30 epochs at batch size
   ≥ 32. The 8-epoch pilot was a smoke test, not a
   convergence.

3. **Source-pretrained encoder not exercised.** The Yvutu
   deforestation encoder (Chapter 3) was a 300M-parameter
   Prithvi-fine-tuned model; the Yrupe pipeline currently does
   not use it as the source encoder. A from-scratch ResNet was
   used as the encoder instead. The cross-domain transfer
   hypothesis therefore was not even tested.

We state all three failures explicitly because the original
draft of this chapter reported "F1 = 0.83" (aspirational target,
not measured) and "transfer ratio = 0.74" (also aspirational,
not measured) as if they had been measured; in fact those
numbers were aspirational (literature benchmarks), and the
experiment that was supposed to verify them was the pilot
that returned the current degenerate result.

## D.2 What the negative result does NOT mean

The negative result does not mean:

- **Cross-domain transfer learning from satellite imagery to
  crop yield is impossible.** The published literature contains
  successful examples (e.g., the [Kamilaris & Prenafeta 2018]
  review of deep learning in agriculture documents multiple
  cross-domain success cases).
- **Sentinel-2 imagery is uninformative for soybean yield.**
  Many papers have demonstrated real R² > 0.60 for soybean
  yield from Sentinel-2 + climate features.
- **The Yrupe architecture is fundamentally broken.** The
  12-layer ResNet encoder + 3 task heads is a standard
  multi-task learning recipe; the issue is the training, not
  the architecture.

The honest interpretation: **the experiment was not run with the
data and compute budget that the headline claims would require**.
We made the aspirational claims knowing this, and the pilot
result is a correction.

## D.3 What would need to change for the hypothesis to be testable

Three concrete changes, in priority order:

### D.3.1 Real INBIO yield data + real Sentinel-2

The fundamental constraint is **labeled data**. The synthetic
labels are not representative of real soybean phenology and
cannot support non-trivial learning. The required change:

1. **Partnership with INBIO farmers or with the Ministry of
   Agriculture** to obtain 500+ farm-level yield records for
   multiple growing seasons.
2. **Sentinel-2 L2A download** for the corresponding
   geographic area (≥ 150 tiles covering the Eastern Pampas).
3. **Per-pixel alignment** of Sentinel-2 time series to each
   farm's yield record, using Catastro parcel boundaries.

Estimated cost: 2-3 months human (partnership) + 2 weeks compute.

### D.3.2 GPU training

CPU is not a viable training environment for a deep-learning
multi-task CNN with a 300M-parameter pretrained backbone.

Required:

1. **Vast.ai A100 80GB** instance, ~$1/hr, 12 hours = $12.
2. **Batch size 32** (instead of 1) — enables batch
   normalization.
3. **30 epochs** (instead of 8) — sufficient for convergence on
   standard remote-sensing datasets.
4. **Cosine LR schedule** with warm-up — standard transfer-
   learning recipe.

The combined GPU spend for a publication-quality re-run is
**$50-150**.

### D.3.3 Real source encoder

The cross-domain transfer hypothesis requires a real source
encoder. The Yvutu (Chapter 3) deforestation model provides
exactly this: a Prithvi-based encoder trained on 16,628 km² of
real Hansen-derived loss data. Using the trained Yvutu encoder as
the source for Yrupe is the genuine cross-domain test.

Required:

1. Export the Yvutu encoder weights from
   `outputs/p0011/` (after the GPU re-run documented in
   `discussion.md` Section D.4 of Chapter 3).
2. Wire the encoder into the Yrupe multi-task CNN's backbone slot.
3. Compare: target-task performance with Yvutu-pretrained encoder
   vs. ImageNet-pretrained encoder vs. from-scratch encoder.

Estimated cost: 4 hours code change + 1 hour GPU training time.
The bottleneck is the **availability of the Yvutu encoder
weights** (blocked on the Tier 3 Yvutu GPU re-run).

## D.4 Path forward + the next experiment that should happen

If the project pursues this paper:

1. **Estimate the cost**: 1 partner-meeting with INBIO +
   2-3 months lead time for the partnership + $50-150 GPU + 4 h
   integration = the publication-quality re-run.
2. **Defer until after Chapter 3 (Yvutu) has the GPU re-run.** The
   cross-domain transfer requires the Yvutu encoder, which
   requires the GPU spend documented in Chapter 3
   `discussion.md` Section D.4.
3. **Run the synthetic pilot at 32 batch + 30 epochs** as a
   minimum-viable confirmation that the architecture converges
   under standard training conditions. If it does, the real-
   data run is worth doing.

The synthetic pilot at $\approx$ 0 cost took 7 minutes of wall
clock on a CPU. The publication-quality re-run at the
estimated cost is a 100× or so investment from where we are.
That is the appropriate scale of investment before committing
to a multi-year re-run.

## D.5 Why publish a negative result?

It is reasonable to ask why publish this paper when the
hypothesized result is falsified. Three reasons:

1. **Documentation of failed experiments is itself a research
   contribution.** Saving the community 6 months of failed
   CPU training by surfacing this negative result.
2. **Path-forward clarity.** The three changes in Section D.3
   are concrete and modest in cost. The paper is publishable as
   "do this differently" rather than "we did this and it didn't
   work, sorry".
3. **Methodology publication.** The synthetic-data experimental
   design + the cross-domain transfer pipeline are both
   reusable for other researchers in data-scarce agricultural
   applications.

This paper is a worked example of the project's broader
honest-reporting convention (see `docs/CONVENTIONS.md`).
Publication with measured numbers that falsify the headline
claim is the contribution that distinguishes this thesis
substrate from the standard literature pattern of "we report
great numbers" + a methods section that turns out to be
under-engineered.

## D.6 Limitations

The pilot has the following limitations, in addition to the
negative-result framing:

- **Train/test split is scene 1 only**; the other 3 scenes are
  held out qualitatively only. A temporal split (2022 train /
  2023 test) would be needed for generalization claims.
- **Sample is 4 scenes.** Statistically, n=4 scenes does not
  support any generalization claims.
- **No comparison to a non-transfer baseline.** A
  Random Forest trained directly on the soybean regression
  task (without the cross-domain transfer) would be the fair
  baseline against which to measure transfer signal. We do
  not include this comparison because the CNN itself did not
  converge.
- **No per-pixel augmentation.** Real-data augmentation
  (rotation, flip, crop, brightness) would help with sample
  efficiency; the synthetic dataset was not augmented.

These limitations are what the real-data replication (Section
D.3) addresses.
