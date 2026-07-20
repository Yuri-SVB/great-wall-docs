# Next steps — Jade Clock: the outsourced, anonymized post-graduation time-lock

> Captured from design discussion. **Status: design, not yet implemented.** Jade
> Clock is the post-graduation RSW time-lock puzzle (TLP) and, optionally, the
> marketplace that runs it anonymously on the user's behalf. It sits *on top of*
> the recall floor from `next-steps/post-graduation-security-tiers.md` (Shamir
> `t`-of-`n`, the definitive gate); the panic button aborts it, falling back to
> hard reset. Ties to `great-wallet/THREAT_MODEL.md` (coercion, surprise
> seizure), `next-steps/provisional-key-bootstrapping.md` (graduation), and
> `next-steps/cpnf-lifecycle-and-deck.md` §3 (the graduation gate + the
> graduation→first-arming sequence that arms the first clock).

## 0. What Jade Clock is (and is not)
- It is a Rivest–Shamir–Wagner time-lock over the **deck** — which holds the
  `t`-of-`n` Shamir *structure* (fractals `(o,p,q)`, params, schedule) but **not
  the shares** (recall-only). After `T_TLP` it decrypts the deck; **waiting it out
  still faces the `t·32`-bit recall barrier**, because the deck contains no shares.
  So the recall floor is **automatic** (nothing to cap — shares are never stored
  or time-locked), and the clock's real job is the **coercion delay**: it forces
  `T_TLP` even on a cooperating/coerced user before the still-recall-gated vault
  can open. Normal opening is recall + Shamir once the deck is available.
- It is **re-armed at every vault close** and **starts ticking immediately** — so
  the recovery clock's `t = 0` is "last practice," and the memory model (below)
  has a clean origin. Every second the vault stays open is window-of-vulnerability;
  the last action before closing is arming the next Jade Clock.
- Its duration is **calibrated from the setup's SM-2 grades**: solid consolidation
  → **longer `T_TLP`** (rarely needed, so maximize coercion delay); shaky recall →
  **shorter `T_TLP`** (recovery is likelier, keep it quick).

## 1. Two timers, one fallback ladder
| | primitive | wall-clock |
|---|---|---|
| **Jade Clock (TLP)** | repeated modular squaring (RSW) | `T_TLP` (calibrated) |
| **Hard reset** | the Argon2d^D derivation chain | `T_hard = N · t_D` |

`t_D` = the per-link Argon2d^D time you already calibrate for derivation (`D` =
Argon2d **D**erivation steps between stages; `N` = number of stages), so the
**same `D` knob sets the hard-reset cost**. Panic/abort tears down the TLP fast
path and forces hard reset — a "deny rather than delay" option, **not** the floor
(the floor is the recall gate, which needs no user action; see §6).

## 2. Why RSW at all — the frequency ceiling (and its dent)
Sequential squaring **cannot be parallelized**, so no amount of money buys a
dramatic shortcut: device spread is a small factor. This is *the* property that
makes the delay coercion-resistant — it bounds both scenario 2 (a legit slow
device, ~2–5×) and an attacker's speed-up. **Dent:** dedicated modular-squaring
ASICs/FPGAs (the VDF-hardware line) run **~10×** a commodity CPU. So size `T_TLP`
so that `T_TLP / ~10` is still a meaningful delay against a resourced attacker.

## 3. Construction — per-user RSA + trapdoor-precomputed milestone digests
- **Per-user modulus `M_rsa`; factorization destroyed at setup.** (`M_rsa` — the
  RSA modulus — is distinct from `D`, the Argon2 derivation-step count of §1.)
  With the trapdoor the creator cheaply precomputes each milestone `H(m_i)` (via
  exponent reduction mod `φ(M_rsa)`), stores the *digests*, then **destroys
  `φ(M_rsa)`** — after which the puzzle is a genuine time-lock for everyone, owner
  included.
- Milestone **digests attest progress without enabling a skip** (preimage
  resistance) and **without leaking the secret** (hashes). They do **not** enable
  resume (a lost squaring value can't be recovered from its hash) — so "breaks →
  restart or hard reset" stands.
- **`M_rsa` must be the user's, never the company's.** A company-supplied `M_rsa` is a
  universal backdoor. This choice (per-user RSA) is deliberate and *enabling*:
  the trapdoor precompute is what lets the client know `H(m_i)` in advance, which
  is what makes the Lightning payment layer (§4) work. The trustless alternative
  (class-group VDFs, no trapdoor) would force per-batch Wesolowski/Pietrzak proofs
  and an expressive on-chain contract → metadata footprint. RSA wins here.

## 4. Verification & payment — LN-HTLC atomic verify-and-pay
Full fair exchange is impossible with pure crypto and no trusted third party, and
on-chain enforcement leaks metadata. But the **typical case is code-enforced
off-chain**:

- The precomputed **`H(m_i)` is the HTLC hashlock.** The client offers a Lightning
  payment locked to `H(m_i)` and hands the provider the operand `m_{i-1}`. The
  only way to claim it is to reveal the preimage `m_i`, obtainable **only by doing
  the squaring** (no trapdoor in the wild). Provider reveals `m_i` → gets paid;
  the client **learns `m_i` from the settled preimage.** Atomic, off-chain,
  **paid iff correct** — no arbiter for correctness.
- **Correctness + atomic payment = code-enforced; liveness = reputation.** A
  provider that locks and never delivers just times out → funds return → re-
  dispatch + slash. The `1000`-batch × ongoing-market structure is a repeated
  game, so honesty is the equilibrium.

## 5. The marketplace — a dealer that monetizes the residuals
The company is a **dealer (principal), not a broker**: it takes the other side of
each counterparty risk for a **spread**. The spread prices exactly the residuals
that cryptography leaves on the table:

- **Client — sourcing performance:** crypto gives correctness, never *speed*; the
  market supplies a fast provider to meet `T_TLP`, dispatched with **priority
  proportional to the provider's stats**.
- **Client — provider time-out (rare at equilibrium):** the dealer sets the
  client-facing timeout **long enough to hire a provider *and* bail out** — if the
  provider times out, the dealer **does the squaring itself** in its place. So the
  client always completes; the time-out is the dealer's problem, not the client's.
- **Provider — malformed / bogus request** (`H(squarings(m_i)) ≠ h_{i+1}`):
  **no client bond.** On a provider's complaint the dealer **verifies it** (it can
  re-square the one disputed batch itself — the same bail-out capability), then:
  - provider in the right ⇒ **ban the client** (hostile LN channel force-close);
  - client in the right ⇒ **slash / ban the provider** (same).
- **Provider stats:** incremented on success, slashed on time-out or false
  complaint; dispatch priority tracks the stats.

**Why no bond:** the **sunk cost of opening an LN channel** already makes bad
behavior / DoS **anti-economical** — a banned party must open a fresh channel to
return, so griefing costs more than it yields. Deterrence comes from channel
sunk-cost + slashing (a 3-strikes-style rule), not upfront capital.

**Redundancy (optional feature):** the dealer can **duplicate a client's request
across providers** — first valid result wins — to raise **availability and
speed**. An availability/latency upsell.

**Load-bearing: separate the risk/payment plane from the data plane.** A principal
that *relays batches* would hold every milestone → it could complete any user's TLP
and **decrypt their deck** — not the shares (recall-only), but the deck's
*metadata* (that a setup exists, its shape/size/schedule), a deanonymization
break. So the company brokers **matching + payment + reputation** (sees LN
metadata) while the squaring **payload flows client ↔ provider directly through
the mix** (company blind in the typical case); disputes escalate only the *single*
contested batch. Keep these planes separate or the dealer quietly becomes a
universal backdoor.

**Three mutually-reinforcing flywheels:**
- **Anonymity:** more adoption → bigger anonymity set → more adoption.
- **Reputation:** more adoption → more reputation (marketplace + vetted providers)
  → more adoption.
- **Intel:** more adoption → more client/provider **operational** stats
  (performance/liveness/quality — not use or identity) → better matching &
  efficiency → better quality → more adoption.

## 6. Anonymity — three linkage vectors, plus cover traffic
Uniform, standardized batch size/cadence is itself an anonymity requirement (a
non-standard shape is a fingerprint — cf. fixed-size Tor cells). Three vectors,
each needing its own layer:

- **Content** → **chain-encryption**: `m_i` (via KDF) encrypts batch `i+1`'s
  operand/params, so an observer can't see the linkage and the chain is
  *cryptographically* serialized (you can't dispatch `i+1` before `i` returns).
  Composes with the HTLC (the revealed preimage both claims payment and unlocks
  the next operand). Note: links only accumulate `T_TLP` if crypto-chained end to
  end — parallel links give `max`, not `sum`.
- **Timing** → **cover traffic (dummy chains)** — but *who it hides you from
  differs by adversary*, because each user is a **distinct LN node with its own
  direct channel to the dealer** (the Phoenix↔LSP topology). So:
  - **The dealer** sees your channel/node, so it attributes every batch to *you* —
    **community cover cannot hide you from it** (no shared channel exists, and its
    being your first hop denies even LN onion source-privacy). Against the dealer
    the model is **trust (the VPN bargain)**, plus the structural facts that it
    still can't tell *which* of your chains is real or *which* result you consume
    (consumption is offline). If you also want to hide your *completion timing*
    from the dealer, only **your own** dummies on your own channel do that, and
    that cost does **not** shrink with adoption.
  - **Providers and external/network observers** get real **community cover — not
    from a shared channel but from the dealer's *dispatch*:** it pools all users'
    batches and hands the provider pool an *unattributed* stream (providers are
    paid by the dealer, never see the user), and Tor blends the outside view. To
    everyone *beyond* the dealer you're mixed into the whole user base, so here
    **per-user self-cover → 0 as adoption grows** (the crowd keeps the aggregate
    flux uniform). This is exactly the VPN model: your provider sees you; the world
    sees the crowd.
  Dummies must **run to completion** (an abandoned chain is a tell). Uniform flux
  implies effectively **always-on** cover (presence is a signal) → a steady cost
  vs. a cheaper bursty-with-padding mode. And **never rush the real chain to hit
  its deadline** — size it to finish at the *standard* rate over `T_TLP`, all
  chains at the same rate.
- **Payment** → **Lightning**, routed through the company (its LN-provider hat):
  off-chain, no on-chain footprint, and it *is* the HTLC rail. Caveat: a company
  that is both marketplace and LN hub sees both legs → it is the **residual
  correlation point** (VPN bargain). Mitigate the VPN way: uniform amounts,
  timing jitter, optional multi-hop.
- **Transport/network** → **Tor by default.** The LN wallet must connect over Tor
  out of the box (as Phoenix, Breez and other LN wallets already do), so neither
  the company nor a network observer can tie LN traffic to the user's IP. This is
  a distinct, fourth linkage vector (network layer), not covered by the payment
  mitigations above. **Necessary but not sufficient:** Tor removes the *IP*, but
  the company-as-LSP still sees the *LN-layer* graph — a persistent node
  identity/channel set can re-link you across sessions even over Tor. So pair Tor
  with node-identity hygiene (rotate/unannounced channels where feasible) and the
  amount/timing standardization above; the VPN-trust caveat in the payment bullet
  survives Tor.

## 7. The three tuning knobs
```
squaring → batch (knob 1: squarings/batch)     ← the HTLC / verify unit
         → link  (knob 2: batches/chain-enc)    ← content-linkage hidden; unlock-serialized
         → delay (knob 3: links/delay)          ← composed to the programmed T_TLP
```
Finer (smaller batches, more links, more cover) = better attestation +
decorrelation + cover granularity, but more key-gen precompute + HTLC/verification
+ cover cost. Coarser = cheaper but blunter. These are the dials on the
cost / anonymity / attestation surface.

## 8. Skipping the clock gains only the deck, not the shares
Even a coercer who deanonymizes, seizes in-window, and blocks the panic abort, and
so **skips the clock** via the stored current milestone, gets only the **deck
structure** — never the shares (recall-only). So they still face the full
`t·32`-bit recall barrier; skipping buys them nothing beyond the non-secret
structure they'd face anyway. The genuinely exposed state is an **open** vault
(the recall is in RAM). Cloaking imminent completion (§6) therefore matters not
because skipping leaks secrets, but because it lets an attacker **predict when the
user will next be open** and time a strike to that window — so close promptly and
keep the completion schedule hidden.

## 9. Recovery-outcome model (the TLP-setting display)
For a chosen `T_TLP`, show the probability/time of each outcome. Two independent
uncertainty sources: **TLP timing** (hardware squaring-rate variance, §2) and
**memory** (`R(T) = r*^(T/I)` from cpnf-lifecycle, per stage):

1. **On time** — recover at `T_TLP`; `P(actual ∈ window)`, hardware model.
2. **×k slower — extra delay, nothing lost.** `~k·T_TLP` (any multiplier, not just
   2×). Two sources land here: (a) *involuntary* — hardware slower than benchmarked
   (slow tail of §2; also show the fast tail — a faster attacker is the *security*
   side); and (b) *voluntary* — the **soft panic** (§below): rewinding the TLP to a
   target milestone (typically 0 = restart) **keeps the deck and the Shamir
   bail-out**, so the only cost is the re-injected squaring delay. Deck + floor
   intact.
3. **Hard panic → hard reset.** The user **wipes the TLP-encrypted deck** on
   perceived imminent wrench attack near completion. This destroys everything on
   the device (even the deck *metadata*), so recovery is *obligatorily* hard reset,
   landing at **`T_TLP` (invested, worst case ≈ full) `+ T_hard`**. A deliberate
   *deny* trade: sacrifice the invested time and accept a hard reset so the
   attacker gets nothing — a wiped clock **and** a hard reset that needs your
   recall (not on the seized device). Recovery *success* is the directional
   hard-reset memory model below; the `T_TLP` is simply spent. (An accidental
   last-second hardware loss lands at the same cost, minus the intent.)

**Two panic levels (graduated response).** The panic button is not binary — it
matches the response to the threat, and the two rungs are exactly scenarios 2 and 3:
- **Soft — reset TLP progress to a target milestone, keep the deck.** *Buys
  delay.* Pushes completion back so you're not in the open/vulnerable state when a
  threat is near; the deck stays TLP-encrypted and the Shamir bail-out is kept, so
  when it's safe you just wait out the (restarted) clock. Cost ≈ scenario 2 (the
  re-injected delay). Rewind-to-0 is always possible (restart from the public
  start); rewinding to an intermediate milestone needs that milestone retained.
- **Hard — wipe the TLP-encrypted deck.** *Denies.* No deck ⇒ no TLP, no stored
  structure ⇒ mandatory hard reset (scenario 3). Maximum denial (attacker gets not
  even deck metadata), maximum cost.

This mirrors what a TLP defense actually offers: the soft rung is **delay** (rewind
the clock, lose only time), the hard rung is **denial** (destroy the deck, force a
recall-gated hard reset).

**Caveat — the soft rung assumes no collusion.** A client-side rewind discards only
the *client's* copy of the progress; an **outsourced squarer (provider/dealer) that
was computing it retains the pre-reset milestone.** So the re-injected delay is
*illusory* against a colluding squarer. The full attack requires all of:
1. a provider/dealer **deanonymizes** the client — which is really *two* linkages,
   both required: **(1a) who** — linking an LN channel / chain to the prospective
   victim's real identity; and **(1b) when** — mapping out their **vault-opening
   schedule** (the completion timing that reveals the window of vulnerability). One
   without the other is inert: knowing *who* but not *when* leaves the attacker
   without a moment to strike; knowing *when* but not *who* leaves them without a
   target;
2. it **colludes** with a surprise wrench attacker;
3. the client chose **soft** (kept the deck); and
4. the attacker **seizes the TLP-encrypted deck**.
Then the colluding party hands over the near-complete milestone, the attacker
**opens the deck during the attack**, and coerces the victim into clearing `t`
stages → **the wrench succeeds.** (More generally, against a *present* wrench
attacker the soft rung buys at most `T_TLP` — they can simply wait while holding
the victim; collusion + near-completion erases even that.)

**The hard rung rules this out** — no deck ⇒ no fast reconstruction path ⇒ even
*coerced* recall forces the attacker through a full `T_hard` hard reset, with no
fast feedback (so decoys stay viable), buying rescue time. The price is the legit
user's own hard reset. So: **soft = delay against a remote seizure; hard = the only
real defense against a present or colluding wrench attacker.** (Running the squaring
**locally** removes the collusion vector entirely — no external party holds the
progress — so soft reset is effective there; the vector is specific to outsourcing,
and local squaring is the standing escape.)

**This is where anonymity earns its keep as a *product*, not just a privacy
nicety.** Every step of the collusion attack is downstream of **step 1 —
deanonymization**: a squarer that cannot bind a chain to a client's identity (or
correlate its completion timing to a real person) can never *be* the "colluding
party" that hands a wrench attacker the near-complete milestone, no matter how
willing. So the anonymity guarantees of §6 — per-provider blindness via the
dealer's dispatch pooling, Tor transport, community cover traffic, and the
dealer's own **structural ignorance** (it relays squarings/payments and stores
nothing that maps a chain to a person) — are not decoration; they **sever link 1
of the only chain that defeats the soft rung.** Anonymity-as-a-service therefore
does real security work: it keeps the *soft* panic rung viable against outsourced
squaring by making the collusion precondition unsatisfiable.

Splitting deanonymization into **who (1a)** and **when (1b)** shows *why the
specific anonymity mechanisms exist* — each attacks one linkage:

- **Dummy requests — defeat (1b), the schedule.** A steady baseline of decoy
  squarings **cloaks the window of vulnerability**: a squarer watching request
  volume/timing cannot tell a real vault-open cadence from cover, so it cannot map
  *when* the client is exposed. (This is the timing half of §6's cover traffic,
  aimed squarely at the completion-timing leak.)
- **One TLP-setup → many chain-encrypted setups — defeat (1a)+(1b), unlinkability
  of batches.** Breaking a single client's TLP into **multiple chained sub-setups**
  means a provider sees a stream of batches it **cannot partition** — batches from
  *different* clients look the same as batches from *one* client. It can neither
  bind a coherent chain to one identity (1a) nor reconstruct that identity's true
  completion schedule (1b), because it never knows which batches belong together.
- **Reputation flywheel / first-mover moat — makes non-collusion the *incentive*.**
  Even where blindness is only partial (the dealer on a per-user channel), a
  **reputed dealer's standing as a non-colluding relay is its most valuable asset**:
  one provable betrayal destroys the franchise. First-mover reputation thus
  *economically* secures the very non-collusion the crypto can't fully guarantee —
  the moat and the security property are the same thing.

(The residual is the dealer itself on a per-user LN channel — see §6: against the
dealer, blindness is a trust/VPN assumption, not a cryptographic one, which is
exactly why the reputation moat matters there; local squaring remains the
zero-trust floor, and the hard rung remains the unconditional defense.)

### Scenario 3 is directional (this is the subtle part)
Hard reset re-derives the chain from zero with **no stored fractals**, and
`fractal_k = H(text ‖ points 1..k−1)`, so you can only obtain `point_k` after
resolving `1..k−1`. Consequences:
- **No per-stage oracle — this is far worse than a clean `2³²` bail.** With the
  **deck present** (normal recall / Shamir bail-out) a single forgotten stage costs
  a clean `2³²`: you render the *stored* fractal and test guesses against the
  over-sampled shares / AEAD — a **cheap per-stage oracle**. At hard reset there are
  **no stored fractals and no per-stage oracle** — the *only* correctness signal is
  the **terminal AEAD**, reached only after resolving the entire chain. So a stage
  forgotten at depth `j` **from the end** cannot be brute-forced in isolation: each
  of its `2³²` candidates must be **carried forward through all `j−1` downstream
  Argon2d^D inter-stage derivations to the terminal** before it can be judged — cost
  ≈ `2^(32·j)` guesses × `(j−1)` chained hard derivations apiece. For `j = 1` (only
  the very last stage lost) this is a bounded `2³²` sweep against the terminal; for
  **`j > 1` it is combinatorially and computationally game over.** (Recalled *late*
  stages still can't rescue a forgotten *early* one — Shamir's "any `t`" symmetry
  needs the deck; without it, resolution is strictly prefix-ordered along the fixed
  deterministic orbit, not reorderable.) The earlier `2^(32·f)` figure was the
  *deck-present* cost and does **not** apply here.
- **The only Hail Mary — both parts required, feasible for ~one forgotten stage.**
  1. **Narrow the space** (feature not yet implemented —
     [`hard-reset-area-narrowing-recovery.md`](hard-reset-area-narrowing-recovery.md)).
     If the user has *partial* recollection of roughly where a stage's point sat,
     they draw include/exclude rectangles; bisection exhausts that region into its
     leaves, shrinking that stage from a `2³²` sweep to a handful of leaf-area
     candidates.
  2. **Human perceptual oracle on the *next* stage.** If step 1 leaves few enough
     candidates, hash each into the **next** stage's fractal and let the user
     **perceptually recognize** which one renders a familiar / findable board —
     substituting for the missing algorithmic oracle. This is contingent on **both**
     the human verifiability of the candidates *and* the feasibility of computing
     all the inter-stage hashes. Applied across **more than one** forgotten stage it
     fans the candidates into a cross-product and multiplies the derivations —
     **throwing both feasibilities out of the window.** So practical hard-reset
     tolerance is **at most one** forgotten stage, and only with partial recall.
- **Timing:** stage `i` surfaces at `T_TLP + T_hard·(i/N)`; a fully-recalled
  reconstruction completes at `T_TLP + T_hard·(t/N)` (plus the Hail-Mary sweep for a
  single forgotten stage; more than one is effectively unrecoverable).
- **Age gradient (self-cancelling, and free to compute):** the first `t` stages
  are the oldest / longest-practiced, so their `p_forget` are smallest — the
  stages that *solely* decide hard-reset feasibility are the best consolidated,
  and they surface earliest (least extra decay). Use each card's **actual** SM-2
  interval for its `p_forget` (not a uniform `Ic`), which captures whatever the
  true gradient is. (The gradient is automatic for incrementally-grown setups;
  read it off intervals regardless.)

## 10. Guardrails
- **The marketplace is an enhancement, never a dependency.** The wallet must
  recover if the company vanishes or is censored — the user can always **self-run
  the squaring** (slower, less anonymous) or fall to **hard reset**. Local
  squaring is the standing escape hatch that keeps the company honest.
- **Risk/data plane separation** (§5) is mandatory, not optional.
- **Scope boundary:** cover traffic cloaks the *compute flux / vulnerability
  window*, **not** the eventual **on-chain spend**. Linking "a chain completed
  ~now" to "coins moved ~now" is coin-privacy analysis — a separate layer, out of
  Jade Clock's scope, and must not be assumed away.

## 11. Product strategy & operating posture (the business layer)

**Rationale.** The service is deliberately *centralized, simple, and
non-load-bearing*:
1. **Simple** — also a security property (small, auditable surface).
2. **Bitcoin-centric** — LN/BTC only; no token, no securities baggage; matches
   the users' ethos.
3. **Delivers real value** — monetizes genuine residual-risk absorption, not
   speculation.
4. **Sellable to investors** — a spread-earning company with a network-effect
   moat captures value a bare protocol can't.
5. **Flywheel** — more users → bigger anonymity set + provider pool + reputation
   → more users.
6. **State resistance via jurisdiction optimization** — *necessary but weak
   alone*; it only holds because of (a) the non-load-bearing guardrail (seizing
   the company can't touch funds) and (b) **data-minimization** ("we can't
   produce what we don't hold").
7. **Credible exit** — the protocol is open and the wallet is provider-agnostic,
   so users dissatisfied with centralization can replicate the model or deploy
   decentralized alternatives (and that pressure keeps the operator honest).

**The single linchpin behind 6, 7, and the guardrail:**
> **Open protocol + provider-agnostic wallet + company never load-bearing for
> security.**

**The red line.** The failure mode is letting growth/monetization make the
company *load-bearing* — vault custody, KYC, data retention, a wallet that only
works with this service. That breaks 6 **and** 7 simultaneously (the state gets a
real target *and* users lose their exit). "Never a dependency" is therefore a
*business-survival constraint*, not just an architecture note.

### Operating posture — the dumb pipe
The company is **an anonymous pay-to-modular-square relay. Full stop.** Collect no
data, store even less; relay the squaring requests, relay the responses, settle
the payments, collect the spread. A subpoena yields only a bunch of uninformative
LN logs and cryptographically opaque RSW-TLP setups. Five thorns keep this real:

1. **Structural ignorance, not willful blindness.** "I *cannot* know," not "I
   don't *want* to know" — the latter is treated as knowledge in law. Architect
   inability; never market refusal.
2. **Payments are the regulatory fault line, not the data.** Relaying value can
   classify you as a money transmitter (MSB/AML) regardless of logging. Cleaner
   frame: **compute reseller** (buy squaring wholesale, sell retail — a markup on
   a good, not a payment fee), ideally with sats settling **P2P (client↔provider
   HTLC) off your path.**
3. **"Uninformative logs" only under log-nothing discipline** — retained
   per-payment timing/amount is *correlatable* (re-threads chains). Persist
   ephemeral/aggregate only; enforce in code.
4. **They can kill you, not read you.** Sanctions/de-banking can end the business
   even with spotless data — survivable *only* because the guardrail makes the
   company expendable (funds + function stand via local squaring).
5. **Pure relay trims default arbitration.** "Know nothing" conflicts with
   "arbitrate disputes"; make disputes **opt-in reveal** (user submits the one
   contested batch) and justify the spread on liquidity + matching + anonymity +
   SLA, not default visibility.

### Dual-use (why "content-neutral" is real, not a fig leaf)
Repeated modular squaring / VDFs are genuinely dual-use: **public randomness
beacons** (unbiasable RNG, leader election), **sealed-bid auctions** (bids locked
till close), **timed-release / timelock encryption** (escrow, vesting, embargoed
disclosure, inheritance), **MEV / fair ordering** (front-running-resistant
mempools), **timestamping / timed commitments** (fair signing, post-close
e-voting), and **non-parallelizable anti-spam**. Honest caveat: the *primitive*
is broadly dual-use while the *specific product* (anonymous outsourced pay-per-
batch squaring) fits time-lock consumers best — but time-locks are themselves a
broad, legitimate category of which coercion-resistant custody is just one member;
don't overclaim a large non-GW user base, claim *content-neutrality*. The
reinforcing point: a squaring batch for an auction, a beacon, and a Great Wall
vault are **byte-identical**, so the operator *cannot* distinguish them — the
dual-use is precisely what makes the structural ignorance (thorn 1) literally
true.

**The pitch / legal one-liner:**
> "We sell verifiable sequential compute — VDFs and time-locks — a primitive used
> for randomness, auctions, fair ordering, and timed release. We can't distinguish
> one customer's use from another's, by construction."

**Compressed operating principle:**
> A compute reseller of a dual-use primitive, architected so it structurally
> cannot know its use, off the money-movement path, retaining nothing — and
> expendable by design.

## 12. Open decisions
1. `T_TLP` calibration curve from SM-2 grades (solid → longer; shaky → shorter) —
   the exact mapping.
2. Cover mode default: always-on (max anonymity, steady cost) vs bursty-padded.
3. Knob defaults (squarings/batch, batches/link, links/delay) as a **universal
   standard** (uniformity = anonymity).
4. Payment-privacy hardening beyond single-hop-through-company (multi-hop? amount
   standardization?). Transport is settled: **Tor on by default** (§6); open part
   is LN node-identity hygiene (channel rotation / unannounced channels).
5. Does Jade Clock ship as a *self-run* feature first, with the marketplace as a
   later, opt-in layer? (Consistent with the "enhancement, not dependency"
   guardrail.)
