# A memorization-free, precomputation-resistant salt from the Bitcoin timechain

> **Paper skeleton (draft).** Academic write-up of the primitive specified in
> [`../next-steps/bitcoin-nonce-salt.md`](../next-steps/bitcoin-nonce-salt.md).
> Target: a short paper / workshop submission; also the technical core of the HRF
> spin-off. Structure below is a scaffold — prose to be expanded, results are final.

## Abstract (draft)

Salts defeat *precomputation* — rainbow tables and cross-target amortization — but a
salt that is itself recovery-critical faces a bootstrapping problem: it must be
**reproducible** by a user (and heirs) with minimal stored state, yet **unpredictable
in advance** and **unique per user**. We show that a salt derived from Bitcoin block
headers at a **user-memorable date** meets all three. The user memorizes only a date;
the salt is reconstructed from the public timechain. Under a standard random-oracle
assumption on SHA-256, the winning header of a future block is computationally
unpredictable (Lemma), so no table precomputed before the date can contain the salt,
and per-user date-keying makes tables non-amortizable across targets. The salt is
**public** (not secret) — precomputation defense, not confidentiality, is its remit —
and inherits the timechain's decentralized availability and proof-of-work integrity,
making it uniquely suited to **decades-horizon recovery**. We situate the primitive
against prior "Bitcoin-as-randomness-beacon" work and show that the beacon literature's
central caveat — miner **manipulability** of block entropy — does *not* affect the salt
use case, because a pre-dated block predates any targeting and a salt requires
unpredictability-before, not unbiasability.

## 1. Introduction

- The precomputation threat to KDF salts; why a *public* salt suffices (salts are not
  secret).
- The *recovery-critical* twist: the salt must survive decades and be reproducible from
  near-zero memorized state — rules out random per-user salts stored only on a device.
- Contribution: a date-keyed timechain salt; three formal properties; the manipulability
  non-issue; a reference implementation — **Namtso — the Sacred Salt**
  ([`../next-steps/namtso-app-and-api.md`](../next-steps/namtso-app-and-api.md)).

## 2. Background

- Salts, rainbow tables, amortized precomputation; memory-hard KDFs (Argon2).
- Bitcoin headers, proof-of-work, difficulty, median-time-past; header fields (nonce,
  merkle, timestamp, version) and their distributions.
- Public randomness beacons (NIST beacon; drand / League of Entropy) and their trust /
  availability models — contrast with a permissionless, archival source.

## 3. Construction

- Date `d` → deterministic block `B(d)` via **median-time-past** (consensus-defined,
  reorg-stable); a *past* date is deeply buried ⇒ no reorg ambiguity.
- Window `w` of headers → `σ = XOF₁₀₂₄(headers)`; `≥ 1 Kb`, greedy-for-good-measure.
- **Whitening** and the nonce-vs-digest distinction (nonce ≈ uniform but thin; digest
  high-bits fixed by difficulty; timestamp low-entropy) — hash full headers, slice
  nothing raw.
- Reproducibility contract: exact serialization, endianness, block-selection rule.

## 4. Security

- **A1 (random-oracle heuristic on SHA-256 / nonce-search optimality)** — assumption,
  with the economic-dominance argument as *corroboration*, not proof.
- **Lemma N1 (block unpredictability).** Min-entropy `≥ β` of block `N+1`'s header given
  the chain at `t_N`.
- **Corollary N2 (no pre-dated table).** Precomputation before `t_{B(d)}` cannot contain
  `σ`.
- **Corollary N3 (non-amortization).** Per-user `d` ⇒ per-target salt ⇒ tables don't
  amortize.
- **Manipulability is a non-issue here.** Prior work (Pierrot–Wesolowski, *Malleability
  of the blockchain's entropy*, 2016) shows a miner can bias/withhold to skew
  block-derived randomness. This does **not** affect the salt because: (a) the block
  **predates** the user's setup and any targeting — a miner years earlier had neither
  motive nor ability to aim at this user's future salt; and (b) a salt needs
  *unpredictability-before-`d`* and *uniqueness*, **not unbiasability** — a miner-skewed
  block is still unpredictable to a pre-dated table-builder. (Full-entropy beacons, by
  contrast, *do* need unbiasability — hence the gap in applicability.)
- `σ` is **public**; threat model is precomputation, not confidentiality; `d` is
  guessable and that is fine.

## 5. Properties (why it's an unusually good salt)

1. **Relatable to a cheap memorized datum** — a date the user already holds.
2. **Unsurpassable availability + PoW integrity** — recomputable from any archive,
   forever; the block at `d` is immutable and unforgeable retroactively.
3. **Cheap enough to be greedy** — `1000×` a salt's need is as cheap as the minimum.

## 6. Related work

- Bonneau–Clark–Goldfeder, *On Bitcoin as a public randomness source* (2015).
- Bentov–Gabizon–Zuckerman, *Bitcoin beacon* (2016).
- Pierrot–Wesolowski, *Malleability of the blockchain's entropy* (2016) — the
  manipulability result we neutralize for this use case.
- Randomness beacons: NIST; drand / League of Entropy.
- **Positioning / novelty.** "Bitcoin as public randomness" is *known*, and *known to be
  manipulable*. Our contribution is the **salt** application, in which manipulability is
  irrelevant, plus (i) **memorization-free date-keying**, (ii) the **unpredictability-
  before-`d`** and **non-amortization** corollaries as the exact properties a
  precomputation-resistant salt needs, and (iii) a **recovery-grade** availability /
  integrity argument for decades-horizon self-custody. Modest but crisp.

## 7. Applications

- Bootstrapping self-custody KDFs (Great Wall: retires the tacit "canonical stage"
  pepper; see [`../next-steps/bitcoin-nonce-salt.md`](../next-steps/bitcoin-nonce-salt.md)).
- General password/KDF salting where the salt must be reproducible without stored state.
- Inheritance / dead-man recovery, where heirs hold only a date.

## 8. Limitations

- Recovery requires **chain-history retrieval** (a node or archive) at recovery time.
- `d` is low-entropy / guessable — *by design* (salt, not secret); do not over-claim.
- Assumes SHA-256 preimage resistance and honest MTP timestamps within consensus bounds.

## 9. Conclusion

A date is the cheapest thing a human can carry; the timechain is the most durable public
record we have. Binding them yields a salt that is reproducible, unpredictable-in-advance,
per-user, and recovery-grade — with the beacon literature's manipulability caveat
designed around rather than inherited.

---

### Open items for the full draft
- Concrete `β` lower bound (min-entropy per block from the nonce alone; whitened window).
- Exact serialization spec + test vectors (shared with the reference implementation).
- Empirical nonce-distribution note (search-pattern structure; why whitening suffices).
- Venue: workshop (e.g. a Financial Crypto / S&P workshop) vs. eprint-first.
