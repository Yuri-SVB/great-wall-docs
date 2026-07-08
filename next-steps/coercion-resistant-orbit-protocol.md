# The coercion-resistant orbit protocol (canonical spec)

> **Status: canonical redesign.** This supersedes the post-graduation cryptography
> scattered across [`post-graduation-security-tiers.md`](post-graduation-security-tiers.md)
> (§6 block-orbit / `64*` floor / deep-master-block) and
> [`cpnf-lifecycle-and-deck.md`](cpnf-lifecycle-and-deck.md) §2 (orbit / accretion) —
> those remain as design history; this doc is the single source of truth for the
> orbit, the master secret, and the coercion argument. Threat-model lemmas live in
> [`../great-wallet/THREAT_MODEL.md`](../great-wallet/THREAT_MODEL.md); the stage-0
> salt is [`bitcoin-nonce-salt.md`](bitcoin-nonce-salt.md) (Namtso).
>
> Normative keywords per RFC 2119. Frozen-parameter changes bump the protocol version.

## 1. Definitions

| Symbol | Meaning |
|---|---|
| `H(·)` | a **cheap** one-way hash, assumed **not** to collapse entropy. |
| `H*(·)` | a **memory-hard** hash (Argon2-class), tunable cost, non-entropy-collapsing. |
| `N` | number of **deep** (non-zero) stages. |
| `σ` | the **Namtso** salt — public, precomputation-ruling-out, cross-user amortization ≈ 0. |
| `o₀` | `:= H(σ)` — orbit point of stage 0. |
| `theta_i_j` | `:= H(o_i ‖ j)` — parameter vector of **fractal `j` of stage `i`**. |
| `p_i_j` | `j`-th point of stage `i`: a **32-bit** leaf-area of fractal `theta_i_j`. |
| `Sh_i` | the **full Shamir polynomial** (degree `t_i−1`) reconstructed from any `t_i` of `s_i` points — **`t_i·32` bits**, `t_i ≥ 2`. *Not* the constant term. |
| `o_i` (i>0) | `:= H*( H( o_{i−1} ‖ Sh_{i−1} ) )` — the orbit advance. |
| `K` | master secret `:= H( o_N ‖ Sh_N )` — **cheap `H`**, deliberately (see §5). |
| `TLP(·)` | RSW time-lock-puzzle encryption. |

**Shamir abscissa convention.** The `t_i` primary shares sit at **positive** abscissae;
opt-in ad-hoc `(s_i − t_i)` forgetting-resistance shares sit at **negative** abscissae.
Extra `(s_i − t_i)` shares strengthen hard-derivation against forgetting; they do **not**
change `Sh_i`'s entropy (still `t_i·32`).

**Why the nested `H*(H(·))`.** Computing `c := H(o_{i−1} ‖ Sh_{i−1})` first (instant),
**wiping `{o_{i−1}, Sh_{i−1}}`**, then running the long `o_i := H*(c)`, means the raw prior
orbit point and Shamir secret exist only for an instant — not across the whole memory-hard
window. This directly shrinks K's seizability window (design goal 1) and is the reason not
to write `H*(o_{i−1} ‖ Sh_{i−1})` directly.

## 2. Threat model

1. **Kerckhoffs** — the attacker knows the protocol *and the victim's setup topology*.
2. **Dolev-Yao** — the attacker sees all on-the-wire plaintext/ciphertext but cannot
   decipher beyond its capabilities.
3. **NNPL** (Non-Negative-Proof Lemma) — no agent can prove *non*-knowledge/access.
4. **DRL** (Deadly-Race Lemma) — an attacker willing to coerce is willing to **assassinate
   racers** to `K` (subject to the reachability remark, THREAT_MODEL).
5. `H`, `H*` are **preimage-resistant**.
6. `σ` is trivially guessable but **unknowable in advance**; cross-user table amortization
   reduced to an acceptable minimum.
7. **TKBA₁** — `p_i_j` are intransmissible *without* `theta_i_j` (which the attacker knows
   for stages it can render).
8. **TKBA₂** — `theta_i_j` (deep) are not a memorizable artifact the victim can hand over;
   they are regenerated from `o_i`, which requires the chain.
9. **`p_0_j` are seized at any wrench attack** (stage 0 is the always-present, `σ`-public
   entry; assume it compromised).
10. **`32*`** — a `2³²`-element brute-force, *each element costing `H*` or more*, is **within**
    attacker capability.
11. **`64*`** — a `2⁶⁴`-element brute-force, *each costing `H*` or more*, is **beyond** it.

**`H*` calibration (user-tunable).** Choose the per-`H*` cost so that `2³²·H*` sits at the
feasibility edge (TM.10) and `2⁶⁴·H*` is beyond it (TM.11). A **few-minutes** Argon2 barrier
per element also **defeats Grover**: a quantum search would need `~2^{n/2}` *coherent*
evaluations of a memory-hard oracle, which is impractical — so sub-256-bit standards (96/128)
are quantum-defensible without a 256-bit seed. The *whole orbit* is calibrated to hours-to-week.

**Softest number (must be named, per TM).** TM.11 stipulates only that `2⁶⁴·H*` is infeasible.
The **cheap** `2⁶⁴` (ledger brute of a 64-bit `K`, `H` not `H*`) is the softest quantity in the
model — resourced-attacker-borderline (~hours). It appears in exactly two places: the **Setup-1
post-wrench floor** (§6) and the **residual-window endgame** for Setups > 1 (§9). It is tolerated
inside the residual reasoning, not claimed flatly infeasible.

## 3. The orbit

```
o₀   = H(σ)
o_i  = H*( H( o_{i−1} ‖ Sh_{i−1} ) )              # wipe {o_{i−1}, Sh_{i−1}} before the H*
```

Each link **absorbs a whole stage** (`Sh_{i−1}`, `t_{i−1}·32 ≥ 64` bits). Consequences:

- **No single-point oracle.** The smallest thing any orbit link commits is a full stage
  (`≥ 64` bits), so no individual `p_i_j` is ever checkable alone — this is the block-orbit
  `k ≥ 2` condition, realized as Shamir `t_i ≥ 2` per stage.
- **Forward-only.** `H*`/`H` preimage resistance ⇒ a seized `o_i` cannot yield `o_{i−1}`.
- **Chain-brute cost.** From a seized `o_i`, reaching `K` requires guessing `Sh_i … Sh_N`;
  each `Sh_j` guess is `2^{t_j·32}` and is `H*`-gated (checked by recomputing the link). So
  from any `o_i` with `i ≤ N`, `K` is `2^{Σ_{j≥i} t_j·32}` — `≥ 2⁶⁴·H*` for every `i ≤ N`
  under the standard build (see §6).
- **Stored-orbit safety, with a caveat.** Because each link is `≥ 64*`, exposing the *whole*
  `{o_i}` still leaves every stage `≥ 64*` against offline reconstruction — **no extra sealing
  needed**. **But** `o_i → theta_i_j` renders *every board of stage `i`*, making that stage's
  points **immediately coercible** at a wrench attack (no stage-by-stage derivation required).
  So a stored orbit is *offline-safe* yet *coercion-accelerating* — it MUST stay **TLP-gated /
  guarded**, never plaintext at rest.

## 4. Fractals and points

`theta_i_j = H(o_i ‖ j)` gives fractal `j`'s parameters; `p_i_j` is a 32-bit leaf-area on it.
Multiple fractals per stage (indexed `j`) let a stage carry `t_i·32` bits at **lower zoom
depth per board** (a *shallow zoom* — distinct from the "shallow **stage**" = stage 0
sense; here it is only about how far a single board is zoomed). That yields

1. **Granularity:** 64, 96, 128… — stage entropy tunable in 32-bit steps.
2. **Gradual extendability:** memorizing one more point buys a security-property
   upgrade (as in the Setup 1 → 2 transition).
3. **Cheap memorization forgiveness:** three shallow-zoom (32-bit) points for an
   above-64-bit standard — equivalent to 96 tacit bits memorized — rather than two
   deep-zoom (64-bit) points equivalent to a 128-bit minimum.
4. **Multiplies the tacitness hardness of `theta_i_j`:** more fractals to describe.

## 5. Master secret

```
K = H( o_N ‖ Sh_N )        # cheap H, by design
```

**Why cheap, not `H*`.** A memory-hard last step would *prolong* the window in which `o_N` and
the last points are live (you'd pay an `H*` *after* the final point) — worsening goal 1. Instead
the resistance lives in **entropy**: standard non-0 stages carry **96 bits** (`t=3`), so the
cheap ledger brute of `Sh_N` from a bare `o_N` is `2⁹⁶` — infeasible — *and* the window stays
instant. (Making the step `H*` was considered and rejected: it buys nothing `96`-bit entropy
doesn't already buy, and it costs window length.)

## 6. Entropy accounting & floors

| | stage-0 | non-0 stage (Setup 1) | non-0 stage (Setup ≥ 2) |
|---|---|---|---|
| points | 2 | 2 | 3 |
| `t_i` | 2 | 2 | 3 |
| `Sh_i` | 64 b (assumed seized, TM.9) | 64 b | **96 b** |

- **Pure device seizure** (no coercion; nothing at rest but TLP-gated blobs) ⇒ `K` unreachable
  (all tacit points required).
- **Wrench seizure of `p_0`** ⇒ attacker computes `o_1` (one `H*`). From `o_1`, `K` is
  `2^{Σ_{j≥1} t_j·32}`: **Setup 1** (`N=1`, 64-bit) ⇒ `2⁶⁴` (the accepted bare-minimum floor,
  *cheap* — the softest number); **Setup ≥ 2** ⇒ `≥ 2⁹⁶`.
- **Mid-chain seizure at `o_i`** (`i ≤ N`) ⇒ `K` is `≥ 2⁹⁶` (standard build) — infeasible.
- **Only exception:** `o_N` present (§9 residual).

**Setup 1 is the 64-bit entry tier**, deliberately low to flatten the adoption curve — a *real*
`2⁶⁴` barrier, **one extra point + a rekey** from Setup 2's 96-bit stage. Even there, "seize
up to `N−1`" = "seize stage 0 alone" still leaves `K` at `2⁶⁴`. Conversely, a slightly greedier
user MAY **skip the entry tier and start at Setup 2** (memorize the first deep stage's third point up front),
economizing on the later Setup 1 → 2 rekey — the tier is an option to lower the barrier, not a
mandatory first rung.

## 7. Setup pathway, level-up, retirement

Progressive builds (each prefix is a valid setup):
```
1.  σ ‖ p0_1 ‖ p0_2 ‖ p1_1 ‖ p1_2                                   (stage 1: 2 pts, 64 b)
2.  … ‖ p1_3                                                        (stage 1: 3 pts, 96 b)
3.  … ‖ p2_1 ‖ p2_2 ‖ p2_3                                          (add deep stage 2)
4.  … ‖ p3_1 ‖ p3_2 ‖ p3_3                                          (add deep stage 3)
```
Extra `(s_i − t_i)` shares (negative abscissae) opt-in per stage for forgetting-resistance.

- **Rekey on every change.** Any orbit change alters `K`; whatever `K` gates MUST be re-keyed
  (move funds) for the update to take effect. So level-up is an on-chain event (rate-limited by
  cost — a feature).
- **Gradual level-up** answers TM.9: a *second* wrench attacker effectively starts at stage 1,
  a third at stage 2, and so on. Aim to memorize **≥ 2 deep levels** so a wrench attack can
  trigger immediate, seamless retirement of the lowest (least-deep) in-use stage.
- **Retirement via the timechain.** To retire compromised lower levels, **bury `o_i` on-chain**,
  making it the de-facto new `σ` for a fresh setup rooted at `o_i`. The attacker already had
  `o_i` (they compromised up to it), so publishing leaks nothing new; cost is a small permanent
  chain artifact (a privacy footprint tied to the event) — acceptable for an emergency lever.

## 8. Forgiving TLP decks (sub-deck construction)

Forgiveness for review/practice is delivered **not** by exposing Shamir shares (that would
re-open a sub-threshold oracle) but by an enumerated, TLP-gated deck. Rules:

1. **Outer vault is `TLP`.**
2. **Inner vaults are key–payload pairs, replicated to exhaustively cover every intended
   `k`-of-`n` combination of points**, subject to:
   1. the **two stage-0 points (or three in-use shallow points) are always included** (always
      seizable — no reason not to deploy them; also lets a deck contemplate stage retirement);
   2. if a payload *plus the points gating it* contains **all-but-≤1** points of some stage
      `i`, then **also include `o_i`** in that payload (otherwise a deadly-race for `o_i`
      arises — the holder would be one coerced point from `o_i` without holding it);
   3. a payload *plus its gating points* **must not trigger a deadly-race** (must leave `K`
      `≥ 64*`);
   4. **(where possible)** a payload *plus its gating points* is **insufficient for `K`** (no
      single sub-deck reconstructs the master).

This is customizable per setup; the rules above are the invariants any customization MUST hold.
*(Intricate — verify this section against intent before implementation.)*

## 9. Residual deadly-race window (tolerated)

A wrench attack that lands with `o_N` **imminently/currently available** and subdues the victim
**before its deletion** can force surrender of the `p_N_j` and thus `K`. Right after the
**second-to-last** `p_N_j`, the attacker (TM.10) already has enough — the last point is a `2³²·H`
brute (cheap `H`, since `K = H(o_N ‖ Sh_N)`) — so a vicious attacker *could* assassinate to save the last ~1 minute. This tiny residual
is tolerated because:

1. A well-trained fractal is retrieved in **~1 minute**.
2. The attacker's plan already budgeted TLP/rederivation + subdue-and-calm + interface time; a
   few minutes rarely changes the escape.
3. Assassinating **trusts** the earlier surrendered points were real — a wrong one, and the
   coercion retry is **burned**.
4. It **dramatically worsens judicial liability** — murder qualified by futile motive *and by the
   victim's defenselessness*, atop armed robbery (cf. robbers who kill cooperating victims).
5. A resourced attacker could pre-stage the `2³²` brute as a "victim-stalls" contingency anyway
   — hence **cheapen the last Shamir-KDF step** (§5) and keep memory/sequential hardness in the
   *orbit*, not the terminal `K`.

**Net:** a tiny window in which the attacker is, far more likely than not, *incentivized not to
act*. The window's exact opening (after `t_N−1` vs `t_N−2` points) rests on the softest number
(§2): whether cheap `2⁶⁴` is out of reach — inside the tolerated reasoning either way.

## 10. Design goals — how they are met

1. **Minimize K's seizability window** — `H*(H(·))` deletion (§1), cheap terminal `K` (§5),
   forward-only orbit (§3).
2. **Minimize K's deadly-race window** — shrunk to §9's endgame; every earlier state is `≥ 64*`.
3. **Gradual level-up** — §7 (progressive builds, retire-via-chain, ≥2-deep target).
4. **Forgiving TLP decks without Shamir exposure** — §8.
5. **Stage-0 entropy = 64** — don't waste memory on the most-exposed stage (TM.9).
6. **Setup 1 = bare-minimum** — 64-bit entry (§6).
7. **Setup ≥ 2 = 96-bit non-0 stages** — TLP decks with ≥ 2 fractals; a wrench seizure still
   leaves each non-0 stage with enough uncompromised fractals to keep re-derivation `≥ 64*`.

## 11. Open items to pin

- **`H*` per-eval target** (a concrete "few minutes"), so TM.10/11 are quantitative.
- **Exact TLP-deck tables** (§8): default `s_i`, which fractals ride each payload, and the
  precise guarantee behind goal-7's "enough uncompromised fractals."
- **TKBA₁/₂** formal statements for the write-up.
- **The softest-number footnote** (§2) carried wherever `2⁶⁴` is invoked.
