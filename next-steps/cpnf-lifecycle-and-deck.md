# CPNF — setup lifecycle, deck model, and post-graduation self-custody

> Design note. Extends `great-wallet/ARCHITECTURE.md §4 celestial-peace-nf-core`.
> CPNF trains and maintains recall of a Great Wall setup. It has two phases —
> **pre-graduation** (still propped up by an external provisional key) and
> **post-graduation** (the setup secures itself). The cryptography of the setup
> itself is unchanged; CPNF is a study/maintenance layer on top of it. The
> buildable first slice is `cpnf-step1-scheduler.md`.

## 1. Pre-graduation — study against the provisional-key ciphertext

Until graduation (the user's brain has consolidated the setup), the setup lives
only as a **ciphertext backup encrypted under the provisional key** (the
existing bootstrapping key — see
[`provisional-key-bootstrapping.md`](provisional-key-bootstrapping.md)). In this
phase the user may study **as often as they like** — there is no TLP gating yet
— though following the CPNF (SM-2) schedule is recommended for good
consolidation. (SM-2 = P. A. Woźniak's SuperMemo algorithm, 1990:
<https://www.supermemo.com/en/archives1990-2015/english/ol/sm2>; cite it in docs
and code, don't paraphrase from memory.)

**CPNF consumes the encrypted setup file** to deliver the *same* stages the user
created, with **one crucial difference: the canonical island is NOT
highlighted.** This is not a security measure — it protects the **validity of
the memorization exercise**: showing the island first would test recognition of
a freshly-drawn marker, not genuine recall. CPNF decrypts the stored point only
to *validate* the user's located point, never to display it.

## 2. The deck — what a setup's Anki deck tracks

One deck per setup. It tracks a recall **score** (SM-2 state) for each of:

- **Each stage's point recollection** — the stored point is used to grade the
  user's unaided attempt (highlight off, §1).
- **Memory profile `m`** — must be recalled **exactly** (wrong profile ⇒ wrong
  Argon2 digest ⇒ every fractal breaks).
- **Initial salt / pepper** (the stage-0 input).
- **Number of derivation steps between stages (`N`)** — exact-recall fact; the
  practical safety net for imperfect memory is *adjust-`N`-on-open-setup*
  (roadmap §3a), not any "approximate" special-casing here.
- **(bonus) Download provenance** — official repo / app-store id / a Bitcoin
  block height pinning the release, enabling a **supply-chain-resistant hard
  reset** (re-obtain a trusted build, not whatever a coercer hands you).
- **Per-stage user-defined export salts** — including the salt for CPNF's *own*
  setup (§3).
- **(optional) Miscellaneous reminders** — anything the user wants
  memory-insured, GW-related or not: "custody address of Shamir share #1",
  password-manager name, password-manager login (its master password presumably
  yielded by GW + an export salt), "wedding anniversary", …

### Storage model — uniform encryption

**Everything in a deck is encrypted uniformly** — the provisional key
pre-graduation, or GW-own-legs keys post-graduation (§3) — **including each
stage's points**, since CPNF needs the true point to grade recall accurately.

- **Tacitness / coercion-resistance is preserved by the encryption**, not by
  omission. Pre-graduation the external provisional prop guards the points;
  post-graduation the key is derived from the very secret the point encodes, so
  decrypting a stored point already presupposes reproducing it. Storing it grants
  an attacker nothing.
- **Deferred nuance (not implemented now).** Some cards are inherently less
  sensitive — a *salt* (a public-ish initial input) less than a *pepper* (a
  secret one) — so parts of a deck could in principle tolerate weaker storage.
  That tiering is a rabbit hole we are not digging now: **uniform encryption for
  everything.**

## 3. Post-graduation — "setup standing on its own legs"

1. **The provisional key is destroyed.** The external prop is gone.
2. **Own-legs key schedule.** CPNF derives its encryption keys from the user's
   *own recalled secret* using a **sequential family of export salts**
   `CPNF-1, CPNF-2, …` — each revision KDFs the next key that encrypts the
   setup (and its deck). Sequential, not fixed, so each revision rotates the key
   (a leaked interval-key does not unlock the next ciphertext). *Cost: one small,
   non-secret piece of state — the current index. If lost it is recoverable by
   trial-decrypt from `CPNF-1`, just slower. The own-legs key is **never**
   independently stored — that is what keeps this self-custody rather than a
   stored-key model.*
3. **Derivation shorter than the maintenance interval → just re-derive each
   time.** Before each scheduled revision, rerun the hard derivation from memory.
   *Example: a 24-hour setup with a one-week interval — every Friday/Saturday the
   user reruns derivation and does the exercise on the weekend.* No TLP needed.
4. **Derivation ≈ or > the interval (or to avoid planning/syncing the
   re-derivation) → RSW-TLP-encrypt the deck.** The TLP setup is itself KDF'd
   from the own-legs secret (§3.2) and is **never written to disk** (or, if it
   must be, only to a **wipeable medium**). It encrypts the GW setup **in place
   of the provisional key**. (Uses `tlp-core` / `jade-clock`.)
5. **Panic button (wrench-attack defense).** On perceived coercion risk, a panic
   button **aborts the sequential squaring** and **wipes the setup from RAM**.
   Recovery falls back to a hard reset (rerun derivation).
6. **Outsourcing the sequential squaring** (untrusted compute). To keep it safe,
   the user does **one** of:
   1. store the GW **ciphertext on an HDD they can physically wipe**; or
   2. make the **RSW-TLP setup necessary-but-not-sufficient** to decrypt GW — a
      second, physically-destroyable provisional key is also required, so the
      outsourced squaring alone never yields plaintext.
7. **Alternatives to outsourcing the squaring** *(to be defined)*:
   1. GW setup lives on **Desktop**, the RSW-TLP setup runs on **mobile**, keys
      pass by **QR scan**; the portable device gives an always-accessible abort.
   2. **Mobile hosts the abort button** for RSW-TLP running on a remote Desktop;
      **loss of the mobile↔desktop connection also triggers abort.**

## 4. Next steps / to define

- **Adjust `N` on an open setup** and **calibration nudging round `N`** — the
  practical recovery path for imperfect `N` memory. Tracked in
  [`chained-protocol-size-and-ux-roadmap.md`](chained-protocol-size-and-ux-roadmap.md)
  §3a.
- **Time-to-clear as a scoring signal (maze-rat analogy).** The wall-clock time
  the user takes to locate each stage's point could feed the card's grade, the
  way maze-solve latency indexes a rat's learning (cf. the framing in
  `ARCHITECTURE.md`). Today the Again/Hard/Good/Easy grades already encode
  attempts + hesitation; this would make **time an explicit, quantitative
  input**. *To be defined.*
- The **§3.7 abort-button topologies** remain *to be defined*.
