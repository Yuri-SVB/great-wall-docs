<!-- Moved here from the great-wall-core repository README, where design
     documentation should not live. Build and run commands stay in that README. -->

# Great Wall Reference Implementation

> ⚠️ **PROOF OF CONCEPT — NOT SAFE FOR USE.** The current Great Wall
> implementation is a **substandard proof of concept**: it does not yet match the
> finalized protocol specification and has not undergone independent security
> review. **Do not use it to protect real Bitcoin, funds, or any secret of
> value.** This notice will be removed once the implementation is brought up to
> the specified protocol.

Bijective mapping between BIP39 mnemonic seeds and Burning Ship fractal
locations, with an Argon2-based chained pipeline: a mandatory text-only
**stage 0** seeds the chain, then one 32-bit point per later stage, each stage
its own fractal derived by hashing stage-0 text plus all preceding points.

> **Design documentation** for the encoder lives in the `great-wall-docs`
> repository (`great-wall-core/DESIGN.md`) — the single source of truth. This
> README is the only doc kept in this repo.
>
> **Versioning guarantee.** This core implements **chained protocol
> `PROTOCOL_VERSION = 0.3.0`** (see `burning_ship/protocol.py`), and the
> authoritative `DESIGN.md` declares the *same* version. The two are therefore
> verifiably in sync: bump the protocol version in both — and re-stamp the
> encode/decode JSON `protocol_version` field — whenever the protocol's
> behaviour changes. (This is independent of the Rust `ENGINE_VERSION`, the
> single-fractal encode/decode algorithm, now at `0.2.0` — it was bumped from
> `0.1.0` when the encode/decode island-discovery escape cap was raised
> (`64 → 1024`) so deep bisection levels near the set boundary stay navigable
> instead of stalling. That is an output-changing change, so `0.1.0` frozen
> vectors are flagged **STALE** and rebuilt at the stable release.)
>
> **What's new in `0.3.0`** (hard, backward-incompatible — `0.2.0` encodings do
> not round-trip across it):
> 1. A **mandatory, point-less stage 0** carries only a short text input and is
>    chained into stage 1, so **there is no longer a public "canonical" first
>    fractal** — every point-bearing fractal is private and chain-derived.
> 2. Stage-0 text (and every non-0 stage's export label) is **restricted to
>    `[A-Z0-9-]`** for safe cross-device round-tripping, and doubles as a
>    **salt** (a label like `MAIN-STASH`) or a **pepper** (build one setup over
>    another).
> 3. The master-secret carry-over is no longer `SHA512(seedphrase ‖ text)`; it
>    is a single **Argon2id** pass over the reproducible setup transcript.
>
> **Pre-1.0 / test-vector policy.** The protocol is pre-`1.0.0` (unstable;
> more changes are expected — new parameter families, etc.). Comprehensive
> frozen test vectors are intentionally **deferred to the stable `1.0.0`**
> release rather than rebuilt for every interim bump. This is safe because the
> test harness carries a **version guard**: any vector whose `protocol_version`
> differs from the current one is reported **STALE** (skipped, never counted as
> a pass), so stale vectors can never show false-green.

Licensed under either of [Apache License, Version 2.0](LICENSE-APACHE)
or [MIT License](LICENSE-MIT) at your option.

## Why Great Wall?

Protecting a Bitcoin seed phrase is a problem with no good conventional
solution. Every existing approach sacrifices at least one desirable
property. Great Wall provides all four at once:

1. **Knowledge-Based Authentication.** Your secret lives entirely in your
   memory — no device, physical vault, or geographic location required.
2. **Individual Custody.** You depend on no one else. The core premise of
   Bitcoin — full self-custody — is kept intact.
3. **Non-Obscurity.** The method is not a secret trick that fails the
   moment an attacker learns about it. Nor does it rely on convincing the
   attacker that the stash doesn't exist or is smaller than it really is.
4. **Coercion-Resistance.** The threat of violence is ineffective as a
   means to obtain the secret leading to the stash.

> **In one sentence:** it's all in your head (1), in nobody else's (2),
> the attacker is aware of that (3), and is nevertheless unable to rob
> it (4).

This sounds like having your pie and eating it too — many times over. It
is only possible because the secret knowledge (that is only in your head)
is *tacit*, and the interface for *deploying* it (to convert it into a key)
is gated by an inescapably lengthy computation.

### How it works (the simple version)

The Burning Ship fractals are indescribable labyrinths. Great Wall converts
your secret into exact coordinates on these labyrinths.

Your memory of *where* those points are is **tacit knowledge** — the same
kind of knowledge that lets you recognize a friend's face but not describe
it precisely enough for a stranger to pick them out of a crowd. You can
identify your locations by looking at the fractal, but you literally
cannot dictate them to someone else. There is no verbal shortcut: the
only way to extract the secret is to sit in front of the fractal and
point.

Great Wall begins with a text-only **stage 0** — a short label (`MAIN-STASH`,
`RETIREMENT`) or a pepper — and then splits your secret into one 32-bit point
per later stage. Before *each* point can be encoded *or decoded*, the system
requires a long, memory-intensive computation using Argon2 — a key-stretching
algorithm where each step depends on the previous one (strictly sequential) and
requires gigabytes of RAM that cannot be traded for speed. The delay is
configurable: hours, days, or weeks. Each computation produces a unique key
that reshapes the fractal itself — generating a *new, private* labyrinth — and
its input is **stage-0 text plus all the preceding points**, so the labyrinths
form a chain that begins at stage-0 text: even the first point's fractal depends
on your stage-0 label, and stage *k+1*'s fractal cannot even be derived until
stage *k*'s point is fixed. There is **no public fractal** an attacker can know
in advance.

Each next-stage fractal **does not exist** until its computation finishes.
No one — not even a fully cooperative user — can reveal the later locations
any faster, because there is nothing to point at until Argon2 is done, and
the chain must be walked in order.

This is why coercion fails: the user **cannot verbalize** their fractal
locations (tacit knowledge), and the later-stage fractals **cannot be
materialized** without completing the full Argon2 chain. Coercing the user
into giving up the entire secret effectively requires kidnapping them for at
least as long as the total Argon2 delay — and that delay compounds across the
chain (one memory-hard derivation per point stage). That is the wall.

## Burning Ship Seed Encoder (`burning_ship/`)

Bijective mapping between BIP39 mnemonic seeds and locations in the
Burning Ship fractal, using I4F60 fixed-point arithmetic (60 fractional
bits, range [-8, +8)).

Because the protocol uses exactly one 32-bit point per (later) stage,
`N = entropy_bits / 32 = words / 3` point stages atop a mandatory, point-less
stage 0 (total stages `N + 1`), so **every** BIP39 size that is a multiple of
32 bits is supported uniformly — one extra point stage per extra 32 bits
(3 words). All sizes from 32 to a hard cap of **256 bits** are offered, and
**every** point stage's fractal is secret and chain-derived (there is no
canonical fractal):

| Words | Entropy | Point stages (N) | Total stages (incl. stage 0) | Tier |
|------:|--------:|-----------------:|-----------------------------:|------|
| 3     | 32      | 1                | 2                            | sub-standard |
| 6     | 64      | 2                | 3                            | sub-standard |
| 9     | 96      | 3                | 4                            | sub-standard |
| 12    | 128     | 4                | 5                            | standard (default) |
| 15    | 160     | 5                | 6                            | standard |
| 18    | 192     | 6                | 7                            | standard |
| 21    | 224     | 7                | 8                            | standard |
| 24    | 256     | 8                | 9                            | standard |

**Hard cap at 256 bits / 24 words.** Larger mnemonics are valid BIP39 in
principle but are deliberately *not* offered: one more stage is the same
marginal mental effort for diminishing returns, so the better lever past 24
words is **more between-stage Argon2 iterations**, not more stages. (A future
"advanced pepper" field — pepper = a prior setup's result — could chain
multiple setups for anyone with a specific reason to exceed 256 bits; see the
design docs' next-steps.)

**Single Argon2 iteration count per setup, calibrated on-device.** To avoid
parameter explosion, one iteration count `N` is fixed at setup and applied to
**every** stage. `N` is the durable parameter; wall-clock "hours" is only a
*perishable label* on it — recovery reproduces the digest from `N`, so hardware
progress changes how long a given `N` takes, never correctness or security. The
interface offers a few **target durations** and calibrates `N` on the user's own
device. `N` is the **user's responsibility to memorize** (for hard recovery if
the device is lost); the protocol gracefully stores the sequence of intermediate
results so an approximate memory of `N` suffices (recognize the correct one).
Users are encouraged to set the time **conservatively (≈2×)** and then use the
TLP / jade-clock layer (see the `great-wallet` family) to tune the effective
per-session delay. Official policy; may be revisited.

**A note on the 32-bit (3-word, single-point) mode.** With stage 0 plus a single
point stage, it still runs the memory-hard chain — stage 1's fractal is derived
from stage-0 text — so even here there is **no public canonical surface**. Its
coercion-resistance is *minimal but still nonzero*: a wrench attacker who lacks
a Great Wall–compatible app still fails, and the setup outperforms the
brute-force resistance of a 9-decimal-digit PIN. It is offered for completeness;
128 bits (12 words) remains the recommended default.
