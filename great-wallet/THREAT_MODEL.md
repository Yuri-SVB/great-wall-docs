# Great Wall Ecosystem — Threat Model (Draft)

This document records the security assumptions under which the Great
Wall ecosystem operates. The concrete threat-to-mitigation mapping
lives in [ARCHITECTURE.md § Security Model
Summary](./ARCHITECTURE.md#security-model-summary); this document
states what makes those mitigations hold, and what lies outside the
current release's scope.

Status: **first draft**. Parameters, framing, and wording are
expected to evolve alongside the protocol.

---

## Attacker Capabilities (Assumed)

The attacker:

- has full knowledge of the protocol, all source code, the user's
  setup choices, and every in-scope parameter (non-obscurity — one of
  the Four Properties);
- can seize any user device and read all state on it (vault blobs,
  TLP blobs, commitment scripts, SM-2 schedules);
- has unbounded compute within their effective wall-clock custody
  window (see [*Calibrating Argon2
  duration*](./ARCHITECTURE.md#calibrating-argon2-duration)),
  including the ability to hire `jade-clock` solvers;
- runs full Bitcoin and Lightning Network nodes, monitors the chain,
  and can participate in routing;
- may coerce users or heirs physically, for durations bounded by the
  wrench-attack incidents compiled in
  [jlopp/physical-bitcoin-attacks](https://github.com/jlopp/physical-bitcoin-attacks/).

## Trust Base (What Is Assumed Hard)

| Primitive / property                                 | Relied on for                           |
|------------------------------------------------------|------------------------------------------|
| Bitcoin consensus, PoW, secp256k1 signatures         | All on-chain settlement and key pairs    |
| RSA-2048 factoring hardness                          | RSW TLP (training vault, inheritance)    |
| Argon2 at the configured parameters                  | Stage-2 fractal derivation gating        |
| AES / HMAC-SHA512 at textbook strength               | Vault and TLP ciphertext                 |
| Bit-exact `great-wall-core` implementation (Rust, I4F60) | Stage-1 / stage-2 bijection          |
| Standard LN commitment-update + revocation semantics | Dead-man's-switch inheritance channel    |
| Tacit knowledge is non-transmissible (TKBA premise)  | Coercion-resistance (property 4)         |
| SHA-256 preimage resistance / nonce-search optimality (A1) | Bitcoin-nonce salt unpredictability ([`../next-steps/bitcoin-nonce-salt.md`](../next-steps/bitcoin-nonce-salt.md)) |

## Coercion-Resistance Lemmas (the deadly-race framework)

These results fix the *bar* a coercion-resistance protocol must clear. They rest
on a classical premise (0) and then form an escalating chain: each of 1→2→3
follows from the one before. Alternative names are recorded for citation (this
framework is intended material for PhD application / publication).

0. **Kerckhoffs' Principle** (assumed throughout). The attacker **knows the
   protocol** — all algorithms, source, the user's setup choices, and every
   in-scope parameter; only the tacit secret is hidden. (The classical
   security-by-non-obscurity assumption; restated among the Attacker Capabilities
   above. Every lemma below is proved *against* such an attacker.)

1. **Non-Negative-Proof Lemma.** No agent can furnish satisfactorily verifiable
   proof of *lack of access* to a given piece of information — whether that access
   would be through their own brain memory, or directly or indirectly through
   physical media. (You can prove you *know* something; you cannot prove you have
   *forgotten* it, nor that no backup of it exists anywhere.)

2. **Deadly-Race Lemma** (from 1) — *also* **Villas Boas' Lemma**. Because a victim cannot prove they hold no
   backup, no wrench-attack victim can produce a credible promise that they lack
   copies of their Great Wall files on which they could resume the protocol once
   released. Therefore **any wrench attack in which the perpetrator seizes enough
   information to *eventually* reach the master secret — however much slower than
   legitimate use — defines a *race*** between perpetrator (working from the seized
   information) and the released victim (presumed to hold complete information):
   whoever reaches the master secret first seizes whatever it gates. The existence
   of that race introduces a **material incentive for the perpetrator to
   assassinate the victim — and possibly the heirs** (`phoenix-scroll`) — upon
   seizing sufficient information, to eliminate the competing racer.

3. **No-Gray-Area Principle** (from 2) — *also* **Deadly-Race Principle** /
   **Villas Boas' Principle**. A coercion-resistance protocol must,
   **for a given threat model, admit only outcomes in which a wrench attack
   clearly *succeeds* or clearly *fails*.** A protocol in which some wrench-attack
   outcome is a *race* is, by construction, **not acceptable** — the gray area is
   precisely where the assassination incentive lives.

**Remark (reachability — the remote-racer escape).** The assassination incentive in
(2) is *realizable only against a racer the perpetrator can reach*. A racer beyond
physical reach — e.g. a **remote** rescuer/delegate — cannot be eliminated, so their
racing advantage stands and the attack fails cleanly. **Remoteness of the racer is
therefore itself a DRL remediation** — but it buys safety by moving the winning racer
*off the individual*: it requires a trusted third party, i.e. it **gives up individual
custody**. So a design has two honest ways to clear (3): remove the *race* (no feasible
seizure path — Great Wall's recall floor, custody stays individual), or remove the
attacker's *reach* over the racer (a remote delegate — custody becomes shared). The
worked example below is the second kind.

**Operational restatement (the design axiom).** Seizing a device must yield
either *nothing feasible* (clear failure) or *the secret itself while the attacker
is present and the victim captive* (clear success, no free racer) — **never a
feasible-but-slower offline path** that the attacker could pursue after releasing
(or killing) the victim. "Feasible" is judged against the assumed attacker of the
capabilities section, not against a casual one.

**Design consequences (remedies).** The canonical construction that discharges the
No-Gray-Area Principle post-graduation — the `H*(H(·))` orbit, `Sh_i`-polynomial
stages (`t_i ≥ 2`), the cheap terminal `K`, the setup pathway, retirement, forgiving
TLP decks, and the tolerated residual window — is
[`../next-steps/coercion-resistant-orbit-protocol.md`](../next-steps/coercion-resistant-orbit-protocol.md).
(The earlier framings in
[`../next-steps/post-graduation-security-tiers.md`](../next-steps/post-graduation-security-tiers.md)
§6 and [`../next-steps/cpnf-lifecycle-and-deck.md`](../next-steps/cpnf-lifecycle-and-deck.md)
§2 are design history, superseded by it.)

## Engineering Stipulations (the feasibility line)

These fix what "feasible" means for the attacker of the capabilities section, and
turn the lemmas into concrete parameter bounds.

- **S1 (feasible).** `2³²` **cheap** (non-memory-hard) evaluations are within the
  attacker's budget.
- **S2 (infeasible).** `2⁶⁴` **memory-hard** evaluations — each an hours-scale
  Argon2d, written **`64*`** — are beyond it.

*Corollary.* A residual `≥ 64*` clears the No-Gray-Area bar; `32` does not. Two
different currencies span the gap: **entropy** buys `32 → 64` (a second deep stage),
but plain `2⁶⁴` *cheap* work is still within a resourced attacker's reach — so the
`64 → 64*` step is bought **by memory-hardness**, which is why the threshold KDF must
be Argon2 (see `post-graduation-security-tiers.md` §6).

## Applied Theorem — the `64*` floor on the master secret

**T1 (last-stage-KDF is deadly-race-vulnerable).** In a sequential re-derivation
setup whose master secret is `KDF(pₙ)` — determined by the **last** stage alone — a
surprise seizure at stage `N−1` holds the pre-image of stage `N`; deriving it and
brute-forcing `pₙ` costs `2³²` (S1, feasible) → master. By the No-Gray-Area
Principle, rejected.

*General requirement.* The master secret must be **`≥ 64*` from every seizable
state** — i.e. no single seizure may leave it fewer than two memory-hard 32-bit
stages away. *Corrected construction:* this is the **no-single-point-oracle /
block-orbit (`k ≥ 2`)** condition — a bespoke `KDF(p₂, p₄)` is merely the 2-point
instance, and is safe **only if** no seizable intermediate state checksums `p₂` (or
`p₄`) alone (a running seed or an intermediate fractal *does* checksum it, so
"deleting `p₂`" is insufficient). The floor lives in the **deep** stages; see
`post-graduation-security-tiers.md` §6 "The `64*` floor & shallow/deep split." (This
condition is reached independently from the *storage* side — via the sub-threshold
oracle — and from the *deadly-race* side here; the two routes coincide at `k ≥ 2`.)

## Worked example — timelock-rescue wallets (Rewind Bitcoin)

A sanity check on the framework: it should classify a *shipping* design, and it does —
**via the reachability remark, not by calling it broken.** Take **Rewind Bitcoin**
(<https://rewindbitcoin.com/>) as the exemplar; the analysis must be fair to it.

**Mechanism (as advertised).** Funds sit in a Bitcoin-native **timelock vault**;
unlocking starts a multi-day **countdown**; if an unauthorized unlock is triggered, the
owner **or a trusted delegate** has that window to press **"Rescue"** and sweep to a cold
panic address.

**Against remote theft it is sound** — a thief who steals keys trips the countdown, the
owner notices and rescues.

**It *remediates* the Deadly-Race — by the remote-racer escape, at the cost of individual
custody.** The spend capability sits behind **only a delay** (the timelock), keys **on the
seized device**, **no recall floor** — so a wrench attacker who seizes the device does hold
a *feasible path* (unlock, wait out the countdown), and the only thing between them and the
funds is a **rescue by a live, free defender**. That *is* a race. Rewind's answer is to put
the winning racer **out of the attacker's reach**: a **remote delegate** the wrench
attacker cannot find or eliminate presses Rescue, so the attack fails cleanly. This is a
legitimate DRL remediation — but it is the *remote-racer* kind, so its cost is exactly the
one the remark names: **custody is no longer individual** — it now depends on a trusted
third party.

**When the escape closes — both problems return.** The remedy holds *only while the
delegate is genuinely remote*. If the delegate is a **friend who happens to be visiting**
at the time of the wrench attack, then **both** problems apply at once: custody was already
**non-individual**, *and* the racer is now **co-located and reachable** → **deadly-race-
susceptible again** (coerce/eliminate the owner *and* the present delegate). So the design
forces the user into an awkward corner: either **trust someone they can rarely be near**
(remoteness weakens practical availability and the trust relationship), and/or accept a
**perverse incentive to avoid physical proximity to a trusted friend** — lest that friend's
presence re-open the race.

**The structural difference from Great Wall.** Both clear the No-Gray-Area Principle, but by
the two different routes of the remark. Rewind removes the attacker's *reach* over the racer
(remote delegate) → **shared custody**. Great Wall removes the *race itself*: the secret is
tacit, never on the device, so seizure yields *nothing feasible* (`≥ 64*`) — there is no
racer to reach, and the TLP is only a delay *on top of* an already-clean failure. So Great
Wall keeps custody **individual** while achieving the same DRL-safety. **"Put the racer out
of reach" (Rewind, at the price of a trusted third party) vs. "leave no race to run" (the
recall floor, custody intact)** — that is the honest comparison.

## Out of Scope (This Release)

- **Adversarial-agent scenarios.** Testator / heir mutual distrust,
  or third parties maliciously interfering with rotation, require
  stronger monitoring and dispute machinery than this release
  targets. Future iterations may address.
- **Quantum adversaries.** Breaking secp256k1 or RSA-2048 factoring
  via quantum computation is not defended against directly. The
  inheritance path has a post-quantum escape hatch documented in
  [*TLP Enforcement*](./ARCHITECTURE.md#tlp-enforcement-off-chain-key-wrapping).
- **Device side-channels during active recall.** Timing, EM,
  acoustic, and similar attacks on the user's device while tacit
  recall is happening.
- **Long-horizon cryptographic erosion.** Century-plus hardness of
  RSA-2048 factoring and of Argon2 parameters against future
  hardware is not guaranteed.
- **Mass on-chain correlation attacks.** Beyond the privacy afforded
  by standard taproot outputs and private (non-routing) LN channels.

---

## Cross-Reference

See [ARCHITECTURE.md § Security Model
Summary](./ARCHITECTURE.md#security-model-summary) for the concrete
threat-to-mitigation table.
