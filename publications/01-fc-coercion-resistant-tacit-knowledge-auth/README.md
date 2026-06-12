# Paper 01 — Great Wall: Coercion-Resistant Tacit-Knowledge Authentication

**Working title:** *Great Wall: Coercion-Resistant Authentication from Tacit
Knowledge and Sequential Memory-Hardness*

**Lead venue:** Financial Cryptography & Data Security (FC)
**Priority companion:** IACR ePrint Archive (post first)
**Fast-insurance fallback (only if a hard grant deadline looms):** Computers &
Security or Ledger

_Status: Preparing · Last updated: 2026-06-12_

---

## Why this paper, this venue

This is the **first publication** and is intended to double as a backing
credential for grant applications. FC is the most strategic first peer-reviewed
home: it spans cryptography, systems security, and the economic/usability
dimensions, so Great Wall fits without amputating any angle; it is A-tier and
legible to grant committees without being a coin-flip; and it rewards the
novel-construction + threat-model narrative this work offers. See the
`Strategy` section of `../gw-journals-crm.md` for the full rationale.

## Thesis (one paragraph)

A secret can be held entirely in human memory, known to no one else, with the
attacker fully aware of this, and *still* be unextractable under coercion —
because the knowledge is **tacit** (the user can recognize fractal locations
but cannot verbalize them) and the interface to deploy it is gated by an
**inescapably sequential, memory-hard computation** (Argon2d, p=1, t=2). The
second-stage secret surface does not exist until the derivation completes, so
coercion requires detaining the user for at least the configured delay.

## Core claims to defend

1. **Four properties at once** — knowledge-based, individual custody,
   non-obscurity, coercion-resistance — which no conventional seed-protection
   approach achieves simultaneously.
2. **Tacit-knowledge encoding** via a deterministic, lossless bijection between
   BIP-39 entropy and Burning Ship fractal coordinates (no stored state beyond
   shared parameters).
3. **Coercion cost lower-bounded by the Argon2 delay**, with parameter choices
   (p=1, t=2, Argon2d) justified by an OOM-gate / attacker-defender ratio
   argument.
4. **Threat model + attacker economics** showing why the wall holds (and the
   residual risk of intermediate-state checkpoints, plus the TLP / secure-delete
   mitigations in sibling tools).

## Outline (draft)

1. Introduction — the seed-protection dilemma; the four properties.
2. Background — BIP-39, Argon2 memory-hardness, time-lock puzzles, tacit
   knowledge.
3. Construction — two-stage pipeline; fractal bijection; Argon2-derived
   stage-2 perturbation.
4. Threat model & coercion-resistance argument.
5. Parameter analysis — why p=1, t=2, Argon2d; delay tiers.
6. Security & limitations — checkpoint hygiene; TLP gating; precision limits.
7. Related work — KBA, deniable/coercion-resistant systems, hardware wallets.
8. Conclusion.

## Source material in this repo

- `great-wall-core/README.md` — protocol overview, four properties, pipeline.
- `great-wall-core/DESIGN.md` — bijection, fixed-point determinism, Argon2
  parameter justification (p=1, t=2, Argon2d), stage-2 derivation.
- `great-wallet/THREAT_MODEL.md`, `great-wallet/ARCHITECTURE.md` — threat model
  and wrapping architecture (TLP gating, secure deletion).
- `justification-and-economics/JUSTIFICATION.tex` — attacker economics /
  incentive framing.
- `doctorate-proposal/` — framing, motivation, and related-work scaffolding.

## Next actions

- [ ] Draft IACR ePrint version of the cryptographic core (post first to stake
      priority and give the grant proposal a citable artifact).
- [ ] Confirm the upcoming FC submission deadline and CFP scope; size the paper
      to it.
- [ ] Decide author list and corresponding author.
- [ ] Pull threat-model + economics material from the repo into §4–§5.
- [ ] Re-evaluate the SOUPS fork: is a human-factors study fast enough to lead
      instead? (See CRM Strategy.)
- [ ] If a hard grant deadline applies, line up Computers & Security / Ledger as
      parallel fast insurance.

## Files (to be added)

```
01-fc-coercion-resistant-tacit-knowledge-auth/
  README.md          ← this plan
  (paper.tex)        ← manuscript (FC / LNCS style) — TODO
  (eprint.tex)       ← IACR ePrint variant — TODO
  (figures/)         ← diagrams — TODO
  (refs.bib)         ← bibliography — TODO
```
</content>
</invoke>
