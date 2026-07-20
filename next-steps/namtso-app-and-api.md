# Namtso — the Sacred Salt (timechain salt harvester)

> Spin-off of Great Wall. **Namtso** turns a user-memorable **date** into the ≥ 1 Kb
> timechain salt `σ` — deterministically, reproducibly, decades later — by *harvesting*
> `σ` from Bitcoin block headers around that date.
>
> **The name.** *Namtso* ("Heavenly Lake") is one of Tibet's three great **sacred salt
> lakes**; its salt is the *sacred salt*. The epithet earns its own memorization: one
> expects something *sacred* to be **kept, preserved, and to transcend** — exactly what
> the timechain's unsurpassable availability and proof-of-work integrity deliver for the
> salt harvested from it. (Bonus etymology: **Na** = sodium; *-tso* ≈ "salt.") It stays in
> the dissident-naming family — Great Wall · Formosa · Celestial Peace · **Namtso** — and
> follows the house principle that *memory consolidates on a pleasant image*.
>
> **Build from the normative spec:** [`namtso-spec.md`](namtso-spec.md) (this doc is the
> design/product overview; the spec is the implementation contract). Formal basis:
> [`bitcoin-nonce-salt.md`](bitcoin-nonce-salt.md); paper:
> [`../papers/timechain-salt.md`](../papers/timechain-salt.md).

## 1. What it is (and isn't)

- **Is:** a small, **stateless**, deterministic function `harvest(date) → σ`, packaged as
  a **reference library + CLI + optional HTTP API**. Handles **no secret material** — its
  output is a *public* salt.
- **Isn't:** a wallet, a key manager, or a randomness *beacon* for live use. It reads a
  *past* window of the chain; nothing here is secret, live, or unbias-critical (§security
  of the salt doc).

## 2. Core primitive (recap)

```
harvest(d, w) :
  B ← firstBlockWithMTP_atLeast(midnightUTC(d))      # deterministic selection
  H ← headers[B .. B+w-1]                              # w canonical 80-byte headers
  σ ← SHAKE256( H[0] ‖ H[1] ‖ … ‖ H[w-1] , 1024 bits )
  return σ, receipt(B, heights, hashes, rule, version)
```

Default `w = 32` (≥ 1 Kb of nonce-grade entropy; greedy for good measure). `σ` is 128
bytes.

## 3. Architecture

Three layers, only the middle one does I/O:

1. **Deterministic core (pure).** `harvest()` above — no network, no clock, no
   randomness. Given the `w` headers it is a pure function. This is the part that must be
   **bit-identical forever**; everything else is replaceable.
2. **Header-source adapters (pluggable I/O).** Fetch `w` consecutive headers from block
   height `B`:
   - **Local Bitcoin full node** (RPC `getblockhash`/`getblockheader`) — trust-minimized
     default.
   - **Public explorers** (fallback; query ≥2 and cross-check).
   - **Offline** — user supplies a headers file (air-gapped recovery).
3. **Interfaces.** CLI, library bindings (Dart for great-wallet; Rust/JS optional), and an
   optional stateless HTTP endpoint.

### 3a. Trust-minimization — PoW self-verification

Because headers are **self-authenticating**, the core **verifies** what any adapter
returns, so the *source need not be trusted for integrity*:

- each header hashes below its own `target` (valid PoW),
- each `prev_block` links to the previous header (a real chain),
- MTP of `B` brackets `midnightUTC(d)` per the selection rule.

An untrusted or malicious explorer therefore **cannot forge `σ`** — it can at worst refuse
service (availability, not integrity). This is the property that lets Namtso use cheap
public data sources without a trust cost.

## 4. Interfaces

- **CLI:** `namtso harvest --date 1990-06-04 --window 32 [--node <rpc> | --headers <file>]`
  → prints `σ` (hex) + a human-readable **receipt** (heights, block hashes, rule, version).
- **Library:** `harvest(date, window, source) -> {sigma, receipt}`; plus `verify(receipt,
  headers)` to re-check a prior harvest offline.
- **HTTP (optional):** `GET /salt?date=YYYY-MM-DD&window=32` → `{ "sigma": "...", "receipt":
  {...} }`. **Stateless; logs nothing.** (See privacy, §6 — hosted use leaks the *date*, so
  local/offline is the recommended default.)

## 5. Reproducibility contract (the load-bearing part)

Recovery may happen **decades** later on different software, so the algorithm is pinned:

- **Fixed forever:** UTC; the `midnight-UTC + first-block-by-MTP` selection rule; canonical
  80-byte little-endian header serialization (as in Bitcoin); `SHAKE256`; 1024-bit output;
  concatenation order = ascending height.
- **Versioned:** `NAMTSO_VERSION` stamped into every receipt; recovery uses the matching
  version. A change to *any* fixed element bumps the version (never silently).
- **Test vectors:** `(date, window, version) → σ` fixtures, shipped and frozen at 1.0, so a
  clean-room reimplementation can prove bit-identity.
- **Burial requirement:** reject a `date` unless `B+w` is buried by `≥ C` confirmations
  (default deep, e.g. `C = 100`) so no reorg can change `σ`. A *past birthday* satisfies this
  trivially; a near-present date is refused.

## 6. Trust & privacy posture

- **No secrets handled.** `σ` is public; the only sensitive input is the **date** (a
  birthday → personally identifying).
- **Local-first.** Recommended default: run the core against a **local node or an offline
  headers file**, so the date never leaves the device. The hosted API is a *convenience*
  that reveals the date to the operator — gate it behind Tor and a "we log nothing" stance,
  and prefer local for the privacy-conscious.
- **Date cloaking (for remote sources).** Rather than request the exact `w`-block window,
  fetch a **larger, coarser interval** (e.g. a random month-scale range) that *contains* it and
  extract the window locally — the source learns only the interval, not the day (anonymity set ≈
  the interval span). The larger contiguous sample is also an **integrity dividend** (more PoW to
  forge), pairing with checkpoint anchoring against re-mined old-window forgeries. **σ-orthogonal**
  — the cloak never affects the salt (spec §7b).
- **Low blast radius.** Compromising Namtso leaks at most a user's chosen date; it cannot
  leak funds or recall (those never touch it).

## 7. Great Wall integration

great-wallet **Setup** calls `harvest(date, w)` → `σ`, which seeds the derivation orbit
(`Argon2d^D(σ)`). At recovery, the same library + version + date reproduces `σ`. The date is
stored/handled like any other stage-0 material (recalled, not written); the *receipt* may be
kept as a non-secret convenience (it reveals only public block references).

## 8. Edge cases & failure modes

- **Future / unmined date** → error (must be past).
- **Pre-genesis date** (< 2009-01-03) → error.
- **Insufficient burial** (reorg risk) → error with the confirmations shortfall.
- **Source unavailable** → try next adapter; offer offline-headers path; never silently
  substitute a different window.
- **Leap/timezone ambiguity** → pinned to `00:00 UTC`; no local-time interpretation.

## 9. Roadmap to "shipped" (MVP)

Honest bar for reporting Namtso as *shipped* (vs. "in development"):

1. **Core lib** (Rust or Dart) implementing `harvest` + `verify`, pure & tested.
2. **One trust-minimized adapter** (local node RPC) **+** offline-headers path.
3. **CLI** + frozen **test vectors** + reproducibility doc.
4. **Open-source repo**, MIT/Apache, with the paper linked.

That set is genuinely shippable and small. The HTTP API and extra bindings are
post-MVP. Only once (1)–(4) are live and tagged do we describe Namtso as *shipped* in
the HRF report; until then it is "spun out of Great Wall, in active development."

## 10. Open decisions

- **Language of record** for the core (Rust = portable/auditable; Dart = reuses
  great-wallet toolchain). Recommend **Rust** for a standalone, embeddable, auditable core
  with a thin Dart FFI for great-wallet.
- **Repo home:** new standalone repo `namtso` (cleaner spin-off story for HRF) vs. a
  subfolder of an existing repo. Recommend standalone — it's the point of a spin-off.
- **Hosted API at all?** vs. local-only (max privacy, min liability). Lean local-only for
  1.0; revisit.
