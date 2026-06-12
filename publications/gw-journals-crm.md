# Great Wall (GW) — Journal Submission CRM

A lightweight tracker for managing paper submissions to peer-reviewed venues
relevant to **Great Wall**: a coercion-resistant security protocol based on
**Tacit-Knowledge-Based Authentication**, combining memory-hard key derivation
(Argon2), time-lock puzzles, fractal-encoded secrets, and Bitcoin self-custody.

_Last updated: 2026-06-12_

## How to use this CRM

1. Pick a target venue from the **Venues** table whose scope matches the paper's
   angle (cryptography / systems security / usable security / blockchain /
   economics).
2. Log the live manuscript in the **Submission pipeline** table and advance its
   status as it moves through review.
3. On a reject, move to the next-best venue in the same angle (see the
   `Angle` column).

## Strategy — first publication (and grant backup)

A first paper and a grant-backing credential pull on two different clocks: a
**citable artifact now**, and a **peer-reviewed credential by the grant
deadline**. The plan optimizes both with a pair of moves rather than one venue.

1. **IACR ePrint — immediately.** Post the cryptographic core to stake priority
   and produce a permanent, citable artifact the grant proposal can reference
   this cycle. Not peer-reviewed, so it is the companion, not the credential.
2. **Financial Cryptography & Data Security (FC) — lead venue.** Most strategic
   *first* peer-reviewed home: it spans crypto, systems security, and the
   economic/usability angles, so Great Wall fits whole; it is A-tier and
   committee-legible (matters for CNPq/FAPESP/CAPES-style ranking) without being
   a coin-flip; and it rewards exactly the novel-construction + threat-model
   narrative Great Wall offers.
3. **Fast insurance for a hard deadline — Computers & Security or Ledger.** Run
   in parallel only if a fixed grant deadline needs a guaranteed DOI'd,
   peer-reviewed paper in hand before FC's annual cycle resolves.

**Fork:** if the human-factors study (memorability / re-pointing reliability /
coercion-robustness of tacit fractal locations) is the more finished piece,
swap the lead venue to **SOUPS** — the single best *fit* for the
tacit-knowledge thesis — and keep FC for the systems/crypto follow-up.

**Avoid for the first + grant-timed paper:** top-4 security conferences
(S&P/CCS/USENIX/NDSS) — long cycles, high variance, expect more maturity than a
v1 — and pure-theory journals (Journal of Cryptology, Designs Codes &
Cryptography) — slow, and they strip the systems/usability story that makes the
work compelling to a panel. Reserve both for the flagship follow-up.

Working drafts live in per-paper directories alongside this CRM (e.g.
`publications/01-fc-coercion-resistant-tacit-knowledge-auth/`).

## Status legend

- **Idea** — candidate venue, not yet contacted
- **Preparing** — manuscript being tailored to this venue
- **Submitted** — under editorial / peer review
- **Revision** — major / minor revisions requested
- **Accepted** — accepted for publication
- **Published** — in print / online
- **Rejected** — declined (consider next venue)

## Why these venues fit Great Wall

The protocol sits at the intersection of several fields, so the CRM is grouped
by **angle** — submit the same core idea to whichever community the specific
paper speaks to:

- **Crypto theory** — memory-hard functions, time-lock puzzles, KDF analysis
- **Systems security** — protocol design, threat models, coercion resistance
- **Usable security / HCI** — tacit knowledge, memorability, human factors
- **Blockchain / fintech** — Bitcoin self-custody, key management, wallets
- **Economics of security** — incentive analysis, attacker/defender cost models

## Venues (journals first, then flagship conferences)

| # | Venue | Type | Publisher | Angle | Open Access | Impact (≈) | Status | Notes / Next action |
|---|-------|------|-----------|-------|-------------|-----------|--------|---------------------|
| 1 | Journal of Cryptology | Journal | IACR / Springer | Crypto theory | Hybrid | ~3 | Idea | Best home for memory-hard / TLP formalism |
| 2 | Designs, Codes and Cryptography | Journal | Springer | Crypto theory | Hybrid | ~1.6 | Idea | For the encoding/bijection math |
| 3 | IEEE Trans. Information Forensics & Security (TIFS) | Journal | IEEE | Systems security | Hybrid | ~7 | Idea | Top security journal; broad fit |
| 4 | IEEE Trans. Dependable & Secure Computing (TDSC) | Journal | IEEE | Systems security | Hybrid | ~7 | Idea | Strong for protocol + threat model |
| 5 | ACM Trans. on Privacy and Security (TOPS) | Journal | ACM | Systems security | Hybrid | ~3 | Idea | Rigorous, archival systems-security |
| 6 | Computers & Security | Journal | Elsevier | Systems security | Hybrid | ~5 | Idea | Fast, applied; good fallback |
| 7 | International Journal of Information Security | Journal | Springer | Systems security | Hybrid | ~3 | Idea | Solid mid-tier archival venue |
| 8 | Cryptography | Journal | MDPI | Crypto theory | Gold OA | ~1.6 | Idea | Fast OA; verify indexing/APC |
| 9 | Ledger | Journal | Univ. of Pittsburgh | Blockchain / fintech | Diamond OA | n/a | Idea | Peer-reviewed cryptocurrency journal — ideal for self-custody framing |
| 10 | ACM Trans. Computer-Human Interaction (TOCHI) | Journal | ACM | Usable security / HCI | Hybrid | ~5 | Idea | For the tacit-knowledge / memorability study |
| 11 | Behaviour & Information Technology | Journal | Taylor & Francis | Usable security / HCI | Hybrid | ~4 | Idea | Human-factors of authentication |
| 12 | IEEE Security & Privacy (Magazine) | Magazine | IEEE | Systems security | Hybrid | ~2 | Idea | For an accessible overview / position piece |
| 13 | IEEE Symposium on Security & Privacy ("Oakland") | Conf. | IEEE | Systems security | — | flagship | Idea | Tier-1; reserve for the flagship result |
| 14 | ACM CCS | Conf. | ACM | Systems security | — | flagship | Idea | Tier-1; protocol + crypto fit |
| 15 | USENIX Security | Conf. | USENIX | Systems security | OA proceedings | flagship | Idea | Tier-1; systems + usable tracks |
| 16 | NDSS | Conf. | Internet Society | Systems security | OA proceedings | top | Idea | Tier-1; strong for deployable protocols |
| 17 | SOUPS (Symp. on Usable Privacy & Security) | Conf. | USENIX | Usable security / HCI | OA proceedings | top | Idea | **Best fit** for tacit-knowledge usability study |
| 18 | Financial Cryptography & Data Security (FC) | Conf. | IFCA / Springer | Blockchain / fintech | Hybrid | top | **Preparing** | ⭐ Chosen lead venue for first paper — see `01-fc-...` dir |
| 19 | Workshop on the Economics of Information Security (WEIS) | Workshop | — | Economics of security | OA | top | Idea | For the coercion-cost / incentive analysis |
| 20 | IACR ePrint Archive | Preprint | IACR | Crypto theory | OA (preprint) | n/a | **Preparing** | ⭐ Post first — priority + citable artifact for grant proposal |

## Submission pipeline (active)

| Paper title / working ID | Target venue | Angle | Status | Submitted | Editor / Ref # | Decision due | Owner |
|--------------------------|--------------|-------|--------|-----------|----------------|--------------|-------|
| **P1 — "Great Wall: Coercion-Resistant Tacit-Knowledge Authentication"** (priority preprint) | IACR ePrint | Crypto theory | Preparing | — | — | — | — |
| **P1 — same, peer-reviewed** (first paper / grant backup) | FC | Blockchain / fintech | Preparing | — | — | — | — |
| P1 — fast-insurance alt (only if hard grant deadline) | Computers & Security / Ledger | Systems security | Idea | — | — | — | — |
| P2 — "Memorability & Coercion-Robustness of Fractal-Encoded Secrets" (human study) | SOUPS | Usable security | Idea | — | — | — | — |

## Reject → next-venue ladders (suggested)

- **Crypto-theory paper:** Journal of Cryptology → Designs, Codes & Cryptography → Cryptography (MDPI)
- **Systems-security paper:** IEEE S&P / CCS / USENIX → NDSS → TIFS / TDSC → Computers & Security
- **Usable-security paper:** SOUPS → TOCHI → Behaviour & Information Technology
- **Blockchain paper:** FC → Ledger → International Journal of Information Security

## Notes

- In computer security, **top-tier conferences (S&P, CCS, USENIX, NDSS) are the
  primary archival venue**, not journals — weight them accordingly when the
  result is flagship-grade.
- **SOUPS** is the natural home for the human-factors core of Great Wall (can a
  user reliably re-point their tacit fractal locations? how memorable, how
  coercion-robust in practice?).
- **Ledger** and **FC** are the right places to argue the Bitcoin self-custody
  value proposition to the cryptocurrency research community.
- Always post the cryptographic core to the **IACR ePrint Archive** first to
  establish priority and gather feedback before formal submission.
- Impact-factor figures are approximate and drift yearly — verify on each
  venue's site, along with current APC / open-access deals, before submitting.
