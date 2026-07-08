# CPNF — setup lifecycle, deck model, and post-graduation self-custody

> Design note. Extends `great-wallet/ARCHITECTURE.md §4 celestial-peace-nf-core`.
> CPNF trains and maintains recall of a Great Wall setup. It has two phases —
> **pre-graduation** (still propped up by an external provisional key) and
> **post-graduation** (the setup secures itself). The cryptography of the setup
> itself is unchanged; CPNF is a study/maintenance layer on top of it. The
> buildable first slice is `cpnf-step1-scheduler.md`.

## 1. Pre-graduation — study against the provisional-key ciphertext

Until graduation (the user's brain has consolidated the setup), the setup lives
only as a **ciphertext backup encrypted under the provisional key** (the
existing bootstrapping key — see
[`provisional-key-bootstrapping.md`](provisional-key-bootstrapping.md)). In this
phase the user may study **as often as they like** — there is no TLP gating yet
— though following the CPNF (SM-2) schedule is recommended for good
consolidation. (SM-2 = P. A. Woźniak's SuperMemo algorithm, 1990:
<https://www.supermemo.com/en/archives1990-2015/english/ol/sm2>; cite it in docs
and code, don't paraphrase from memory.)

**CPNF consumes the encrypted setup file** to deliver the *same* stages the user
created, with **one crucial difference: the canonical island is NOT
highlighted.** This is not a security measure — it protects the **validity of
the memorization exercise**: showing the island first would test recognition of
a freshly-drawn marker, not genuine recall. CPNF decrypts the stored point only
to *validate* the user's located point, never to display it.

## 2. The deck — what a setup's Anki deck tracks

One deck per setup. It tracks a recall **score** (SM-2 state) for each of:

- **Each stage's point recollection** — the stored point is used to grade the
  user's unaided attempt (highlight off, §1).
- **Memory profile `m`** — must be recalled **exactly** (wrong profile ⇒ wrong
  Argon2 digest ⇒ every fractal breaks).
- **Initial salt** (the stage-0 input) — now the **Bitcoin-nonce `σ`-salt**, recalled
  as a *memorable date* rather than memorized entropy (§2 "Stage-0 salt";
  [`bitcoin-nonce-salt.md`](bitcoin-nonce-salt.md)).
- **Number of derivation steps between stages (`D`)** — exact-recall fact; the
  practical safety net for imperfect memory is *adjust-`D`-on-open-setup*
  (roadmap §3a), not any "approximate" special-casing here.
- **(bonus) Download provenance** — official repo / app-store id / a Bitcoin
  block height pinning the release, enabling a **supply-chain-resistant hard
  reset** (re-obtain a trusted build, not whatever a coercer hands you).
- **Per-stage user-defined export salts** — including the salt for CPNF's *own*
  setup (§3).
- **(optional) Miscellaneous reminders** — anything the user wants
  memory-insured, GW-related or not: "custody address of Shamir share #1",
  password-manager name, password-manager login (its master password presumably
  yielded by GW + an export salt), "wedding anniversary", …

### Storage model — uniform encryption

**Everything in a deck is encrypted uniformly** — the provisional key
pre-graduation, or GW-own-legs keys post-graduation (§3) — **including each
stage's points**, since CPNF needs the true point to grade recall accurately.

- **Tacitness / coercion-resistance is preserved by the encryption**, not by
  omission. Pre-graduation the external provisional prop guards the points;
  post-graduation the key is derived from the very secret the point encodes, so
  decrypting a stored point already presupposes reproducing it. Storing it grants
  an attacker nothing.
- **Deferred nuance (not implemented now).** Some cards are inherently less
  sensitive — a *salt* (a public-ish initial input) less than a *pepper* (a
  secret one) — so parts of a deck could in principle tolerate weaker storage.
  That tiering is out of scope: **uniform encryption for everything.**

### Stage accretion — growing the setup, and the floor constraint

> **Superseded (design history).** The orbit/accretion cryptography in this subsection
> is the *earlier* framing; the canonical orbit, master secret, and level-up/retirement
> are in [`coercion-resistant-orbit-protocol.md`](coercion-resistant-orbit-protocol.md)
> (§3 orbit, §7 pathway). Kept for lineage.

A setup can grow by **stage accretion**: appending a new point stage at the end
(the source of the "incrementally-grown setup" age gradient in
[`jade-clock-outsourced-anonymous-timelock.md`](jade-clock-outsourced-anonymous-timelock.md)
§9).

**Notation.** `D` = the number of **Argon2d Derivation steps between stages** (the
per-link memory-hard work); `N` = the number of **stages** (= Shamir total shares).

**The chain is an orbit of memory-hard seeds.** With `salt` the stage-0 input, the
setup's derivation visits the orbit points

```
{ salt,
  Argon2d^D(salt),
  Argon2d^D(salt ‖ point₁),
  Argon2d^D(salt ‖ point₁ ‖ point₂),
  …,
  Argon2d^D(salt ‖ point₁ ‖ … ‖ point_{N−1}) }
```

one seed per stage (`θ_k` → fractal `(o,p,q)` via SHA-256; the `digest` out of
`great-wall-core/burning_ship/argon2_pipeline.py` → `derive_stage_params`).

**Store the orbit, not the points.** The points are redundant — the degree-`(t−1)`
Shamir polynomial recovered from `t` recalled shares **regenerates all `N` points by
interpolation, for free.** Keeping the **orbit** (the seeds) is what makes growth
cheap: appending stage `N+1` then computes only the **one** next orbit point
`Argon2d^D(salt ‖ point₁ ‖ … ‖ point_N)`, continuing from the last stored point,
**instead of re-deriving every prior stage from `salt`.**

But the seed orbit, **left in the clear, is exactly the sub-threshold oracle**
[`post-graduation-security-tiers.md`](post-graduation-security-tiers.md) §1 forbids:
`θ₂` checksums `point₁` alone, `θ₃` checksums `point₂`, … so an exposed single-point
orbit is crackable **one point at a time** — a *feasible ladder*, i.e. the gray-area
**race** the Deadly-Race Lemma rejects
([`../great-wallet/THREAT_MODEL.md`](../great-wallet/THREAT_MODEL.md)). **Two
independent defenses** close it, because neither alone suffices once frequent review
forces the orbit to be *partially* unsealed:

1. **Coarsen it — the block-orbit** (feed `k` points per checkpoint; see below): an
   *exposed* checkpoint checksums a whole `k`-point block, so the smallest crackable
   rung is `2^{32k}` memory-hard (`k=2 → 2⁶⁴`), not `2³²`.
2. **Seal it — under the `t`-of-`N` threshold key** `K = Argon2id(polynomial)` (the
   same memory-hard key gating the AEAD payload, §"Verification, in three layers",
   layer 3). Opening the orbit needs `≥ t` shares, so a wait-out-TLP seizure gets
   nothing below the recall floor.

Pre-graduation the orbit rides under the provisional key; post-graduation it is
sealed under `K` **and** coarsened by the block structure — because routine review
cannot afford a full `t`-threshold unseal every time (**sub-deck juggling**, below,
bounds the exposure that follows). Sealing under a key that itself needs `≥ t` shares
is not a contradiction of "shares are recall-only" — it is a backup of the orbit
under a key derived from the very shares it would help re-derive.

**Accretion** is unchanged: reconstruct `K` from a **threshold** recall (bail-out if
short), decrypt the orbit, continue the derivation onto the new stage, re-seal, wipe
the plaintext — cost is a threshold reconstruction (recall `t`, not all `N`), never a
stored share.

> **Implementation note (protocol 0.3.0 re-concatenates; the orbit above is written
> in that form).** Today each stage's seed is `Argon2d^D` over the **full
> concatenation** `stage-0 text ‖ bits of points 1..k−1` (`derive_stage_params`:
> `data = stage_text_bytes(stage0_text) + bits_to_bytes(prior_bits)`), not `Argon2d^D`
> of the *previous seed*. So each seed is an independent `D`-step link over its own
> input: computing the next orbit point is one `Argon2d^D` link (`D` steps) whether or
> not the earlier seeds are stored, and the sealed `{θ_k}` chiefly serve as a
> **derivation/render cache** (skip re-deriving priors for review). A genuine
> *running-orbit* refinement — `θ_{k+1} = Argon2d^D(θ_k ‖ point_k)` — is what makes the
> **last** sealed seed the sole checkpoint, so continuing strictly needs it and
> "continue the orbit from the last point" becomes literal. Either way accretion is
> ≈ one `Argon2d^D` link and the sealed-orbit floor argument is unchanged; adopting
> the running-orbit form is a protocol decision (would bump `PROTOCOL_VERSION`).

### Stage-0 salt — the Bitcoin-nonce salt (no pepper)

Stage 0 carries a **public, per-user salt `σ`** derived from Bitcoin block data at a
user-memorable date — **not a secret pepper** (full spec + formal results in
[`bitcoin-nonce-salt.md`](bitcoin-nonce-salt.md)). The only job stage 0 must do for
the orbit is defeat **precomputation**: a low-entropy or shared stage-0 would let an
attacker precompute one rainbow table and reuse it against every victim, bypassing
the memory-hard barrier for the shallow stages. `σ` closes both holes — it is
**unpredictable before the date** (Corollary N2, so no pre-dated table can contain
it) and **per-user** (Corollary N3, so tables don't amortize across targets).

Because `σ` does this while being **public and memorization-free** (the user recalls
only the date; the app reconstructs `σ` from the chain), the tacit **"canonical
stage" pepper is retired**: no secret at stage 0, no coercion target, no memorization
budget. `σ` seeds the orbit (`Argon2d^D(σ)`, `Argon2d^D(σ ‖ p₁ ‖ p₂)`, …). Note `σ`
is *not secret* — but secrecy was never the salt's job; N2/N3 are (see the salt doc).

### Block-orbit — feed `k` points per checkpoint

To deny even an *exposed* orbit a single-point oracle, incorporate points **`k` at a
time**. All `k` stages of a block share one point-prefix and differ only by
**iteration depth**; the block's `k` points enter the chain **jointly** at the next
checkpoint:

```
{ σ,
  Argon2d^D(σ),        Argon2d^{2D}(σ),          ← block 1 (stages 1,2)
  Argon2d^D(σ‖p₁‖p₂),  Argon2d^{2D}(σ‖p₁‖p₂),    ← block 2 (stages 3,4)
  Argon2d^D(σ‖p₁..p₄), Argon2d^{2D}(σ‖p₁..p₄), … ← block 3 (stages 5,6)
```

No single point is ever checksummed alone (the first thing that commits `p₁` also
commits `p₂`), so the exposed-orbit oracle granularity rises to **`2^{32k}`**
memory-hard probes (`k=2 → 2⁶⁴`; **`k=3 → 2⁹⁶`, the recommended default** — infeasible
even without the hard KDF, at the *same* `N·D` total work; see
[`post-graduation-security-tiers.md`](post-graduation-security-tiers.md) §6 "Choosing
`k` and `s`"). `Argon2d^{2D}(C)` is just `Argon2d^D` applied to `Argon2d^D(C)`, so
storing both depths is a compute cache, not extra secret. Adopting the block form is a
`PROTOCOL_VERSION` change from 0.3.0 re-concatenation (note above).

### Sub-deck juggling — cap seizure exposure at `s`

Because review is far more frequent than vault-opening, the orbit cannot sit behind a
full `t`-threshold unseal for *every* review. **Partition the `N` stages into
sub-decks of `s` non-consecutive stages** (4-of-6 → `{1,5}, {2,6}, {3,4}`, `s=2`,
three decks). Only the *active* sub-deck is unsealed for a review, so a device
seizure exposes **at most `s` non-consecutive shares** — held infeasible by the §6
exposure bound `min(2^{32(t−s)}, 2^{seed_bits})` under the hard KDF. `s` is coupled to
`t` (`t − s ≥ 2`), so **`s=3` needs `t ≥ 5`** — the low-juggling form of the resilience
tier (6-of-9 → 3 decks); the `s=2` default stays `s=2`
([`post-graduation-security-tiers.md`](post-graduation-security-tiers.md) §6 "Choosing
`k` and `s`").

- **Asymmetric placement.** The `σ`-salt is public, so the risk is a deck
  whose *lowest* stage is shallow (few unknowns from the public `σ`). `{3,4}` is the
  deepest-floor deck; `{1,5}` and `{2,6}` each pair a shallow stage with a deep one.
- **Gating.** `K_i ← KDF( H(pts_{i+1}) ‖ H(pts_{i+2}) ‖ TLP_i )` — unsealing deck `i`
  needs the *other* decks' point-hashes plus its own TLP. The hashes bind the gate to
  knowledge of the other decks **without storing their points** (preimage resistance).
- **Transient tokens (load-bearing).** The gating hashes must be **recall-derived and
  wiped at unseal**, never persisted. Otherwise a seizure that catches deck `i` open
  captures `H(i+1), H(i+2)`, and with the just-opened `H(i)` the attacker holds all
  three hashes and can chain the remaining decks offline via their TLPs — a
  feasible-slow path, the Deadly-Race gray area. With transient tokens a single-deck
  capture leaves the attacker **one hash short** of every other deck's `K` (each needs
  two), so the cyclic structure **deadlocks at one deck**.
- **Worst case, cleanly on one side of the line.** Surprise seizure at `TLP_i`
  imminence, before panic, held through `TLP_i`: attacker leaves with **one sub-deck
  (`s` non-consecutive stages) + the public `σ`** — below threshold, infeasible to extend
  (clear *fail*). A longer seizure that also outlasts `TLP_{i+1}` reaches threshold —
  but the victim was captive throughout, so it is a **clear success with no free
  racer**, not a race. No gray area either way.

## 3. Graduation — the gate (honest grade → honest lockout estimate → user decides)

Graduation is the **one-way, user-confirmed** milestone: destroy the provisional
key; the setup becomes self-standing (Tier 2). **Never automatic** — the app only
shows the green light. The chain is *honest grading → honest lockout estimates →
the user's own call at an acceptable risk for a target delay*.

**Honest grading is the foundation.** Grades measure **memory, not outcome**: a
point found by luck, by guessing, after giving up, or via brute-force **bailout**
must be graded **Again (1)** despite the success, so it does not falsely
consolidate. (Already wired: Again is always available after a find; the `H` hint
forces Again; a bailout-recovered stage is graded Again by the error-locator.)
Garbage-in grades poison both the schedule *and* the lockout estimate, so the gate
would lie — hence the manual must state this loudly.

**Per-card consolidation** (conservative SM-2): `consolidated(card) :=
intervalDays ≥ Ic AND repetitions ≥ Rc`. A lapse zeroes the interval, so it is
auto-excluded. Defaults **`Ic = 90 d`, `Rc = 5`** (reached at the 5th successful
`good` review; imposes a **~2-month wall-clock floor** — consolidation cannot be
rushed).

**Lockout probability** (SM-2 gives intervals, not probabilities, so overlay a
forgetting curve): `R(T) = r*^(T/I)` per stage (`r* ≈ 0.9`), composed to a
deck-level lockout probability that is **scenario-dependent**:
- **Normal recall** — symmetric Shamir: `Binomial(n, p)`, `p` per-stage; lockout =
  recalled `<` bail tolerance.
- **Hard reset** — *directional* (prefix-only) **and oracle-free**: there is no
  stored fractal to check a stage against, so a forgotten stage can't be bailed
  independently — it must be brute-forced *jointly to the terminal AEAD*. Tolerance
  is effectively **one** forgotten stage (only via partial-recall narrowing + a
  human perceptual oracle on the next stage — see
  [`hard-reset-area-narrowing-recovery.md`](hard-reset-area-narrowing-recovery.md));
  two or more is unrecoverable. This is
  **far worse** than the deck-present `2³²`-per-stage bail. See
  [`jade-clock-outsourced-anonymous-timelock.md`](jade-clock-outsourced-anonymous-timelock.md)
  §9.

Default sharing is **4-of-6** (128-bit secret; forget ≤2 free; `2³²` bailout at 3;
`2⁶⁴` at 4). **Graduation decision:** the user destroys the provisional key when,
for their **target next-session delay**, the lockout probability across the
scenarios they care about is `≤` their chosen `ε` — "enough stages consolidated
for acceptable lockout at the target delay." `Ic/Rc` are the conservative floor;
the `ε`-calibration is the general, user-tunable form. **Caveats (err safe):** the
curve shape, `r*`, and *stage independence* are assumptions (correlated forgetting
makes the estimate optimistic) — guidance, not a guarantee; the per-user-calibrated
upgrade is FSRS/SM-17 (needs review-log storage).

### The graduation → first-arming sequence
At graduation the user, in order:
1. **Confirms the gate** (lockout `≤ ε` at the target delay).
2. **Seals the setup under the recall floor** — Shamir `t`-of-`n`; nothing
   sensitive stored but the fractals `(o,p,q)` + the AEAD tag (see
   [`post-graduation-security-tiers.md`](post-graduation-security-tiers.md)).
3. **Arms the first Jade Clock:** the RSW-TLP **encrypts the deck** — which holds
   the `t`-of-`n` Shamir *structure* (fractals, params, schedule), **not the
   shares** (recall-only). So a surprise seizure that waits out the clock gets
   only the deck and **still faces the `t·32`-bit recall barrier** — the floor is
   automatic (no shares are ever stored or time-locked). Sized to the target
   delay.
4. **Destroys the provisional key.**
5. **Starts the clock immediately — locally, via hired non-dummy Jade-Clock
   chains, or both** (both = liveness redundancy: local is the always-available
   fallback, hired chains carry the anonymity/offload; "marketplace = enhancement,
   never dependency").
6. **Re-arms at every close** — the next clock starts ticking immediately, sized
   from the then-current SM-2 grades (solid → longer `T_TLP`; shaky → shorter).

The construction of the clock (per-user RSA + milestone digests, HTLC verify-and-
pay, the marketplace, cover traffic) is in
[`jade-clock-outsourced-anonymous-timelock.md`](jade-clock-outsourced-anonymous-timelock.md).

## 4. Post-graduation — "setup standing on its own legs"

> **Superseded — retained for context.** The cryptography below (sequential
> export-salt keys) is replaced by the Shamir recall floor + a TLP that
> **encrypts the deck (Shamir structure, not shares)** — the shares stay
> recall-only, so waiting out the clock still faces the `t·32` floor. The current
> model is in
> [`post-graduation-security-tiers.md`](post-graduation-security-tiers.md) and
> [`jade-clock-outsourced-anonymous-timelock.md`](jade-clock-outsourced-anonymous-timelock.md);
> the whole-setup-TLP wording in §4.4 below does not apply.

1. **The provisional key is destroyed.** The external prop is gone.
2. **Own-legs key schedule.** CPNF derives its encryption keys from the user's
   *own recalled secret* using a **sequential family of export salts**
   `CPNF-1, CPNF-2, …` — each revision KDFs the next key that encrypts the
   setup (and its deck). Sequential, not fixed, so each revision rotates the key
   (a leaked interval-key does not unlock the next ciphertext). *Cost: one small,
   non-secret piece of state — the current index. If lost it is recoverable by
   trial-decrypt from `CPNF-1`, just slower. The own-legs key is **never**
   independently stored — that is what keeps this self-custody rather than a
   stored-key model.*
3. **Derivation shorter than the maintenance interval → just re-derive each
   time.** Before each scheduled revision, rerun the hard derivation from memory.
   *Example: a 24-hour setup with a one-week interval — every Friday/Saturday the
   user reruns derivation and does the exercise on the weekend.* No TLP needed.
4. **Derivation ≈ or > the interval (or to avoid planning/syncing the
   re-derivation) → RSW-TLP-encrypt the deck.** The TLP setup is itself KDF'd
   from the own-legs secret (§4.2) and is **never written to disk** (or, if it
   must be, only to a **wipeable medium**). It encrypts the GW setup **in place
   of the provisional key**. (Uses `tlp-core` / `jade-clock`.)
5. **Panic button (wrench-attack defense).** On perceived coercion risk, a panic
   button **aborts the sequential squaring** and **wipes the setup from RAM**.
   Recovery falls back to a hard reset (rerun derivation).
6. **Outsourcing the sequential squaring** (untrusted compute). To keep it safe,
   the user does **one** of:
   1. store the GW **ciphertext on an HDD they can physically wipe**; or
   2. make the **RSW-TLP setup necessary-but-not-sufficient** to decrypt GW — a
      second, physically-destroyable provisional key is also required, so the
      outsourced squaring alone never yields plaintext.
7. **Alternatives to outsourcing the squaring** *(to be defined)*:
   1. GW setup lives on **Desktop**, the RSW-TLP setup runs on **mobile**, keys
      pass by **QR scan**; the portable device gives an always-accessible abort.
   2. **Mobile hosts the abort button** for RSW-TLP running on a remote Desktop;
      **loss of the mobile↔desktop connection also triggers abort.**

## 5. Next steps / to define

- **Adjust `D` on an open setup** and **calibration nudging round `D`** — the
  practical recovery path for imperfect `D` memory. Tracked in
  [`chained-protocol-size-and-ux-roadmap.md`](chained-protocol-size-and-ux-roadmap.md)
  §3a.
- **Time-to-clear as a scoring signal (maze-rat analogy).** The wall-clock time
  the user takes to locate each stage's point could feed the card's grade, the
  way maze-solve latency indexes a rat's learning (cf. the framing in
  `ARCHITECTURE.md`). Today the Again/Hard/Good/Easy grades already encode
  attempts + hesitation; this would make **time an explicit, quantitative
  input**. *To be defined.*
- The **§4.7 abort-button topologies** remain *to be defined*.
