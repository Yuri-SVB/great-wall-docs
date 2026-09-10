<!-- Moved here from the namtso-the-sacred-salt repository README, where design
     documentation should not live. Build and run commands stay in that README. -->

# Namtso — the Sacred Salt

> Turn a memorable **date** into a `≥ 1 Kb` **timechain salt** `σ` —
> deterministically, reproducibly, decades later — by *harvesting* `σ` from
> Bitcoin block headers around that date.

Namtso is a small, **stateless**, deterministic function `harvest(date) → σ`,
packaged as a reference **library + CLI**. It handles **no secret material**:
its output is a *public* salt whose job is defeating **precomputation** (rainbow
tables, cross-target amortization), not confidentiality. The only sensitive
input is the date, so Namtso is **local-first**.

- **Normative spec:** [`docs/namtso-spec.md`](docs/namtso-spec.md) — the
  implementation contract this crate satisfies.
- **Design / product overview:** [`docs/namtso-app-and-api.md`](docs/namtso-app-and-api.md)
- **Formal basis:** [`docs/bitcoin-nonce-salt.md`](docs/bitcoin-nonce-salt.md) ·
  paper skeleton [`docs/timechain-salt.md`](docs/timechain-salt.md)

*Namtso ("Heavenly Lake") is one of Tibet's three great sacred salt lakes; its
salt is the sacred salt — kept, preserved, and transcending, like the salt the
timechain preserves. (Bonus: **Na** = sodium; *-tso* ≈ "salt".)*

## Why a block-header salt

A salt must be **reproducible** from near-zero stored state, yet
**unpredictable in advance** and **unique per user**. A salt derived from
Bitcoin headers at a user-memorable date meets all three:

1. **Relatable to a cheap memorized datum** — the user recalls only a *date*
   (a birthday); the app reconstructs all of `σ` from the public chain.
2. **Unsurpassable availability + PoW integrity** — recomputable from any full
   node or archive, forever; the historical block is proof-of-work-immutable.
3. **Cheap enough to be greedy** — a handful of header lookups gathers `1 Kb`,
   ~1000× what a salt needs, at ~zero cost.

Under a standard random-oracle assumption on SHA-256, a future block's winning
header is computationally unpredictable, so **no table precomputed before the
date can contain `σ`**, and per-user date-keying makes tables
**non-amortizable** across targets. See [`docs/bitcoin-nonce-salt.md`](docs/bitcoin-nonce-salt.md).

## How it works (the pinned pipeline)

```
harvest(date, w):
  target_time = midnight_UTC(date)                        # pin: UTC, 00:00:00
  B           = first height h with MTP(h) ≥ target_time  # pin: MTP selection (BIP113)
  H           = headers[B .. B+w-1]                        # w canonical 80-byte headers
  σ           = SHAKE256( H[0] ‖ … ‖ H[w-1] )  → 1024 bits # pin: SHAKE256, 128 bytes
```

Every fetched header is **self-verified** — valid proof-of-work and linkage to
its predecessor (spec §7a) — so an untrusted source **cannot forge `σ`**; it can
only deny service. Deep **burial** (default `C = 100` confirmations) plus MTP
selection make `σ` bit-stable against any feasible reorg.

## CLI

```
namtso harvest --date YYYY-MM-DD [--window 32] [--network mainnet]
       [--node <rpc-url> [--rpc-auth user:pass] | --explorer [urls] | --headers <file>]
       [--burial 100] [--cloak [BLOCKS]] [--explorer-concurrency 8]

namtso verify --receipt <file.json> --headers <NAMTSOH1 file>
```

`harvest` prints the `σ` hex line, then the receipt JSON. On failure it prints
`{ "error": CODE, ... }` to stderr and exits non-zero.

### Examples

```sh
# Trust-minimized: a local Bitcoin node (the date never leaves your device).
namtso harvest --date 2010-05-22 --node http://127.0.0.1:8332 --rpc-auth user:pass

# Air-gapped recovery from an offline headers bundle.
namtso harvest --date 2010-05-22 --headers ./my.headers

# Fallback: two public explorers, cross-checked byte-for-byte (pair with Tor).
namtso harvest --date 2010-05-22 --explorer

# Date cloaking: fetch a random ~1-month interval that encompasses the window
# and extract it locally, so a remote source learns the interval, not the day.
namtso harvest --date 2010-05-22 --explorer --cloak

# Re-check a prior harvest offline.
namtso verify --receipt receipt.json --headers bundle.headers
```

## Library

```rust
use namtso::{harvest, verify, HarvestOpts, Target};
use namtso::source::{NodeSource, OfflineSource};

let source = NodeSource::new("http://127.0.0.1:8332", Some(("user", "pass")));
let out = harvest(&Target::Date("2010-05-22".into()), &HarvestOpts::default(), &source)?;
println!("σ = {}", out.receipt.sigma);
# Ok::<(), namtso::Error>(())
```

The core (`select`, `mtp`, `salt`, `harvest`) is a **pure function of the
headers**; adapters (`OfflineSource`, `NodeSource`, `ExplorerSource`) are the
only I/O and are injected.

## Header-source adapters

| Adapter | Trust / privacy | Use |
|---|---|---|
| `OfflineSource` (`--headers`) | zero network leak | air-gapped recovery; `NAMTSOH1` container |
| `NodeSource` (`--node`) | trust-minimized, local | **default**; Bitcoin Core JSON-RPC |
| `ExplorerSource` (`--explorer`) | leaks the date; `≥ 2` cross-checked | fallback; pair with Tor |

All are untrusted for **integrity** — the core PoW-verifies every header.

The `ExplorerSource` fetches a window (or a `--cloak` interval) in as few
requests as possible and concurrently, since a per-height fetch (two HTTP
round-trips per explorer) otherwise dominates wall-clock time:

- **Bulk reconstruction.** Ranges are fetched via Esplora's
  `/blocks/{start_height}` endpoint (10 block summaries per request) and each
  canonical 80-byte header is *reconstructed* from the summary fields — ~10×
  fewer requests. Reconstruction is not trusted: the core PoW-verifies every
  header, so a wrong byte fails loudly (never a wrong `σ`), and the
  two-explorer cross-check still applies. If an explorer lacks a usable bulk
  endpoint, it transparently falls back to the exact-bytes per-header path.
- **Graceful degradation.** If one explorer lacks a usable bulk endpoint (or a
  page rate-limits), only the missing `(explorer, height)` pairs fall back to
  per-header — a weak explorer never collapses the whole batch.
- **Concurrency.** `--explorer-concurrency N` (default `4`, `1` = serial) fans
  the bulk pages (and any per-header fills) across a small thread pool over a
  shared connection-pooling agent. The default is deliberately modest: public
  explorers **rate-limit** (HTTP 429) aggressive callers, and with the bulk path
  already cutting request count ~10× a small pool is plenty. Raise it against
  your own node/explorer.
- **Rate-limit resilience.** HTTP 429 and transient 5xx/network errors are
  retried with exponential backoff (honoring `Retry-After`), so a throttling
  explorer slows a harvest rather than failing it.
- **Down-explorer tolerance.** A source that denies service (connection resets,
  persistent errors) is treated as absent, not fatal: as long as one explorer
  returns a height the harvest proceeds. Cross-check still applies to every
  explorer that *did* respond; when a block ends up single-sourced the CLI
  prints a `warning:` naming how many, since that block's `≥ 2` agreement was
  not met (its header is still PoW-verified).

The transport layer never changes `σ`, the byte-for-byte cross-check, or the PoW
verification.

### Troubleshooting `--explorer` (VPN / Tor / shared IPs)

If an `--explorer` harvest is **very slow, retries a lot, or fails** with
`SOURCE_UNAVAILABLE` citing HTTP `429` (rate-limit) or a `Connection reset by
peer`, the most common cause is **not** your connection speed — it's your
**exit IP**. Public explorers (blockstream.info, mempool.space) aggressively
rate-limit or block shared IPs, so a **VPN or Tor exit node** often gets
throttled or reset. This bites exactly when you reach for privacy tooling.

Namtso now degrades gracefully rather than hanging — it retries with backoff,
tolerates one explorer being down (printing a cross-check `warning:`), and
bounds how long it fights a dead source — but a throttled IP is still slow or
one-sided. If you hit this:

- **Switch exit IP** — change VPN region/server (or Tor circuit). A different,
  non-flagged IP usually clears it immediately.
- **Prefer a local source.** `--node` (your own Bitcoin Core) and `--headers`
  (an offline bundle) have no rate limits, are far faster, and leak nothing —
  and are the recommended paths anyway. `--explorer` is the no-infrastructure
  fallback.
- **Wait out the cooldown.** Rate limits are usually a rolling window; a few
  minutes between attempts helps.
- **Point at your own explorer.** `--explorer https://my-esplora/api,https://…`
  uses instances you control (no shared-IP throttling).
- **Diagnose with `--stats`**, which prints elapsed time, HTTP request count,
  effective concurrency, and (via the `warning:`) any degraded cross-check —
  enough to tell a throttled IP apart from a genuinely slow harvest.

Note the tension: the privacy advice to *pair remote use with Tor* and the
reality that *explorers throttle Tor/VPN IPs* pull in opposite directions. For
privacy **and** reliability, run against a local node or offline headers.

## Reproducibility contract

Recovery may happen **decades later** on different software, so the algorithm is
frozen (spec §12, "Determinism pins"). A change to **any** of these bumps
`NAMTSO_VERSION` (currently `namtso-1`), never silently:

1. Time zone **UTC**; `date` ⇒ `00:00:00 UTC`.
2. Selection = first height with `MTP(h) ≥ target_time`; `MTP` = 11-block median.
3. Header serialization = raw **80-byte internal-order**; window ascending `B..B+w-1`.
4. XOF = **SHAKE256**, output **1024 bits**; concatenation ascending by height.
5. Network **mainnet**; genesis `nTime 1231006505`, hash
   `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`.

**Test vectors** live in [`vectors/`](vectors/): each ships a real mainnet
header bundle and a frozen `σ`, produced independently by a stdlib-SHAKE256
reference and reproduced bit-for-bit by this crate (`cargo test`). A clean-room
reimplementation MUST reproduce them.

The dates are chosen to span different difficulty epochs (spec §11) and, in the
spirit of the dissident-naming family, to carry Bitcoin lore and pro-Tibet /
human-rights allusions (each vector records its `meaning`):

| Date | Allusion |
|---|---|
| `2009-01-04` | Genesis-boundary corner case — earliest harvestable date (genesis day 2009-01-03 is pre-genesis at UTC midnight → `DATE_PREGENESIS`) |
| `2010-05-22` | Bitcoin Pizza Day — 10,000 BTC for two pizzas |
| `2013-05-13` | World Falun Dafa Day (first public teaching, 1992) |
| `2014-07-20` | Falun Gong — 15th anniversary of the start of the CCP persecution (1999) |
| `2015-03-10` | Tibetan Uprising Day (1959 Lhasa uprising) |
| `2019-04-25` | Falun Gong — 20th anniversary of the peaceful Zhongnanhai appeal (1999) |
| `2019-06-04` | Tiananmen Square massacre, 30th anniversary |
| `2019-11-17` | First reported COVID-19 case, Hubei |
| `2020-06-12` | HRF's **Bitcoin Development Fund** launch — first grant backed CoinSwap privacy work (see *Dedication*) |
| `2020-07-06` | The 14th Dalai Lama's birthday (b. 1935) |
| `2009-01-11 03:33 UTC` | **Advanced date+time (`timestamp`) mode:** Hal Finney's "Running bitcoin" tweet — selects block 84, mined ~1 h later |

The last vector runs the advanced `--timestamp` path (`date: null`, `mode:
"timestamp"`) — a raw Unix time rather than a UTC midnight. Selection is by MTP
either way, so `σ` is derived identically; the second-level precision does not
change the block.

## Security & privacy

- Handles **no secrets**; `σ` is public. Threat model is **precomputation**, not
  confidentiality.
- **Local-first:** default to a local node or offline headers so the date never
  leaves the device. A hosted API would leak the date — out of scope for v1.
- **Trust-minimized:** PoW self-verification means untrusted sources cannot forge
  `σ`.
- **Date cloaking (`--cloak`, spec §7b):** for remote sources, fetch a random,
  larger, coarser interval that *encompasses* the window and extract it locally,
  so the source learns only the interval, not the day (anonymity set ≈ the
  interval span; larger ⇒ more private, more bandwidth). The larger verified
  sample is also an integrity dividend (more PoW to forge). Cloaking is
  **σ-orthogonal** — the random interval never affects `σ` — and cloaks the
  window fetch; block *selection* still probes the source, so pair remote use
  with Tor and prefer local/offline for zero leak.
- **Low blast radius:** a Namtso compromise leaks at most a chosen date — never
  keys or funds.

## Great Wall integration

Great Wall **Setup** calls `harvest(date, w) → σ`, which seeds the derivation
orbit (`Argon2d^D(σ)`). At recovery the same library + version + date reproduces
`σ`. The date is stage-0 material (recalled, not written); the receipt may be
kept as a non-secret convenience (it references only public blocks).

## Dedication

Namtso is the first spin-off of **Great Wall**, offered in solidarity with the
**[Human Rights Foundation](https://hrf.org)** and the cause it advances through
its **[Chinese Communist Party Disruption Initiative](https://hrf.org/program/chinese-communist-party-disruption-initiative/)**
and its **[Bitcoin Development Fund](https://hrf.org/program/financial-freedom/bitcoin-development-fund/)**:
exposing digital surveillance and transnational repression, and standing with
dissidents in Tibet, Xinjiang, Hong Kong, and beyond.

That is the same cause Namtso serves — a salt harvested from the timechain so a
person can recover their own money from nothing but a remembered date, beyond any
authority's reach. The frozen test vectors carry that intent (see
[`vectors/`](vectors/)): Bitcoin lore alongside pro-Tibet and human-rights
commemorations, including HRF's own Bitcoin Development Fund launch.

## License

Dual-licensed under either of [MIT](LICENSE-MIT) or
[Apache-2.0](LICENSE-APACHE) at your option.
