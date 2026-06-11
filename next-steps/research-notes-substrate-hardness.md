# Research notes — Substrate hardness: parameter-description complexity

> **Research targets for the doctorate** — to be established *empirically* (numerical
> measurement on the actual fractal) **and/or** by *theorem* (asymptotics of escape-time
> level-set measure and parameter sensitivity). **Not part of the submission.**
> Names are provisional (open to revision); original working tags kept in brackets.

## Motivation
Naively, `n` fixed-point parameters carry `64n` bits. The security-relevant question is
sharper:

> Given the encoding of **one 32-bit point** (a location in the fractal labyrinth), what is the
> **minimum MSB precision of the fractal parameters θ** needed to determine — *unambiguously* —
> the labyrinth (the islands) in which that point sits?

This quantity governs the hardness of **bypassing the memory-hard parameter derivation by
*describing* the fractal** (reconstructing θ from perceptual interrogation — cf. OE4's
inverse-problem / one-wayness).

**Design goal (haystack / needle).** Specifying *which* labyrinth (the haystack/barn) should
cost **more** than specifying *where* in it the point sits (the needle):
*"finding the haystack in the barn is harder than finding the needle in the haystack."*

## The three quantities

1. **Entropy-density exponent** `ρ`  *(Rzb)*.
   Asymptotic relation between encoded bits `b` and area contraction: `A_leaf / A₀ ≈ 2^(−b/ρ)`,
   i.e. `ρ = b / (−log₂(A_leaf/A₀))` = **secret bits per bit of geometric capacity consumed**.
   **`ρ < 1` reliably.** When a bit selects the *larger* child, the bisection **contracts that
   child toward the split line** — discarding *part* of the larger half as a **dead zone** (it does
   **not** discard the whole half). The contraction factor is the exact integer fraction
   `f(r) = (1 + 3r)/4` with `r = s/l` (`f = 1` when the children are equal; `f → 1/4` when maximally
   unequal), which bounds the larger child's area growth and makes area contract *faster* than one
   bit per step. The deficit `(1 − ρ)` is **checksum capacity**: if a wrong decode lands in a
   contracted-away **dead zone**, it is **rejected** by validation (`decode_full`) — error detection
   for free, analogous to the BIP-39 / Formosa checksum. **Sub-unity entropy density is therefore a
   feature, not a loss** (and is orthogonal to the decorrelation criterion below — they do not trade
   off). *(See `great-wall-core/DESIGN.md` — contraction `f(r)=(1+3r)/4`, dead-zone rejection.)*

2. **Island-area law** `Ā(e)`  *(Rez)*.
   The asymptotic average area of an island of escape count `e`, as `e → ∞`. A
   measure-geometric property of the escape-time level sets (related to the fractal's dimension
   and boundary measure). Sets how "fine" the labyrinth is at each escape level.

3. **Parameter-precision threshold** `Π(e)`  *(Rpe)*.
   For a parameter `θᵢ`, the number of most-significant bits such that perturbing **below** them
   leaves the islands of escape count `e` (mostly) unchanged, while perturbing **at/above** them
   makes *most* of the level-`e` island-area mismatch, with high probability.
   *(Formalize "most" via area measure `≥ 1−ε`; "probably" via a distribution over
   perturbations.)*  Per-level parameter resolution.

## Combined target

**`Π*`** := minimum MSB precision of θ to pin the islands around a given encoded point —
composed from `ρ` (levels traversed by the `b`-bit encoding), `Ā(e)` (their sizes), and `Π(e)`
(precision per level).

- **Point-description complexity** `D_pt ≈ b` (≈ 32 bits), modulo recognizable-landmark help
  (the non-transmissibility question).
- **Substrate-description complexity** `D_θ ≈ Π*`.
- **Security inequality (design for):** `D_θ ≫ D_pt`.
  If `D_θ` is infeasible to convey under the perceptual-oracle model (OE4), interface
  availability is contingent on the memory-hard derivation — no descriptive shortcut.

## Official design rule — one 32-bit point per stage, chained by hashing

**Rule (official).** The protocol encodes **exactly one 32-bit point per stage**, and **each stage's
fractal is derived by hashing all preceding points** (memory-hard: Argon2 → SHA-256 → θ). One stage
= one fractal = one haystack; one point = one needle. There is **no amortization** — the attacker
must reconstruct a *whole* fractal (`Π*` bits) per ~32 entropy bits.

**Why this is the move.** Chaining one point per stage **multiplies the cost of query-deciphering
the haystacks by the number of stages**: to descriptively bypass the memory-hard derivation, the
perceptual-oracle attacker must reconstruct *every* fractal in the chain, and cannot start on stage
`k+1`'s fractal until stage `k`'s point is fixed (the next θ depends on all prior points). So
`D_θ` scales with the number of stages while `D_pt` stays ≈ 32 bits per point — the haystack/needle
inequality `D_θ ≫ D_pt` is enforced *per stage and compounded across the chain*.

**Instantiation (128 bits).** 128 / 32 = **4 stages → 4 points**. The **first fractal is canonical**
(fixed, public — `o=p=q=0`), so it is not a haystack the attacker must *find*; the remaining
**3 fractals are secret/derived haystacks**. Hence *128 bits ⇒ 3 fractals to decipher, not 1.*
(Generally: `⌈bits/32⌉` stages, of which the first is canonical and the rest are secret haystacks.)

**Breaking change.** This **supersedes** the current prototype's two-stage / multiple-points-per-stage
scheme (`great-wall-core/DESIGN.md`: 2 stages, 1/2/4 points per stage). It is a **hard,
backward-incompatible protocol update** — it requires **discontinuation / non-compatibility** with
the existing prototype version (encodings do not round-trip across the change).

## Design criterion (PRIORITY): perceptual non-ascertainability of θ

**Objective (the actual target).** Under the perceptual oracle (OE4), **θ must not be ascertainable
to MSB precision `Π*` by perceptual querying.** Equivalently — and this is the framing to formalize
against — the **mutual information the perceptual oracle yields about the high-order bits of θ must
stay below `Π*`**: the perceptual channel's *capacity* about the labyrinth is too small to read it
out, so interface availability stays contingent on the memory-hard derivation with no descriptive
shortcut. Non-monotonicity (below) is *one approach* to this, not the objective itself;
a design that fails the non-monotonicity test can still meet the objective by another route, and any
approach that bounds the channel capacity qualifies. **These are still theoretical approaches** — we
do **not yet** have a method to reliably evaluate their effectiveness — so they are deliberately
called *approaches*, not mechanisms or guarantees.

**A palpable analogy (needle / haystack / barn).** A user's private fractal (in general, their
perceptual *substrate*) is a **haystack**; the secret particular object hidden in it — the entropy
reservoir — is the **needle**; and the space of all possible haystacks is the **barn**. The protocol
is effective only if specifying *which* haystack (within the barn) **necessitates the long memory-hard
derivation of the previous steps**. Concretely: it must **not** be true that perceptual querying of a
haystack's *identifiable aspects* suffices to specify it — not exactly, and not even to enough
precision that the needle's specification remains possible. We pursue three approaches to enforce
this. In a slogan: *through perceptual-oracle querying alone, finding the haystack in the barn must
be far harder than finding the needle in the haystack — the barn is a less tractable space than the
haystacks are.*

**Threat.** An attacker UI with one slider per parameter, plus a *cooperating* victim, tries to
**narrow the interval** containing the private θ by **recognition feedback** ("warmer/colder"). This
attack is cheap for one specific reason: it **decomposes into independent per-axis 1-D searches**
(≈ `n · log₂(1/res)` queries). The three approaches below attack this from two angles: (a) and (b)
**break the per-axis decomposition** that makes it cheap, while (c) **inflates the raw cost** of the
search and of learning the map in the first place.

### Approach (a): perceptual non-monotonicity / decorrelation — *kill the signal*

The map **θ → recognizable visual aspects** has **no perceptually-monotone similarity signal** near
the secret: along *every* parameter axis, any *resolvable* step makes the labyrinth look
**unrecognizably / discontinuously different** (appearance *decorrelates* under the smallest
resolvable θ-perturbation). Recognition feedback then carries no warmer/colder information, and the
search degrades to brute force. Non-differentiability is necessary but not sufficient — a
continuous, recognizably-trending map (e.g. a smoothly drifting hue) still leaks.

This is the **parameter-space twin** of the leaf-area brittleness/avalanche target (see the
brittle-mapping issue): there, *bit-flips → leaf-area mismatch*; here, *θ-perturbations →
appearance decorrelation*. As a design criterion it is **global**: it defeats the entire
recognition-guided attack class along every axis at once.

### Approach (b): perceptual confounding / non-identifiability — *kill the attribution*

The signal may remain monotone, yet the attack still fails if the map `θ → aspects` is
**rank-deficient or ill-conditioned in the MSBs**: several parameters push the same perceptual
aspect the same way, so feedback is informative about a *combination* of axes but not about *which*
axis moved. The attacker then faces an **underdetermined inverse problem** — many θ explain the
observations — even with perfectly monotone per-combination gradients. The per-axis decomposition
that made the attack cheap no longer exists.

- **Target the MSBs.** `Π*` is an MSB-precision quantity, so confounding is only valuable where it
  is **concentrated in the most-significant bits** of the confounded parameters — exactly where the
  attacker must operate. Confounding in the low bits is nearly worthless.
- **Load-bearing caveat — perceptual non-identifiability *without* derivational non-identifiability.**
  This is safe *only because the legitimate user never recovers θ by perception* — legitimacy comes
  from the memory-hard derivation; the attacker is the sole party reading θ off appearance. The map
  `θ → KDF-output` must therefore stay **injective exactly where `θ → appearance` goes degenerate**:
  *appearance is a lossy function of θ; the KDF is not.* If the perceptual confounding reflects a
  true substrate symmetry that the **derivation also collapses**, those θ become an equivalence
  class and the redundancy **destroys entropy** rather than hardening. This is the precise sense of
  one-wayness here, and the line between "good confounding" and lost entropy.
- **Coverage — additive, not a replacement.** Partial confounding ("a few" parameters) raises cost
  only on the confounded subset; un-confounded axes stay attackable by independent bisection. So (b)
  is **complementary hardening** layered on (a), and rises to a co-equal *global* defense only when
  the confounded subset covers enough of the `Π*` budget to push channel capacity below `Π*`.

### Approach (c): sheer parameter count — *inflate the cost*

Independently of the map's shape, a **sufficiently large number of independent parameters** raises
the cost of the perceptual attack on two fronts, even granting the attacker the best case (clean,
decoupled per-axis querying):

- **(c1) Learning the map is infeasible.** Accumulating enough operational, practical knowledge of
  *parameter → effect-on-aspect* to query efficiently becomes intractable when the parameter count
  is large enough — plausibly even for AI-assisted attackers, since the relation must be learned
  across a high-dimensional space with no exploitable per-axis structure (see (a), (b)).
- **(c2) Even the worst case is too slow.** Suppose decoupled per-axis querying *is* feasible
  (the defender's worst case). With enough parameters, the search `≈ n · log₂(1/res)` is simply
  **too long to run** — the cost scales with `n`, so a large `n` is itself a wall.

This is the most direct reading of the slogan: *finding the haystack in the barn is far harder than
finding the needle in the haystack*, because the barn has so many dimensions that traversing it
under the perceptual oracle is intractable.

**What the defender actually pays (the cost ceiling).** The cost of *deriving* θ does **not** grow
with the parameter count `n`: all parameters are read off the **memory- and iteration-hard hash of
the previous needles** (Argon2 → SHA-256), so adding a parameter just consumes a few more hash-output
bytes — effectively free. The real cost the honest user pays is the **fractal rendering** (the
escape-time evaluation the user must perceive). Therefore the **size of the barn — and the marginal
cost of each extra parameter — is bounded by the cost of fractal rendering**, and that ceiling is
what keeps runtime performance acceptable. *(Takeaway: revisit the brainstorm of candidate parameters
under this lens — `n` can grow freely on the derivation side; the binding constraint is each
parameter's marginal cost in the **render** loop, not in the hash.)*

**Priority + hard requirement.** The **objective** above is the central property to **formalize
first** and a **must-have for the final design**: a substrate/parameterization whose perceptual
oracle admits *any* recognition-guided narrowing of θ toward `Π*` is rejected, regardless of its
other merits. Candidate formalization routes — (i)–(iii) target approach (a) (the *signal*); (iv)
targets approach (b) (the *attribution*); (c) is a quantitative cost/scaling argument rather than a
property of the map's shape:
(i) bound the mutual information between a *resolvable* θ-perturbation and any perceptual similarity
judgement; (ii) require perceptual similarity to be *non-monotone* along every parameter axis at the
secret's resolution; (iii) an indistinguishability game — given two θ within one resolution step, no
recognition oracle does better than chance at *ordering* them by closeness to the secret; (iv)
require the `θ → aspect` map to be **non-identifiable in the MSBs** — bound the conditioning/rank of
its Jacobian (or show its high-order inverse problem is underdetermined) so no oracle can *attribute*
an observed change to a single axis, while requiring `θ → KDF-output` to remain injective there.

## Candidate parameter families (EXPLORATORY — brainstorm, not validated)

> **Certainty disclaimer.** This whole section is a **design brainstorm**. None of the
> effectiveness claims below are empirically validated; every "good for (a)/(b)/(c)" is an
> *analytical conjecture* pending the acceptance test stated next. Tags: **[given]** = follows
> from the existing substrate/already implemented; **[reasoned]** = argued but unverified;
> **[speculative]** = plausible, weakly argued; **[deferred]** = do not build before screening.

**Baseline substrate (for reference).** `z_{n+1} = (|Re z| + i|Im z|)² + c`, orbit seed `z₀ = o`,
already carrying **`p`** (degree-0 additive term, baseline `2⁻³`) and **`q`** (degree-1 `εz` term,
baseline `2⁻⁵`). New families are perturbations/extensions of this map. *(Source: `great-wall-core/DESIGN.md`.)*

**Shared acceptance gate (the frontier).** [reasoned] Every "more sensitive dynamics" family trades
**decorrelation/brittleness** (approach (a)) against **island survival** — the bijection and human
perception both require escape-time level sets that form **connected, discoverable islands ≥ escape
20** (cf. the "chaotic, unconnectable singletons" failure in `DESIGN.md`). The design objective for
any family is therefore *"maximally decorrelating **subject to** islands surviving."* **Acceptance
test (unrun):** sweep each parameter and confirm (1) connected islands ≥ 20 survive, **and** (2)
gross appearance does **not** drift monotonically under the sweep. Until run, all rankings are
provisional.

**Cost ceiling (settled).** [given] Deriving parameters is free (bytes off the Argon2/SHA hash of
prior needles); the binding cost is each parameter's **marginal cost in the render loop** (see
approach (c)). All families below are cheap on that axis unless noted.

### Lead candidates (favor approach (a), the must-have)

- **History-dependent fold center** — `a(n)=Re(z_{n-k})`, `b(n)=Im(z_{n-k})`: fold about a *moving,
  orbit-dependent* axis (`|Re z − a(n)|`, `|Im z − b(n)|`). [reasoned] **Best-of-class candidate, but
  unscreened.** Rationale: perturbs the *structural* element (the abs-fold crease that gives the
  Burning Ship its character) rather than injecting additive energy; the fold is **magnitude-bounded**
  (abs never amplifies), so it stays inside the fold-map family empirically known to produce islands
  → lowest island-destruction risk among the dynamic families. *Caveat:* still capable of
  destabilizing; `k` and any gain need bounding; not yet tested against the gate.
- **Static fold-axis offsets** — `|Re z − a|`, `|Im z − b|`, constants `a,b`. [reasoned] The Burning
  Ship's identity *is* the fold about 0; relocating the crease changes dynamics **discontinuously**
  where signs flip → strong (a). Cheap (two subtractions). *Caveat:* effect may be locally smooth
  away from sign-flip loci — needs the monotonicity check.
- **Pre-square linear map** — rotate/shear `z` (angle φ / shear) before the abs-square. [reasoned]
  The abs-fold is **not** rotation-invariant, so small φ restructures the fractal nonlinearly → strong
  (a). Cheap (2–4 muls). *Caveat:* unverified that the restructuring is non-monotone in φ.

### Count / confounding multipliers (favor (c), some (b))

- **Bit-gated per-iteration mask** — `… + g·s(n)`, `s(n) ∈ {0,1}` a fixed mask from the hash.
  [reasoned] **Structurally better for (a) than analytic coefficients**: discrete (no slider to
  descend), and an early-orbit flip **avalanches**, so appearance-similarity does not track Hamming
  distance to the secret → defeats Hamming-bisection. Near-free render cost; large `L` ⇒ many
  parameters (strong (c)). **Load-bearing caveat (real, not benign):** late / post-escape bits can be
  **derivationally degenerate** (many `s` → same escape tree) — that is *entropy loss*, not mere
  perceptual confounding. *Mitigation:* cap the gated window to the **active** iteration band
  (~20…`max_iter`). Strong candidate if so bounded.
- **Polynomial perturbation** — `Σ_{i=0}^{d} p_i z^i`, evaluated via Horner. [reasoned] **Natural
  unification** of the existing `p` (`i=0`) and `q` (`i=1`); cheap (render cost linear in `d`); near
  the set `|z|=O(1)` so terms overlap → natural **(b) confounding** in the MSBs, with the escape tree
  still separating them (caveat satisfied *if* not derivationally degenerate). **Weak for (a):**
  analytic in the coefficients → risks the "smoothly drifting gross appearance" leak the criterion
  forbids → **do not rely on it for (a)**. **Constraints:** coefficient baselines must **shrink
  geometrically with degree** (continuing `2⁻³, 2⁻⁵, …`) or the `z²` carrier (coefficient 1) is
  swamped and islands die; the family **saturates ~`d = 3–4`**.
- **Iteration-periodic table** — additive/linear term cycles through a period-`k` constant table by
  iteration index. [reasoned] Cheap (`(c)` multiplier by `k`); the bit-gated mask is its binary,
  avalanche-favoring specialization. *Caveat:* same degeneracy watch as the mask.

### Coarse / discrete selectors (low entropy, maximal decorrelation)

- **Structural toggles** — bits choosing: abs on Re-only / Im-only / both / neither; conjugate `z`;
  swap Re↔Im; sign flips. [reasoned] Each toggle ⇒ a *completely different* fractal → maximal (a) but
  coarse and **low-entropy** (a few bits). A cheap "family selector" layer.
- **Carrier exponent `d`** — iterate `(|Re z| + i|Im z|)^d` instead of the square. [reasoned] Drastic
  lobe/symmetry change → very decorrelating but **coarse, low-entropy**, raises overflow rate and
  render cost (∝ `d`). Coarse selector only.

### Deferred / discouraged (screen before building)

- **Linear delay feedback** — `… + Σ_k w_k z_{n-k}`. [deferred] More parameters, natural confounding,
  but a **hard stability constraint**: the linear recurrence's spectral radius must stay `< 1` or the
  orbit diverges and the fractal collapses → small, stability-bounded `w_k` only. Medium value / medium
  risk; screen first.
- **Nonlinear / cross-history terms** — `z_n · z_{n-k}`, or `|z_{n-k}|` modulating the fold gain.
  [deferred] Strongest decorrelation but **highest blow-up / island-fragmentation risk** (degree-2 in
  state). High risk/reward — behind the island-survival screen.
- **History-dependent escape criterion** — escape on a running functional (e.g. `Σ|z_{n-k}|`
  overflow, moving average). [deferred] Likely **smooth** in its threshold params → weak on (a), and
  abandons the clean "overflow = escape" property. Low priority.
- **Finite escape radius `R` as a parameter.** [discouraged] Smooth in `R` → weak on (a); trades away
  the overflow-escape elegance. Skip unless independently motivated.

### Provisional shape of a final parameterization
[speculative] **Decorrelating backbone** = static + history-dependent fold (offsets, pre-square map)
for the must-have (a); **count/confounding** = bit-gated mask + polynomial family for (b)/(c);
**coarse selectors** = structural toggles / exponent. No single family is asked to do a job it is bad
at — notably, the polynomial family is the confounding/count contributor, **not** the (a) defense.
All contingent on the acceptance gate.

## Ties to the proposal
- `ρ` → entropy-density metric (**OE3a**).
- `Ā(e)`, `Π(e)`, `Π*` → substrate-adequacy criteria + the inverse-problem / one-wayness oracle
  bound (**OE4**); `Π(e)` is the rigorous form of "minimum MSBs for the area-tree to match with
  probability `p`" already stated there.
- Perceptual non-ascertainability of θ → an **OE4** substrate-design criterion (with the
  brittle-mapping target), via three approaches: (a) decorrelation/non-monotonicity, (b)
  confounding/non-identifiability in the MSBs, and (c) sheer parameter count (cost inflation).

## Naming (provisional — open to change)
| Tag | Name | Symbol |
|-----|------|--------|
| Rzb | bit–area contraction law | `ρ` |
| Rez | island-area law | `Ā(e)` |
| Rpe | parameter-precision threshold | `Π(e)` |
| —   | labyrinth-description complexity | `Π*` |
| —   | perceptual non-ascertainability of θ (objective) | criterion |
| —   | ↳ (a) decorrelation / non-monotonicity (θ → appearance) | approach |
| —   | ↳ (b) confounding / non-identifiability in MSBs | approach |
| —   | ↳ (c) sheer parameter count (cost inflation) | approach |
