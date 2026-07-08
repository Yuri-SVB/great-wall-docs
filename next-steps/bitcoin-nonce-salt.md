# Bitcoin-nonce salt — a memorization-free, precomputation-resistant salt

> Formal result + design note. A **public, per-user** salt derived from Bitcoin
> block data at a user-memorable date. It supplies the *anti-precomputation* role
> of a pepper **without being secret or a memorization burden**, letting the setup
> retire the tacit "canonical stage" pepper. Spun out as **Namtso — the Sacred Salt**
> (spec: [`namtso-app-and-api.md`](namtso-app-and-api.md); MVP in development). Referenced by
> [`../great-wallet/THREAT_MODEL.md`](../great-wallet/THREAT_MODEL.md) and
> [`cpnf-lifecycle-and-deck.md`](cpnf-lifecycle-and-deck.md).

## Construction

The user chooses a **memorable date `d`** (e.g. their last birthday before setup).
Deterministic block selection: `B(d)` = the first block whose **median-time-past**
`≥ 00:00 UTC(d)` (MTP is consensus-defined and reorg-stable). Over a window of `w`
consecutive headers — sized so the window carries **≥ 1 Kb = 1024 bits** of
unpredictable material (`w ≈ 32`, i.e. ~32 nonces × 32 bits; fewer if counting
full-header unpredictability):

```
σ = XOF₁₀₂₄( header(B(d)) ‖ header(B(d)+1) ‖ … ‖ header(B(d)+w−1) )
```

`XOF₁₀₂₄` (SHAKE256, or a 128-byte KDF output) **whitens** the material and aggregates
**≥ 1024 bits**. `1 Kb` is deliberately **far beyond** the ~128 bits a salt needs — it
is *greedy for good measure* at ~zero cost (property 3 below), so no conceivable
precomputation or collision concern survives. (Since `σ` then feeds `Argon2d^D(σ)`, the
memory-hard absorb whitens it regardless; the explicit XOF just fixes a reproducible
`σ` value.)
`σ` is **public** and recomputable by anyone holding `d` and chain access. (The name
"nonce" honors the nonce as the *emblem* of a block's unpredictability under Lemma N1;
the salt in fact whitens the **full headers** — nonce plus every other field no one
could predict before the block was found — so the result never depends on any single
field's distribution. See the whitening caveat.)

## Formal results

**Assumption A1 (nonce-search optimality — random-oracle heuristic on SHA-256).**
For difficulty target `T`, finding a header `h` with `SHA256²(h) < T` admits no
algorithm asymptotically better than brute force (`~2²⁵⁶ / T` evaluations).
- *Corroboration (evidence, not proof):* a miner holding a sub-brute-force method
  would accrue unbounded expected advantage and come to dominate hashrate; the
  observed prevalence of brute-force mining is evidence against its existence.
- *Foundation:* preimage resistance of SHA-256.

**Lemma N1 (block unpredictability).** Under A1, conditioned on the entire public
chain at time `t_N` (discovery of block `N`), the winning header of block `N+1` —
hence its hash — has min-entropy `≥ β > 0`: it is **computationally unpredictable
at `t_N`**.

**Corollary N2 (no pre-dated table).** No precomputation built at any time
`≤ t_{B(d)−1}` can contain `σ` — it is computationally unpredictable before `B(d)`
is mined.

**Corollary N3 (no amortization / per-user uniqueness).** Keying `d` to a per-user
datum (birthday; birth-*hour* in advanced/tin-foil mode) makes `σ` w.h.p. distinct
across users, so a table built for one user's `σ` gives negligible advantage
against another — **precomputation cannot be amortized across targets.**

## Consequence — the salt replaces the pepper

`σ` performs the pepper's anti-precomputation function while being **public and
memorization-free**: the user recalls only `d`, and the app reconstructs `σ` from
the chain. Therefore `σ` is **not a coercion target**, needs **no tacit "canonical
stage,"** and imposes **no memorization budget**. It is *not secret* — a targeted
attacker who knows `d` recomputes it — but secrecy was never the salt's job;
N2 (unpredictability-before-`d`) and N3 (non-amortizability) are exactly its remit.

## Why this is an unusually good salt

Three properties make the block-salt not merely adequate but *excellent* — and are
why this is the one place in the design where we can afford to be greedy:

1. **Trivially relatable to a cheap memorization datum.** The user memorizes only a
   **date** — a birthday they already hold — and the app recovers all of `σ` from it.
   Near-zero memorization cost for arbitrarily much salt entropy.
2. **Unsurpassable availability and integrity.** The Bitcoin chain is the most
   replicated, most tamper-evident public dataset in existence: `σ` is recomputable
   from any full node or archive, and the historical block at `d` is **PoW-immutable**
   — its integrity is settled and cannot be retroactively forged. No centralized
   randomness beacon matches this combination of decentralized **availability** +
   durable **integrity** + a decades-long history. (Availability at recovery depends
   only on chain-history retrieval — about as durable as public data gets; the blocks
   persist in archives even in Bitcoin's tail cases, and past PoW is immutable
   regardless of the chain's future.)
3. **Cheap enough to be greedy.** Gathering entropy is a handful of block lookups;
   taking `1000×` what a salt needs is as cheap as taking the minimum. Hence the `1 Kb`
   target — round, generous, and free.

## Engineering caveats

- **Whitening is mandatory — but *not* because the nonce is strongly biased.** Keep
  the fields straight: the header **nonce** is only **32 bits** and *approximately
  uniform* (the winning nonce's position within a swept range is ~uniform — it is
  high-entropy, just thin; the only skew is *weak* search-pattern structure by
  pool/hardware); the block **digest** is the field whose **leading bits are fixed by
  difficulty** (below-target ⇒ ~top-80 bits ≈ 0, only the low ~176 uniform); the
  **timestamp** is genuinely low-entropy (tracks wall-clock). So the hazards are (a)
  **thinness** — one nonce is 32 bits, so several blocks are needed — and (b) **mixing
  fields of unlike distributions**, *not* a biased nonce. The robust,
  distribution-agnostic fix is to derive `σ` by **hashing a window of full headers**
  (SHA-256 / the KDF whitens to uniform and aggregates ≥256 bits) — never slice raw
  bits of any single field as if uniform.
- **Deterministic selection + reorg safety.** Pin the `d → B(d)` rule (MTP-based); a
  *past* birthday is months-deep, so there is no reorg risk and `σ` reproduces
  **bit-exactly at recovery** decades later.
- **Recovery dependency.** Reproducing `σ` requires access to historical Bitcoin
  headers at recovery (a node or archival explorer) — acceptable for a
  Bitcoin-centric product; state it in the manual.
- **Date guessability is fine.** `d` is low-entropy and guessable; this does **not**
  weaken N2/N3 (a salt is public). Do not treat `d` as secret entropy.
