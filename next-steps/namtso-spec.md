# Namtso — reference specification (v1, normative)

> Implementation-ready spec for a neighbor chat to build from. Product/design overview:
> [`namtso-app-and-api.md`](namtso-app-and-api.md). Rationale + formal results:
> [`bitcoin-nonce-salt.md`](bitcoin-nonce-salt.md), [`../papers/timechain-salt.md`](../papers/timechain-salt.md).
> Keywords **MUST / SHOULD / MAY** are per RFC 2119. Everything under "Determinism pins"
> is frozen at v1 — a change to any of it MUST bump `NAMTSO_VERSION`.

## 0. Constants

| Name | Value |
|---|---|
| `NAMTSO_VERSION` | `"namtso-1"` |
| Network (default) | Bitcoin **mainnet** (genesis height 0, nTime `1231006505` = 2009-01-03T18:15:05Z) |
| `w` (window, default) | `32` blocks (≥ 1 Kb of nonce-grade entropy) |
| `w` bounds | `1 ≤ w ≤ 256` |
| `C` (burial, default) | `100` confirmations |
| σ length | `1024` bits = `128` bytes |
| XOF | `SHAKE256` |

## 1. Inputs

- **`date`** — a Gregorian calendar date, **interpreted as `00:00:00 UTC`**. Accept ISO 8601
  `YYYY-MM-DD`. Let `target_time` = its Unix timestamp (integer seconds).
  - *Advanced (optional):* a full `--timestamp <unix>` mode (e.g. birth *hour*) for finer
    per-user uniqueness. Same pipeline with `target_time` set directly.
- **`w`** — window length (default 32; `1..256`).
- **`network`** — default mainnet.
- **`source`** — a header-source adapter (§7): local node RPC, public explorer(s), or an
  offline headers file.

## 2. Deterministic block selection `B(date)`

Let `nTime(h)` be the header timestamp at height `h`.

**Median-time-past.** `MTP(h) = median{ nTime(h), nTime(h−1), …, nTime(h−10) }` — the median
of the block and its 10 ancestors (the standard `GetMedianTimePast`, 11 values; for `h < 10`
use the median of the `h+1` available). `MTP` is **non-decreasing in `h`** (consensus requires
each block's `nTime` > `MTP(parent)`), so the selection below is unique and binary-searchable.

**Selection.** `B(date)` = the **least** height `h` such that **`MTP(h) ≥ target_time`**
(strict `≥`). MUST use `MTP`, not raw `nTime` (raw timestamps are non-monotone within the
~2 h drift; `MTP` is monotone and reorg-stable, per BIP113).

Errors:
- `target_time > MTP(tip)` ⇒ **`DATE_FUTURE`** (no block yet satisfies it).
- `target_time ≤ nTime(0)` ⇒ **`DATE_PREGENESIS`** (before Bitcoin; reject — a *recent* "last
  birthday before setup" is always post-genesis, so this is only a guard).

## 3. Header window & message

Heights `B, B+1, …, B+w−1`. For each, `header_bytes(h)` is the canonical **80-byte** header —
the exact preimage of the block hash:

```
int32LE  version ‖ 32B prev_block ‖ 32B merkle_root ‖ uint32LE nTime ‖ uint32LE nBits ‖ uint32LE nonce
```

`prev_block` and `merkle_root` MUST be in **internal (hashing) byte order** — the raw header
bytes, *not* the byte-reversed explorer-display form. Then:

```
message = header_bytes(B) ‖ header_bytes(B+1) ‖ … ‖ header_bytes(B+w−1)   (ascending height)
```

## 4. Salt

```
σ = SHAKE256(message), squeezed to 1024 bits (128 bytes)
```

- **Raw form:** 128 bytes — the value fed to a KDF as a salt.
- **Display form:** lowercase hex (256 chars).

## 5. Burial / reorg safety

Let `tip` be the current best height. REQUIRE `tip ≥ B + w − 1 + C` (`C` default 100); else
**`INSUFFICIENT_BURIAL`** with the shortfall. `MTP` selection + deep burial together guarantee
`σ` is **bit-stable** against any feasible reorg. A past birthday satisfies this trivially.

## 6. Receipt (non-secret)

`harvest` returns `(σ, receipt)`. Receipt is a JSON object (stable key order for hashing not
required; it is descriptive, not part of `σ`):

```json
{
  "namtso_version": "namtso-1",
  "network": "mainnet",
  "date": "2020-01-15",
  "target_time": 1579046400,
  "window": 32,
  "start_height": 000000,
  "block_hashes": ["<display-hex hash of B>", "…", "<display-hex hash of B+w-1>"],
  "sigma": "<128-byte hex>"
}
```

`block_hashes` are conventional **display** (byte-reversed) hex. The receipt MAY be stored as a
convenience (it references only public blocks) but **reveals the `date`** — treat like any
stage-0 material (§9).

## 7. Header-source adapters (I/O boundary)

The core (§2–4) is a **pure function of the headers**. Adapters only fetch headers for a height
range and MUST NOT alter selection:

- **Local node (default, trust-minimized):** RPC `getblockhash(height)` → `getblockheader(hash,
  false)`; also `getblockcount` for `tip`.
- **Public explorer(s) (fallback):** query **≥ 2** independent explorers and cross-check the
  returned headers are byte-identical before use.
- **Offline:** user supplies a headers file (raw 80-byte concatenation + a height index) for
  air-gapped recovery.

### 7a. PoW self-verification (why adapters need not be trusted)

The core MUST verify every fetched header, so a lying source cannot forge `σ` (only deny
service):

- **PoW:** `target = decode_nBits(nBits)`; `h256 = SHA256d(header_bytes)` read as a
  **little-endian** 256-bit integer; require `h256 ≤ target`.
- **Linkage:** `prev_block(h+1) == SHA256d(header_bytes(h))` (internal order).
- **Selection bracketing** (for `verify`, not needed for a fresh `harvest`): `MTP(B) ≥
  target_time` **and** `MTP(B−1) < target_time` (proves *first*). Computing `MTP(B)` and
  `MTP(B−1)` needs headers `B−11 … B+w−1`, so a self-verifying bundle SHOULD carry those 11
  predecessor headers.

### 7b. Date cloaking (privacy) & main-chain anchoring

**Cloaking (optional; for remote sources).** Fetching exactly `B … B+w−1` reveals the `date` to
the source. Instead, request a **larger, coarser interval** `[lo, hi] ⊇ [B, B+w−1]` — e.g. a
random interval spanning `≥ M` blocks (or a whole calendar month) — download all its headers,
verify the segment (§7a), and **extract the exact window locally**. The source then learns only
the interval, not the day. Choose `lo, hi` so the window's **offset within `[lo, hi]` is random**
(random start + random length `≥ M`), so its position is not inferable. The `date`'s anonymity
set becomes ≈ the interval span (coarser ⇒ more private ⇒ more bandwidth; a month ≈ 4320 headers
≈ 345 KB — cheap). Still weaker than **local/offline** (zero leak); pair remote use with **Tor**.

**σ-orthogonality (normative).** Cloaking is a **fetch/privacy layer only**. `σ` depends *solely*
on the pinned selection `B(date)` and `w`. The interval `[lo, hi]` and its randomness **MUST NOT**
influence `σ`, **MUST NOT** be a determinism pin, and need not be reproducible (ephemeral, locally
random per fetch). Recovery reproduces `σ` under any cloak setting, including none.

**Main-chain anchoring (integrity — the "larger sample" benefit).** PoW-verifying an isolated
window proves *valid work*, not *main chain* — and **old, low-difficulty** windows (early years)
are cheap enough to **re-mine**, so a colluding source could feed a valid-PoW *alternative* history
for an old date. Two mitigations, both strengthened by cloaking's larger sample:
- **Larger contiguous sample** ⇒ more cumulative PoW an adversary must forge to fake the window —
  this is the cloak's integrity dividend.
- **Anchor to a checkpoint** ⇒ verify the fetched segment links, via the header chain, toward a
  **hardcoded recent block hash** (or the live tip). Then it is provably *the* main chain, not a
  re-mined fork. Local-node adapters get this for free; remote adapters SHOULD anchor. Ship a small
  set of hardcoded checkpoint hashes, refreshed per release.

## 8. Algorithms (reference pseudocode)

```
harvest(date, w, source):
    target_time = midnight_utc_unix(date)          # or the given timestamp
    tip = source.tip()
    if target_time > MTP(source, tip): raise DATE_FUTURE
    if target_time <= source.nTime(0): raise DATE_PREGENESIS
    B = min h in [1, tip] with MTP(source, h) >= target_time     # binary search (MTP monotone)
    if tip < B + w - 1 + C: raise INSUFFICIENT_BURIAL(shortfall)
    H = [ source.header_bytes(B+i) for i in 0..w-1 ]
    for each consecutive pair: assert linkage; for each: assert PoW      # §7a
    sigma = SHAKE256(concat(H)).squeeze(128)
    return sigma, receipt(...)

verify(receipt, headers[B-11 .. B+w-1]):
    recompute B from target_time using MTP over the supplied context; assert == receipt.start_height
    assert PoW + linkage over all supplied headers
    assert SHAKE256(concat(headers[B..B+w-1])).squeeze(128) == receipt.sigma
```

`MTP` monotonicity ⇒ selection is an `O(log n)` binary search over height (fetch `nTime` at
probe heights; `MTP` needs the probe and its 10 ancestors).

## 9. Errors (enumerated)

`DATE_FUTURE` · `DATE_PREGENESIS` · `INVALID_DATE` (unparseable / not a real calendar date) ·
`WINDOW_OUT_OF_RANGE` · `INSUFFICIENT_BURIAL` (with shortfall) · `SOURCE_UNAVAILABLE` (all
adapters failed) · `POW_INVALID` / `LINKAGE_INVALID` (a source returned a bad header) ·
`EXPLORER_MISMATCH` (cross-check failed). Errors MUST be explicit; the tool MUST NOT silently
substitute a different window, date, or source result.

## 10. Interfaces

- **CLI:**
  `namtso harvest --date YYYY-MM-DD [--window 32] [--network mainnet] [--node <rpc-url> | --explorer <urls> | --headers <file>] [--burial 100]`
  → stdout: `σ` (hex) line, then the receipt JSON. Nonzero exit + stderr JSON `{ "error": CODE,
  … }` on failure.
  `namtso verify --receipt <file> --headers <file>` → exit 0 iff it recomputes.
- **Library:** `harvest(date, window, source) -> {sigma: bytes[128], receipt}`;
  `verify(receipt, headers) -> bool`. Pure core; adapters injected.
- **HTTP (optional, post-MVP):** `GET /salt?date=…&window=…` → `{sigma, receipt}`. Stateless;
  logs nothing. Discouraged vs. local (§9 privacy) — it reveals the `date` to the operator.

## 11. Test vectors

Fixture schema (`vectors/*.json`), **frozen at v1**:

```json
{ "namtso_version": "namtso-1", "network": "mainnet",
  "date": "YYYY-MM-DD", "window": 32,
  "start_height": <int>, "block_hashes": ["…"], "sigma": "<hex>" }
```

Generation (reference implementation, then freeze): pick several **fixed heights** on mainnet,
record `start_height`, the `w` display hashes, and the computed `σ`; a clean-room reimpl MUST
reproduce `sigma` bit-for-bit. Ship ≥ 3 vectors across different difficulty epochs.
*Anchor for sanity (not a σ vector):* genesis = height 0, `nTime 1231006505`, hash
`000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`. **Do not fabricate σ
values in the spec** — they are produced by the implementation and then frozen.

## 12. Determinism pins (bump `NAMTSO_VERSION` on any change)

1. Time zone **UTC**; `date` ⇒ `00:00:00 UTC`.
2. Selection = **first height with `MTP(h) ≥ target_time`**, `MTP` = 11-block median.
3. Header serialization = raw **80-byte internal-order**; window = ascending height `B..B+w−1`.
4. XOF = **SHAKE256**, output **1024 bits**; concatenation order = ascending height.
5. Network = **mainnet**; genesis constants as above.
6. Defaults `w=32`, `C=100` are *policy* (may vary per call) — but the **rule** above is fixed.

## 13. Security & privacy (normative recap)

- Handles **no secrets**; `σ` is **public**. Threat model is **precomputation**, not
  confidentiality (see the salt doc: A1, N1–N3).
- **Local-first:** default to a local node or offline headers so the `date` never leaves the
  device; the hosted API is a convenience that leaks the `date` — gate behind Tor, log nothing.
- **Trust-minimized:** PoW self-verification (§7a) ⇒ untrusted sources cannot forge `σ`.
- **Low blast radius:** a Namtso compromise leaks at most a chosen `date`.

## 14. Non-goals

Not a wallet/key-manager; not a live randomness **beacon** (reads a *buried past* window, where
miner malleability is a non-issue — see paper §4); no full block/UTXO validation — main-chain
assurance comes from **checkpoint anchoring** (§7b) plus burial and explorer cross-checking, not
from consensus validation of the whole chain.
