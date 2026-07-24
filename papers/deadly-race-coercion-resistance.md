# The Deadly Race: a formal bar for coercion-resistant custody, and a construction that clears it

> **Status: paper skeleton (draft).** Companion publication to
> [`timechain-salt.md`](timechain-salt.md). It lifts the **deadly-race framework** and
> the **orbit construction** out of the design docs into a self-contained argument
> intended for PhD-application / publication use. Normative source material:
> [`../great-wallet/THREAT_MODEL.md`](../great-wallet/THREAT_MODEL.md) (lemmas) and
> [`../next-steps/coercion-resistant-orbit-protocol.md`](../next-steps/coercion-resistant-orbit-protocol.md)
> (construction). Naming for citation: the **Deadly-Race Lemma** (Villas Boas' Lemma)
> and the **No-Gray-Area / Deadly-Race Principle** (Villas Boas' Principle).

## Abstract (draft)

Physical-coercion ("wrench") attacks defeat custody schemes that key-management and
cryptography treat as out of scope. We give a **formal model** of coercion against a
secret-holder and prove that a large class of "graceful" recovery designs — those that
leave a seizure holding a *feasible-but-slower* path to the secret — are **strictly
worse than useless**: they manufacture an incentive to **assassinate** the victim. We
name this the **Deadly Race**, derive it from a single impossibility (you cannot prove
you forgot), and distil a design bar — the **No-Gray-Area Principle** — that a coercion-
resistant scheme must clear. We then present a construction, **Great Wall**, that clears
it for the Bitcoin self-custody setting while keeping custody **individual**, and locate
a shipping alternative (timelock-rescue vaults) precisely: it clears the same bar by the
*other* available route, at the cost of a trusted third party.

## 1. Introduction

- Coercion is the unmodeled attack. Standard threat models (Dolev–Yao, IND-CCA, forward
  secrecy) assume the adversary cannot compel the *holder*. Physical-attack registries
  (`jlopp/physical-bitcoin-attacks`) show that assumption is empirically false for
  bearer assets.
- Contribution: (i) a formal coercion model; (ii) the Deadly-Race impossibility chain;
  (iii) the No-Gray-Area design bar; (iv) a construction that meets it with individual
  custody; (v) a taxonomy that classifies existing designs by *which* clearance route
  they take.

## 2. Model

- **Principals.** Holder `V`, coercer `A`, optional heirs/delegates.
- **Kerckhoffs (premise 0).** `A` knows the protocol, source, `V`'s setup topology, and
  all in-scope parameters; only the protocol secrets are hidden. Every result is proved
  against such an `A`.
- **Capabilities.** `A` is Dolev–Yao on the wire; may seize any device and read all
  state; has unbounded compute within a wall-clock custody window; may coerce `V`
  physically for a bounded duration.
- **Feasibility line (engineering stipulations).** `S1`: `2³²` **cheap** evaluations are
  feasible. `S2`: `2⁶⁴` **memory-hard** evaluations (each an hours-scale Argon2d, written
  `64*`) are infeasible. Corollary: entropy buys `32→64`; **memory-hardness** buys
  `64→64*`; plain cheap `2⁶⁴` sits at the resourced-attacker border and must be named
  wherever invoked (the "softest number").
- **Tacit-knowledge premise (TKBA).** The secret is a set of fractal locations that are
  *recognisable but not transmissible* — `V` cannot dictate them, and later locations do
  not exist until a memory-hard chain is walked. Formalised as TKBA₁ (points
  intransmissible without their fractal parameters) and TKBA₂ (deep fractal parameters
  are not a handoverable artifact; they require the chain).

## 3. The Deadly-Race impossibility chain

State and prove the escalating chain (each follows from the prior):

1. **Non-Negative-Proof Lemma (NNPL).** No agent can furnish verifiable proof of *lack
   of access* to information — neither of having *forgotten* it, nor that *no backup*
   exists. (The negative-knowledge asymmetry: knowledge is provable, non-knowledge is
   not.)
2. **Deadly-Race Lemma (Villas Boas' Lemma), from NNPL.** Because a released `V` cannot
   prove they retain no resumable copy, any seizure that leaves `A` with enough to
   *eventually* reach the secret — however slowly — defines a **race** between `A` and the
   released `V`. The race creates a **material incentive for `A` to assassinate** `V` (and
   heirs) to eliminate the competing racer.
3. **No-Gray-Area Principle (Villas Boas' Principle), from the Lemma.** A coercion-
   resistant protocol must, for a fixed threat model, admit **only** outcomes in which a
   wrench attack **clearly succeeds** or **clearly fails** — never a race. The gray area
   is exactly where the assassination incentive lives.

- **Reachability remark (the remote-racer escape).** The incentive is realizable only
  against a racer `A` can *reach*. Hence two honest ways to clear the Principle: **remove
  the race** (no feasible seizure path — custody stays individual) or **remove `A`'s reach
  over the racer** (a remote delegate — custody becomes shared). This dichotomy is the
  paper's classification axis.

## 4. Construction — Great Wall (clears by removing the race)

- **Orbit.** `o₀ = H(σ)`; `o_i = H*(H(o_{i−1} ‖ Sh_{i−1}))` with the raw inputs **wiped**
  before the memory-hard step. `σ` is a precomputation-resistant timechain salt (Namtso;
  companion paper).
- **No single-point oracle.** Each link absorbs a whole **Shamir polynomial `Sh_i`**
  (`t_i·32 ≥ 64` bits, `t_i ≥ 2`, the *full* polynomial, not `f(0)`), so no individual
  point is ever checkable alone — the block-orbit `k ≥ 2` condition.
- **Tacit multi-fractal stages.** `theta_i_j = H(o_i ‖ j)` gives `s_i` fractals per
  stage; points are recognisable, not transmissible (TKBA), and low zoom depth keeps them
  so.
- **Cheap terminal secret.** `K = H(o_N ‖ Sh_N)` is deliberately cheap — resistance is
  **entropy** (`96`-bit stages), and a memory-hard `K` would only *prolong* the terminal
  seizure window.
- **Theorem (`64*` floor).** From every seizable state, `K` is `≥ 64*` — no single
  seizure leaves it fewer than two memory-hard 32-bit stages away — so a device seizure
  yields *nothing feasible*: **clear failure**, no racer to reach. Prove by case analysis
  over seizable states (pure device; wrench-of-`p₀`; mid-orbit `o_i`; residual `o_N`).
- **Tolerated residual.** The one gray sliver — a wrench landing with `o_N` live — is a
  `2³²·H` window of ~1 minute; §9 of the spec argues (recognition speed, budgeted
  attacker time, cooperation-trust, and *aggravated* judicial liability: murder qualified
  by futile motive **and victim defenselessness**) that `A` is, more likely than not,
  *incentivized not to act*. This is stated honestly as a bounded residual, not zero.

## 5. Classification of existing designs

- **Timelock-rescue vaults (e.g. Rewind Bitcoin).** Spend sits behind a delay with keys
  on the seized device — a *feasible path* — so it is a race; the design clears the
  Principle by putting the winning racer (a **remote delegate**) out of `A`'s reach. A
  legitimate clearance, but the **remote-racer** kind: custody becomes non-individual,
  and the escape *closes* if the delegate is co-located (both problems return).
- **Great Wall** clears by the *other* route: the secret is tacit and never on the
  device, so seizure yields nothing feasible — **custody stays individual**. "Leave no
  race to run" vs. "put the racer out of reach" is the honest comparison.
- (Fill: plausible-deniability / duress-PIN schemes fail Kerckhoffs; Shamir-only
  social-recovery moves reach onto guardians; multisig geography, etc.)

## 6. Quantum note

A few-minutes memory-hard `H*` per element defeats Grover (a search needs `~2^{n/2}`
*coherent* memory-hard evaluations), so sub-256-bit standards (96/128) are quantum-
defensible without a 256-bit seed.

## 7. Limitations & scope

- Adversarial-agent (testator/heir distrust), device side-channels during active recall,
  long-horizon cryptographic erosion, and mass on-chain correlation are out of scope.
- The framework fixes a *bar*; it does not claim Great Wall is the unique construction
  that clears it.

## 8. Conclusion

The Deadly Race turns "graceful degradation" from a virtue into a liability whenever the
degraded state is a *feasible-but-slower* path. The No-Gray-Area Principle is the
resulting design bar, and the orbit construction shows it is achievable with individual
custody.

### Open items for the full draft

- Fully formal statements of NNPL / the Lemma / the Principle with an explicit adversary
  game and a reduction for the `64*` floor.
- Quantitative `H*` per-eval calibration tying `S1`/`S2` to hardware.
- A precise game-based definition of "coercion-resistance" that the Principle implies.
- Empirical grounding of the residual-window argument against the wrench-attack registry.
