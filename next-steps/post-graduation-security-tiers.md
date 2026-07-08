# Next steps — Post-graduation security tiers (the time-lock, the recall floor, and Shamir forgiveness)

> Captured from design discussion. **Status: design, not yet implemented.** This
> opens the long-anticipated "different security tier" question and defines what
> a setup becomes *after graduation* (provisional key destroyed). Ties to
> `next-steps/provisional-key-bootstrapping.md` (graduation = the crutch is
> dropped), `great-wallet/THREAT_MODEL.md` (coercion / device seizure),
> `next-steps/cpnf-lifecycle-and-deck.md` §3 (the **graduation gate** — *when* a
> user crosses into this tier), and `next-steps/cpnf-*` (the review deck must
> change shape to match).

## 0. The gap this closes

A **panic button aborts the RSW-TLP**, falling the setup back to full memory-hard
derivation. That is correct but insufficient, because it makes security depend on
an *action*:

> **A surprise seizure gives the victim no chance to abort.**

So the panic button cannot be the floor — it is defense-in-depth. Post-graduation
security must rest on a barrier that is **already in force at rest and requires
nothing from the victim**. That barrier is: the entropy-carrying answers are
protected by keys **derived from recall itself**, so a seized device (with or
without an uncooperative person) yields only ciphertext. The TLP and the panic
sit *on top* of that floor, never under it.

## 1. The governing principle: no sub-threshold oracle

> **The atomic unit of _confirmation_ is the atomic unit of _attack_.** Any
> stored artifact that lets someone verify fewer than `E_min` bits of
> answer-entropy at once collapses the wall to that size.

Each stage conveys the same **32 bits** (a located point). That is stable design
and is **not** changing. The danger is *divide-and-conquer*: if there is a
**per-stage** oracle (and today there is — Train decodes each tap and says
"right/wrong"), the 128-bit space decomposes into a **ladder of 32-bit rungs** —
crack one stage (2³²), which unlocks the next, and so on. This is the
"2³² four times over instead of one 2¹²⁸ wall" problem.

The fix is not merely "more entropy per answer"; it is **removing every
sub-threshold oracle** and only ever confirming at the `E_min` level. `E_min` is
therefore best understood as **the confirmation granularity, which is
definitionally the attack granularity.**

> **This is a special case of the No-Gray-Area Principle**
> ([`../great-wallet/THREAT_MODEL.md` § Coercion-Resistance Lemmas](../great-wallet/THREAT_MODEL.md#coercion-resistance-lemmas-the-deadly-race-framework)).
> A sub-threshold oracle turns an infeasible wall into a *feasible ladder* — i.e.
> a **race** — which is exactly the gray-area outcome the Deadly-Race Lemma
> forbids. Every hardening below exists to keep a device seizure on one side of
> the line: *nothing feasible*, or *the secret only while the attacker is present
> and the victim captive* — never a feasible-but-slower offline path.

## 2. The two tiers

| | **Tier 1 — pre-graduation (convenience)** | **Tier 2 — post-graduation (self-standing)** |
|---|---|---|
| Reconstruction | provisional key (fast, no Argon2) | recall floor + TLP |
| Device seizure | game over (key is on/near the device) | yields only ciphertext behind an `E_min` wall |
| Per-stage feedback (Train hint `H`, per-tap right/wrong) | **allowed** (it is a learning aid) | **forbidden** (it is exactly the sub-threshold oracle) |
| Depends on panic/abort? | n/a | **no** — the floor is passive |

Tier selection is a setup-time property (or auto by value); Tier 2 costs
materially heavier reviews (see §5), so it is a deliberate choice.

## 3. Construction: Shamir over the stage points

The master secret becomes a **Shamir `t`-of-`n` interpolation of the stages**
(not the concatenation of all `n`).

- Each stage `k` contributes a 32-bit share `y_k = f(x_k)` where `f` is a
  degree-`(t−1)` polynomial over `GF(2³²)`; `x_k` is the (public) stage index.
- The **master secret is the polynomial** — `t` coefficients = `t · 32` bits.
  For a 128-bit secret, `t = 4`. So **`t = seed_bits / 32`, and `E_min = 32·t`.**
- Any `t` shares reconstruct `f` (hence the seed); fewer than `t` reveal
  **nothing** (information-theoretic).
- **Keep the chain, store the haystacks.** Fractals `(o,p,q)` stay chain-derived
  at setup but are **stored** post-graduation. They are one-way hashes of prior
  points, so storing them leaks nothing and gives no per-share oracle — but it
  lets **any card render independently** for review. Only the *needles* (the
  located points `= shares`) are recall-only; the stored `(re,im)` of Tier 1 is
  **dropped** in Tier 2.
- The only stored verifier is the **whole-seed checksum** (BIP39). There is no
  per-stage MAC — that is what enforces §1.
- **Accretion orbit (optional, floor-preserving).** To let the setup *grow* a stage
  without recalling every prior point, the **Argon2 orbit** — the per-stage seeds
  `{θ_k}` that continue the hard derivation onto new stages — may be stored. The
  **points themselves are never stored** (Shamir interpolation regenerates all `n`
  from `t` shares — redundant). Critically, an orbit in the clear **is** the
  per-stage oracle §1 forbids (`θ₂` checks `point₁`, `θ₃` checks `point₂`, … →
  crackable `2³²` at a time), so it must be stored **only encrypted under the
  threshold key `K = KDF(polynomial)`** (layer 3 below). Sealed, opening it needs
  `≥ t` shares, so it is floor-gated by construction and exposes no sub-threshold
  oracle — a checkpoint sealed under a key that itself needs `≥ t` shares. This does
  **not** weaken §1 or the recall floor. See
  [`cpnf-lifecycle-and-deck.md`](cpnf-lifecycle-and-deck.md) §2 "Stage accretion".

### Attacker vs. legitimate user (the asymmetry)

- **Attacker, 0 recalled shares:** must find `t` shares. With the fractals
  stored, any share value is guessable on a known fractal — but there is **no
  per-share oracle**: `< t` shares reveal nothing (Shamir) and the *only* check
  is the whole-seed checksum over a full `t`-tuple. Every `t`-tuple interpolates
  to *some* polynomial/seed, so the checksum offers no shortcut ⇒ `2^(32·t)`
  (= `2¹²⁸` for `t = 4`). (The floor is the threshold, not chain sequentiality —
  the stored fractals are renderable without recall.) Equivalently the attacker
  may **guess the seed directly** and verify it against the wallet address (the
  public ledger is an oracle): `2^(seed_bits)`. The two paths coincide exactly at
  `t = seed_bits/32`, which is why `t` is *pinned* there — a larger `t` does not
  raise this zero-compromise floor (see §6).
- **Legitimate user, `r` recalled shares:** pays `2^(32·(t−r))` to bail out.
  Recall is **free shares**. This asymmetry is the entire mechanism, and it
  survives **only** while nothing stored verifies a single share (§1).

### Verification, in three layers (and why the field is `GF(2³²)`)

Correctness is checked at three escalating strengths, each paid for honestly (no
free confirmation — confirmation is redundancy, and redundancy costs entropy or
recall):

1. **Encoder geometry — a free _syntax_ check, per tap.** The bit-string↔point
   map is a bijection onto the **sparse** leaf set: a near-unit fraction of the
   plane is contracted-away void that decodes to nothing. So a tap that is
   *accepted* (lands in a leaf) is already a strong well-formedness signal and a
   wild mis-tap is rejected outright — **for free**. It costs no entropy because
   it is not information about *which* leaf (all `2³²` are in leaf-land): the void
   exists only in coordinate-space (the human's medium), never in value-space
   (where the attacker enumerates leaf indices). Caveat: it is *syntax*, not
   *semantics* — "a leaf," not "the leaf"; an adjacent island passes. Strength
   scales with island isolation and zoom.
2. **Over-sampled shares — a cheap on-curve pre-check, paid in one extra recall.**
   Recall `t + e` and verify the extra `e` lie on the polynomial through the
   first `t` (`2⁻³²` false-pass per extra share, plain field arithmetic, no KDF).
   This is the import-compatible way to get error-detection; it is paid in
   memory, not entropy (§conservation).
3. **AEAD payload — the definitive _semantic_ gate, at threshold.** `K =
   Argon2id(reconstructed polynomial ‖ label)` decrypts the payload (the seed, or
   anything else the setup gates); the auth tag certifies the whole polynomial. The
   KDF is **memory-hard by mandate** (see §6 "Seizure-exposure hardening"): it makes
   the tag — and the public ledger — a *memory-hard* oracle, so every bail-out guess
   costs an Argon2id. It is **threshold-level** (needs all `t` → no sub-threshold
   oracle), self-contained (verifies offline against the stored tag — no ledger
   needed), and its floor is the seed entropy already budgeted (the tag *is* the
   assumed seed-guess oracle).

**Field.** Use **`GF(2³²) = GF(2)[x]/⟨m(x)⟩`**, `m` irreducible of degree 32;
elements are degree-≤31 polynomials over `{0,1}` (32-bit words), add = XOR, mul =
carry-less multiply mod `m`. Every element is a valid 32-bit leaf, so every share
`f(x_i)` is directly encodable — **no sliver, no `x`-hunting.** (A prime just
above `2³²` also works if you prefer a big-integer SSS library, but then the
`[2³², p)` sliver forces choosing the redundant shares' `x`-coordinates where
`f` lands in-window — extra machinery and a tiny data-dependent side channel that
`GF(2³²)` avoids.)

## 4. Forgiveness (why Shamir, concretely)

`n = 6`, `t = 4` (128-bit):

| Stages forgotten | Recovery | Cost |
|---|---|---|
| 0–2 | remembered `≥4` reconstruct directly | free |
| 3 | remembered 3 + brute-force 1 → interpolate → recover the rest | `2³²` |
| 4 | remembered 2 + brute-force 2 | `2⁶⁴` (heavy bail-out) |
| ≥5 | below threshold | infeasible (by design) |

So `n − t` stages may be forgotten *for free*, and forgetting beyond that
degrades **gracefully** via brute-force bail-out rather than a cliff. `n` and `t`
are independent knobs — but see §6 for what each *actually* buys (`t` is pinned by
the seed size; `n − t` is forgiveness).

### Bail-out doubles as the error-locator

When a group fails (≥1 wrong, opaquely — see §5), brute-forcing the missing
share to a checksum-valid reconstruction yields the **polynomial**, which
recomputes the correct point for **every** stage. Comparing against what the user
tapped reveals **which** stage was wrong. One feature: recovery **and** per-card
diagnosis.

## 5. Consequence for CPNF (cards vs. groups)

**Cards and groups are independent entities.** A *card* is a stage with its own
SM-2 state (unchanged). A *group* is any `≥t` subset convened for one review
session — chosen dynamically to contain the weak cards plus fillers to reach `t`
(e.g. review `A,B,C` by convening `{A,B,C,X}`, `X ∈ {D,E,F}`). Because there is
no stored per-group artifact (§3), **overlapping/dynamic groups are safe** — they
do not create the leak that stored per-group MACs would.

Feedback is coarse, exactly like the provisional-key card ("that you opened it
proves you accessed the key; grade only how *easy* it was"):

- **Group cleared** ⇒ proves every point in it was recalled, but **not** how hard
  each was. → self-grade ease **per card** ∈ {hard, good, easy} (never "again" —
  success proves recall).
- **Group failed** ⇒ proves ≥1 point forgotten, but **not** which. → penalize
  **no** card; the group stays due. Offer the **bail-out** (§4) to identify the
  culprit(s), then grade those "again" precisely.

SM-2 continues to schedule **cards**; the group is only the recall vehicle.

## 6. What `t` and `n` actually buy (and the fixed ceiling)

The zero-compromise brute-force floor is the **seed entropy**, *not* `32·t`. An
attacker who can verify a seed — knows the wallet address (the public ledger is
an oracle) or reads a stored seed checksum — simply guesses the seed at
`2^(seed_bits)`; the shares never enter. Therefore:

- **`t` is pinned at `seed_bits/32`.** Below it the seed is under-entropy; **above
  it the floor does not rise** (the attacker takes the direct seed-guess path).
  What a larger `t` (an over-determined / ramp split) *does* buy is **resistance to
  _partial_ compromise**: with `k` shares leaked (shoulder-surfing, a few coerced
  stages, or a seized sub-deck — *not* the TLP, which holds no shares) the residual
  is `2^(32·(t−k))`, so a bigger `t` makes each leaked share a smaller fraction.
  Under the Deadly-Race Lemma this is **first-order, not second-order**: partial
  compromise is exactly the seizure case, and `2^(32·(t−k))` is what decides
  clear-fail vs. gray-area race. It costs more recall per session. See the
  seizure-hardening subsection below.
- **`n − t` is the forgiveness margin** (§4) — no security effect.
- **The real security ceiling is the seed size (128 vs 256 bits), set once at
  creation.** It cannot be recalibrated later without generating a new seed and
  moving the funds (a re-key, not a tweak).

### Reconfiguring between sessions

The scheme *is* reconfigurable, but the two knobs differ sharply in cost:

- **`n` (redundancy) — cheap, incremental, per-session.** Add a stage:
  reconstruct (recall `≥ t`, or bail out), evaluate the *same* polynomial at a new
  `x`, memorize that one new point. Retire a stage: stop tracking it. Forgiveness
  is dialable a stage at a time without disturbing the others.
- **`t` (threshold) — heavy.** Changing it changes the polynomial *degree*, so it
  re-splits the seed under a new polynomial: **every share moves** → full
  re-memorization. A re-provisioning, not a between-sessions dial.

So "I was greedy on convenience, let me recalibrate" is realistic for
**`n` / forgiveness** and for **how much recall you maintain vs. lean on
bail-out** — but *not* a cheap lever for the headline entropy, which the seed size
fixes at creation. (Secondary costs of a higher `t`: harder to *single out* which
stage was forgotten, since you must convene `t` to attempt, and reviewing one weak
stage drags in `t − 1` others.)

**Effective entropy is a clean 32 bits per stage — no hedge needed.** The
encoder is a *bijection* between bit strings and points
(`great-wall-core/DESIGN.md` §"bijective mapping", with a geometric-bisection
fallback so every bit is always consumed), so all `2³²` codes are valid and
distinct and `2^(32·t)` is **exact, not optimistic**. A brute-force attacker
enumerates 32-bit *codes* (the share value `f(x_k)`), not screen positions; the
many-pixels-to-one-leaf tolerance only aids human recall and does not shrink the
code space, and the seed bits are uniform. So set `t = seed_bits / 32` exactly.

What *is* non-uniform lives on a different axis — **recall difficulty**: leaves
vary in size and salience, so some points are harder for a person to relocate.
That is a **scheduling/UX** concern (harder stages need more review), not a
security one; it does not reduce entropy.

### Seizure-exposure hardening (deadly-race remedies)

> **Superseded (design history).** The block-orbit / `(t,N,s)` / `64*`-floor /
> deep-master-block material below is the *earlier* framing. The canonical construction
> is [`coercion-resistant-orbit-protocol.md`](coercion-resistant-orbit-protocol.md)
> (`H*(H(·))` orbit, `Sh_i`-polynomial stages, cheap `K`). Kept here for lineage.

The No-Gray-Area Principle requires that a device seizure expose *no feasible
offline path*. Three parameters govern it, plus one unconditional primitive.

**Unconditional — memory-hard threshold KDF.** The reconstructed polynomial passes
through `K = Argon2id(polynomial ‖ label)` **before** it becomes the wallet seed /
AEAD key. This makes the public ledger (and the AEAD tag) a **memory-hard** oracle:
each of the `2^(32·(t−r))` bail-out guesses now costs one Argon2id, not a cheap EC
derivation. It is free to add and helps every tier, so it is always on. (Without it,
a 2-share seizure at `t=4` is `2⁶⁴` *cheap* checks — hours-to-days on a cluster,
i.e. a feasible race. With it, `2⁶⁴ × Argon2id ≈ 2^84` effective — infeasible.)

**The three knobs.**
- **`t` — secret strength + seizure resilience.** Floor `seed_bits/32`; *raising it
  above the floor* is the seizure knob (raises `2^(32·(t−s))`), capped at
  `2^{seed_bits}` (past which the attacker just guesses the seed directly). First-
  order under the Deadly-Race Lemma.
- **`N` — forgiveness + redundancy.** `N − t` free forgets; **does not** change the
  secret or the seizure math. Its role here is to *repay* the forgiveness that
  raising `t` spends, and to supply stages for finer sub-decking. Forgiveness and
  seizure-resistance do **not** trade against each other.
- **`s` — per-seizure exposure = sub-deck size** (below). A seizure exposes at most
  `s` non-consecutive shares.

**The exposure bound (the rule the app enforces).** A seizure of one sub-deck must
leave a residual that is infeasible under the hard KDF:

```
residual(seizure) = min( 2^(32·(t − s)) , 2^{seed_bits} )   must be infeasible.
```

The user picks **secret size** (→ `t` floor), **forgiveness** (`N = t + f`), and
**juggling tolerance** (`s`); the app validates the bound and warns otherwise. The
menu below is illustrative, not fixed — the formula is the spec, so it stays honest
as hardware moves.

| tier | `t`-of-`N` | wallet | seizure floor (hard KDF) | free forgets | sub-decks (`s=2`) |
|---|---|---|---|---|---|
| **Default** | 4-of-6 | 128-bit | `2⁶⁴ × Argon2 (~2^84 eff.)` | 2 | 3 |
| **Resilience** | 6-of-9 | 128-bit | clean `2¹²⁸` | 3 | 4–5 |
| **Max** | 8-of-12 | 256-bit | `2²⁵⁶` zero-compromise | 4 | 6 |

**Compounding.** With `s`-sized sub-decks and the hard KDF (feasibility ≈ 2 residual
shares), an attacker must compromise `⌈(t − 2)/s⌉` *independent* sub-decks — each its
own TLP window + transient-token capture — before reaching feasible range: 1 for
`t=4`, 2 for `t=6`, 3 for `t=8`. Raising `t` (funded by `N`) converts "survive one
seizure" into "survive several independent seizures."

**Sub-deck juggling, block-orbit, and the public Bitcoin-nonce `σ`-salt** — the
mechanisms that make `s` a hard cap (rather than a soft one) and that keep the stored
derivation orbit from re-exposing a per-stage oracle — are specified in
[`cpnf-lifecycle-and-deck.md`](cpnf-lifecycle-and-deck.md) §2 ("Stage-0 salt",
"Block-orbit", "Sub-deck juggling") and [`bitcoin-nonce-salt.md`](bitcoin-nonce-salt.md).

**Choosing `k` (block size) and `s` (sub-deck size).** They are *independent*: `k`
hardens the **orbit** oracle (an exposed checkpoint costs `2^{32k}`); `s` bounds the
**ledger** oracle (a seized sub-deck costs `2^{32(t−s)}`).

- **`k` (points per orbit checkpoint).** `k=2 → 2⁶⁴` (memory-hard — already
  infeasible); **`k=3 → 2⁹⁶`** (infeasible even *without* the hard KDF). Total
  derivation is `N·D` for **any** `k` (a block does `k·D` iterations for `k` stages),
  so `k=3` is essentially free — its only cost is a deeper within-block max depth
  (`3D`), felt only at hard-reset / setup (cached review reads sealed seeds, no
  re-derivation). **Recommend `k=3` as default.** Trade-off: points commit in groups
  of `k`, so a partial setup checkpoints only at `k`-stage boundaries.
- **`s` is coupled to `t`.** Safety needs `t − s ≥ 2` under the hard KDF (`≥ 3` for a
  clean fast-KDF margin), so **`s=3` requires `t ≥ 5`** — at `t=4` it collapses to
  `2^{32·1} = 2³²` (unsafe). Where `t` allows it, `s=3` **cuts the number of sub-decks**
  (fewer keys/TLPs to juggle) *without changing memorization* (still `N` stages): e.g.
  **6-of-9, `s=3` → 3 sub-decks** (residual `2⁹⁶`, compounding `⌈4/3⌉ = 2` decks) vs.
  6-of-9, `s=2` → 4–5 decks at the *same* compounding. So `s=3` is the **low-juggling
  form of the resilience tier**; the **default stays `s=2`** (its `t=4` can't carry
  `s=3`).
- **Non-consecutiveness** is now belt-and-suspenders: once `2^{32k}` (orbit) and
  `2^{32(t−s)}` (ledger) hold — both *count*-based, blind to adjacency — consecutive
  and non-consecutive sub-decks give the same residual. Keep it as cheap
  defense-in-depth against the derivation-walk oracle; it is no longer load-bearing.

**Memorization budget & adoption (the real UX risk).** Resilience is paid in *stages
to recall*: `N = 9`–`12` is doable but can scare users versus a familiar 12/24-word
seed. Four levers keep it humane — first-class, not afterthoughts:

- **Argon2 hardening buys back memory.** The memory-hard KDF makes `t=4` (`~2^84`)
  safe, so the **default stays 6 stages** and resilience tiers are opt-in, never
  forced. *Compute is the substitute for memorized bits* — the single most important
  lever.
- **Gradual increment.** Accretion lets a user **start small** (4-of-6) and add stages
  over months as consolidation proves out — the age gradient becomes automatic and the
  burden is amortized, never big-bang.
- **Gamification.** The crystal/island collection, streaks, and the "leveling-up" feel
  of accretion turn recall maintenance into a habit rather than a chore.
- **Value proposition.** The honest pitch — *this is what makes a `$5`-wrench attack
  fail cleanly instead of turning deadly* — is what justifies the budget, and must be
  communicated, not assumed.

### The `64*` floor & shallow/deep split

By the Deadly-Race Principle and stipulations S1/S2
([`../great-wallet/THREAT_MODEL.md`](../great-wallet/THREAT_MODEL.md)), the master
secret must sit **`≥ 64*`** from *every* seizable state — two memory-hard 32-bit
stages, never one (`64*` = `2⁶⁴` hours-scale Argon2d, S2-infeasible; `2³²` is
S1-feasible). This is **Theorem T1**: a master keyed to the *last* stage alone is
`32` bits from a before-last seizure, hence unacceptable.

- **The floor lives in the deep stages.** Partition into **shallow** (`1, 2`, near
  the seizable `σ`-salt) and **deep** (the rest). Shallow stages drive the chain,
  tacitness, and forgiveness but are *expected* to leak under seizure; the master is
  a KDF/Shamir over **deep** points, kept `≥ 64*` from any reachable state. Shallow/
  deep is the deadly-race gradient made structural.
- **No-single-point-oracle is the mechanism** (the same condition the stored orbit
  needs, above). The ≥2 deep points that carry the floor must be **block-committed
  (`k ≥ 2`)** so no seizable intermediate — running seed *or* intermediate fractal —
  checksums either alone. A bespoke `KDF(deep₁, deep₂)` is the 2-point instance;
  "delete the first after use" is **not** sufficient, since the continuation state is
  itself that point's `2³²` oracle. (The block-orbit condition is reached from *two*
  independent directions — the stored-orbit oracle and the deadly-race floor — which
  coincide at `k ≥ 2`.)
- **The ledger cross-oracles the pair (why exposing *one* point is already fatal).**
  The funded address is a *joint* oracle on `KDF(·, ·)`: the instant an attacker holds
  **one** master-point cheaply, the other is only `2³²` away (guess it → reconstruct →
  check the chain). So the requirement is not merely "the pair is `2⁶⁴` jointly" but
  the stronger "**no seizure yields *either* point below `64*`**" — which is why both
  must be a *joint deep block, wiped after commitment*, never two points with a gap.
- **Worked negative example — relabeling the indices can't help.** Take
  `master = KDF(p₃, p₅)` on a 5-stage chain. A seizure at **stage 4** — while the
  device assembles `σ‖p₁‖p₂‖p₃` to render board 4 — grabs **`p₃` raw**; then `p₅` is a
  lone `2³²` gate against the ledger. `2³²`, feasible. Choosing different indices only
  *slides* the vulnerable "between" window; it never closes it. The flaw is structural
  — the two points are traversed *with a gap*, not committed as one block. (This is
  why `p₁` being trivially seizable already dooms `KDF(p₂, p₄)`: `p₂` follows from `p₁`
  cheaply, then `p₄` is the lone gate.)
- **Minimal safe setup — 4 stages, hard-rederivation.** Two shallow + two deep;
  master = the two deep points block-committed → `64*`; `σ`-salted (no pepper);
  nothing stored. Provably on the right side of DRP at the smallest recall budget —
  the entry-tier setup.

## 7. The TLP and the panic button, reframed

- **Recall floor (passive):** always in force; `2^(32·t)`; defeats device-only
  seizure with no action required. This is the foundation.
- **RSW-TLP (delay on top):** imposes a wall-clock delay even *with* recall, so a
  coerced-cooperating victim still cannot produce the seed instantly (buys time;
  enables dead-man / rescue; the delay itself deters kidnappers). **What it
  encrypts is the *deck* — the `t`-of-`n` Shamir *structure* (fractals, params,
  schedule), never the shares** (recall-only). So surprise-seizure + wait-`T`
  yields only the deck and **still faces the `2^(32·t)` floor** — the floor is
  *automatic*, because shares are never stored or time-locked, so there is nothing
  for the TLP to "recover." (The TLP touches no shares at all; its residual value
  is the coercion *delay* and hiding deck *metadata*.)
- **Panic (defense-in-depth) — graduated, not binary.** Two rungs, matched to the
  threat, both used *at the vulnerability window* (near TLP completion):
  - **Soft — rewind TLP progress to a target milestone (typically 0), keep the
    deck.** *Buys delay:* pushes completion back so you aren't in the open state
    when a threat is near; the deck stays TLP-encrypted and the Shamir bail-out is
    kept. Cost ≈ the delay you re-injected (jade-clock §9 scenario 2).
  - **Hard — wipe the TLP-encrypted deck.** *Denies:* no deck ⇒ obligatory hard
    reset; the attacker gets a wiped clock **and** a recall-gated hard reset. Total
    `T_TLP + T_hard` (jade-clock §9 scenario 3).
  Neither is the floor — their unavailability under surprise doesn't compromise the
  setup (the recall floor stands regardless).

## 8. Scope note

The recall floor defeats **device seizure** (with or without an uncooperative
person). It does **not** by itself defeat rubber-hose extraction of recall from a
present, cooperating-under-duress victim — that is the TLP delay's job (plus
duress/decoy setups, out of scope here).

## 9. Open decisions

1. **`t` default** — *resolved:* **4-of-6 default** (with the unconditional hard
   KDF), **6-of-9 resilience** and **8-of-12 max** as advanced tiers; see §6
   "Seizure-exposure hardening." (Remaining sub-question: expose the raw `(t,N,s)`
   formula in advanced settings, or only the three named tiers?)
2. **Keep-chain-store-fractals (recommended) vs. fully decouple fractals** from
   the chain (`(o,p,q)_k = KDF(text, k)`)? The former is least disruptive.
3. **TLP scope** — delay-only that always leaves a residual recall threshold, vs.
   full self-recovery (and is it even offered in Tier 2)?
4. **Tier selection** — explicit at setup vs. auto by value.
5. **Group partition** — purely ad-hoc per session (recommended, since Shamir
   permits it), or persisted suggestions from the scheduler?
6. **Bail-out cost tuning** — how slow is each brute-force candidate (memory-hard
   per-guess cost) so the legit `2³²` is tolerable while an attacker who somehow
   holds `t − 1` shares is not.
