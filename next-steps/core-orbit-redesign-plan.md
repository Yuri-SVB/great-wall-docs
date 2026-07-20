# great-wall-core — orbit-protocol redesign plan (`0.3.0 → 0.4.0`)

> **Status: planning.** This maps the delta from the shipping chained protocol
> (`PROTOCOL_VERSION 0.3.0`, [`../great-wall-core/DESIGN.md`](../great-wall-core/DESIGN.md))
> to the canonical **orbit** protocol
> ([`coercion-resistant-orbit-protocol.md`](coercion-resistant-orbit-protocol.md)).
> It is a **hard, backward-incompatible** move — `0.3.0` encodings do not
> round-trip across it — so it lands as `PROTOCOL_VERSION 0.4.0` ("orbit"). The
> canonical spec is the source of truth for *what*; this doc is the source of
> truth for *how the engine changes*. No code here yet — it exists to be
> stress-tested before implementation.

## 0. One-paragraph delta

`0.3.0` is a **single chain of single-fractal stages**: stage 0 is a text label,
each later stage derives **one** `(o,p,q)` fractal by `SHA-256(Argon2^N(stage-0 text
‖ preceding points))` and carries **one** 32-bit point, and the master secret is an
`Argon2id` pass over the whole transcript. `0.4.0` keeps the fractal-encoding
substrate (I4F60, Burning Ship, island discovery, bisection — **unchanged**,
`ENGINE_VERSION` stays put) but rebuilds the **chain** into an **orbit** with four
structural additions: (1) the root is the **Namtso salt `σ`**, not free text; (2) each
stage carries **`s_i` fractals** (`theta_i_j = H(o_i ‖ j)`), not one; (3) a stage's
contribution to the chain is a **Shamir polynomial `Sh_i`** over its points, not their
raw concatenation; (4) the orbit advance is the **wiped nested `o_i = H*(H(o_{i−1} ‖
Sh_{i−1}))`** and the master secret is the **cheap `K = H(o_N ‖ Sh_N)`**.

## 1. What stays (do not touch)

The determinism-critical substrate is orthogonal to the orbit change and MUST NOT
regress:

- I4F60 fixed-point (`fixed.rs`), Burning Ship iteration (`fractal.rs`), island
  discovery (`discovery.rs`), the bisection tree encode/decode (`bisect.rs`),
  `BITS_PER_POINT = 32`, `ENCODE_MAX_ITER = 1024`, the encode area, the render cache.
- Therefore **`ENGINE_VERSION` stays at `0.2.0`** — the single-fractal encode/decode
  algorithm is unchanged. Only the *protocol* layer (`protocol.py`, its Rust mirror,
  and the FFI orbit helpers) moves.
- The `[A-Z0-9-]` label discipline survives, but demoted (see §2.1): it is a
  **domain-separation pepper / export label**, no longer the entropy root.

## 2. What changes, module by module

### 2.1 Root: Namtso `σ` replaces the free-text stage 0

- `o₀ := H(σ)` where `σ` is the **Namtso** salt harvested from a memorable date
  ([`namtso-spec.md`](namtso-spec.md)). Core gains a dependency on the Namtso
  `harvest(date) → σ` library (Rust core, per that spec's language-of-record
  recommendation) — or accepts a pre-harvested `σ` blob so the two can ship
  independently.
- The old stage-0 text field is retained **only** as an optional pepper mixed into
  domain separation, never as the sole root. Setups that used `0.3.0` stage-0 text as
  their entropy anchor cannot migrate silently — see §6.

### 2.2 Stage: one → `s_i` fractals (`theta_i_j`)

- Derive `theta_i_j = H(o_i ‖ j)` for `j ∈ [0, s_i)`. Each `theta_i_j` parameterises
  an independent Burning Ship perturbation `(o,p,q)` exactly as today — so the encoder
  is called `s_i` times per stage, unchanged per call.
- `p_i_j` is the 32-bit leaf-area on fractal `j`. A stage now yields an **`s_i`-vector
  of 32-bit points**, not a scalar.

### 2.3 Stage contribution: raw concat → Shamir `Sh_i`

- New module `shamir.rs` (+ Python mirror): Shamir over **GF(2³²)** (the field already
  chosen in [`post-graduation-security-tiers.md`](post-graduation-security-tiers.md)).
- Convention: the `t_i` **primary** shares sit at positive abscissae; opt-in
  `(s_i − t_i)` **forgetting-resistance** shares at negative abscissae. Reconstruct the
  degree-`t_i−1` polynomial from any `t_i` points.
- `Sh_i` fed into the orbit is the **full polynomial** (`t_i·32` bits) — *not* the
  constant term `f(0)`. This is load-bearing: it is what makes each orbit link `≥ 64*`
  and the stored orbit offline-safe. A regression to `f(0)` silently reintroduces a
  single-point oracle. Add a test asserting `len(Sh_i) == t_i·32` bits.

### 2.4 Orbit advance: wiped nested `H*(H(·))`

```
c   := H( o_{i−1} ‖ Sh_{i−1} )     # instant; then wipe {o_{i−1}, Sh_{i−1}}
o_i := H*( c )                      # the long Argon2d step, on c alone
```

- The memory-hard `H*` (Argon2d) now runs on the **cheap-hash commitment `c`**, not on
  the raw `o_{i−1} ‖ Sh_{i−1}`. Implement the wipe explicitly (zeroize `o_{i−1}`,
  `Sh_{i−1}`, and the concatenation buffer before entering `H*`). This is the
  seizability-window minimiser (design goal 1); it is a **security property of the
  implementation**, so it needs a test that the raw inputs are not live across the
  `H*` call (at minimum a zeroize-on-drop guard; ideally a RAM-residency assertion).
- `H*` calibration is user-tunable and durable via the iteration count (the `0.3.0`
  "one iteration count per setup, wall-clock is a perishable label" policy carries over
  verbatim).

### 2.5 Master secret: `Argon2id`-transcript → cheap `K`

- `K := H(o_N ‖ Sh_N)` — **cheap `H`, deliberately** (a memory-hard last step would
  prolong the `o_N` window; resistance lives in entropy, not terminal hardness — spec
  §5). This **removes** the `0.3.0` `Argon2id`-over-transcript master export.
- Output-size ergonomics (the `0.3.0` "first 32 hex chars" placeholder) can be settled
  here: define `K`'s full width and its truncation contract once, in `protocol.rs`.

### 2.6 Entropy tiers: BIP39-words → setup pathway

- `0.3.0` binds `N = words/3` and offers 3–24 words. `0.4.0` decouples: stage entropy
  is `t_i·32` and setups follow the **pathway** (Setup 1 = stage-0 2pts + stage-1 2pts
  / 64-bit; Setup 2 = 3pts / 96-bit; Setup 3/4 add deep stages — spec §7). BIP39
  export remains a *downstream* encoding of `K`, not the protocol's internal entropy
  accounting.
- Expose the per-tier `(s_i, t_i)` table over FFI the same way `encode_params()` is
  exposed today (engine dictates protocol; no hand-mirrored copies).

## 3. FFI surface additions

New C-ABI exports (mirroring the `bs_encode_params` discipline — the engine is
authoritative, callers read):

| Export | Purpose |
|---|---|
| `bs_theta(o_i, j) → (o,p,q)` | derive fractal `j`'s params for a stage |
| `bs_shamir_interp(points, abscissae, t) → Sh` | GF(2³²) reconstruct full polynomial |
| `bs_orbit_advance(o_prev, Sh_prev) → o_i` | wiped `H*(H(·))`; zeroizes inputs |
| `bs_master_secret(o_N, Sh_N) → K` | cheap `H`, fixed width |
| `bs_setup_tiers() → table` | canonical `(s_i, t_i)` per setup level |

All secret-bearing buffers are caller-allocated, zeroized by the engine after use, and
never logged (the existing `<redacted>` / no-coordinates-in-logs invariant extends to
`o_i`, `Sh_i`, `theta_i_j`, and `K`).

## 4. Test-vector & versioning plan

- Bump `PROTOCOL_VERSION 0.3.0 → 0.4.0` in both `protocol.py` and `DESIGN.md`; re-stamp
  the `protocol_version` field in encode/decode JSON. The harness version guard already
  flags mismatched vectors as **STALE**, so `0.3.0` vectors go stale automatically —
  no false-green risk.
- New frozen vectors (deferred to `1.0.0` per the pre-1.0 policy, but add at least one
  interim smoke vector per setup tier): `(σ, setup-tier, D) → {theta_i_j, p_i_j, Sh_i,
  o_i, K}`, with a **clean-room reproducibility** target.
- New property tests: Shamir round-trip (any `t_i` of `s_i` reconstruct the same
  polynomial); `Sh_i` width `== t_i·32`; orbit forward-only (`o_i` cannot yield
  `o_{i−1}`); wipe-before-`H*` residency guard; `K` stable across share-subset choice.

## 5. Sequencing (suggested)

1. `shamir.rs` + GF(2³²) + tests (self-contained, no protocol coupling).
2. `theta_i_j` multi-fractal derivation + FFI (`bs_theta`).
3. Orbit advance with wipe + FFI (`bs_orbit_advance`); retire the transcript master.
4. Cheap `K` + FFI (`bs_master_secret`).
5. Namtso `σ` root wiring (or pre-harvested-blob intake).
6. Setup-tier table + `protocol.py` rewrite driving encode/decode through the orbit.
7. Version bump, STALE-flag old vectors, add interim smoke vectors.

Steps 1–4 are independently testable and land without breaking `0.3.0` callers until
step 6 flips `protocol.py`. Retirement/level-up/rekey (spec §7) and TLP decks (spec §8)
are **wallet-layer** concerns and are out of scope for core beyond exposing the
primitives above — cross-referenced in the UX plan
([`ux-orbit-redesign-plan.md`](ux-orbit-redesign-plan.md)).

## 6. Migration & open items

- **No silent `0.3.0 → 0.4.0` migration.** The entropy root moves from stage-0 text to
  `σ`, and the chain arithmetic changes — a `0.3.0` setup is a *different* secret. The
  wallet MUST treat this as a rekey (move funds), the same class of event as any orbit
  change (spec §7 "rekey on every change").
- **Open:** concrete `H*` per-eval target (shared with spec §11); whether Namtso ships
  as a linked Rust crate or core accepts a pre-harvested `σ`; `K` output width/format;
  whether the `(s_i − t_i)` forgetting-resistance shares are a core or wallet concern.
