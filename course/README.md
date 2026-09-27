# Great Wall — Pilot Course

> Didactic materials for a **practical, hands-on pilot course** on Great Wall:
> coercion-resistant Bitcoin self-custody via Tacit Knowledge-Based
> Authentication (TKBA). This directory is the single home for everything used
> to *teach* Great Wall; the design docs it draws on live one level up in
> `great-wall-docs` (see [Sources of truth](#sources-of-truth)).

This is a **pilot**. Its first job is not to be complete — it is to be *run*,
watched, and corrected. Every session is instrumented to collect real-usage
feedback (see [`methodology.md`](./methodology.md) and
[`feedback/`](./feedback/)). Treat the textbook and slides as version-0 drafts
that the first cohort helps us debug.

---

## Problem → Solution → Methodology

The course is built around three nested statements, repeated at every scale
(the course as a whole, each session, and most individual concepts). Students
should always be able to answer: *what problem is this solving, what is the
solution, and how do we know it works?*

### The problem (why this course exists)

Two problems, stacked:

1. **The custody problem.** Protecting a Bitcoin seed has no good conventional
   solution. Hardware wallets, metal plates, multisig, and Shamir shares each
   sacrifice at least one of: knowledge-based authentication, individual
   custody, non-obscurity, or coercion-resistance. The growing wave of
   *physical* ("$5 wrench") attacks makes the missing property —
   coercion-resistance — the expensive one. The community's consensus defense
   (obscurity) is self-contradicting at scale: *if everyone is a needle, there
   is no hay.*

2. **The teaching problem.** Great Wall asks a person to stake their savings on
   *tacit recall of fractal landscapes* gated by a deliberately slow
   computation. This is unfamiliar and, on first hearing, implausible. The idea
   only becomes credible when it is **experienced**, not lectured. So the
   pedagogy itself is part of the product: if we cannot teach Great Wall in a
   way that feels learnable, the protocol does not matter.

### The solution (what we teach)

Great Wall, end to end, framed so each layer answers a specific failure of the
conventional approaches:

- **Tacit knowledge** as the authentication substrate — the one thing a victim
  genuinely *cannot hand over* under coercion (you can recognize your fractal
  points but cannot dictate them).
- **The Burning Ship bijection** — how a secret becomes exact coordinates on an
  indescribable labyrinth, losslessly and reversibly.
- **The memory-hard chain** — Argon2 as the "wall": one slow, RAM-bound
  derivation per stage, chained from a stage-0 salt/pepper, so later fractals
  *cannot be materialized* faster than the wall-clock cost, by anyone.
- **The ecosystem** — training (spaced repetition), acceleration (time-lock
  puzzles + a Lightning marketplace), and inheritance (the dead-man's switch) —
  the parts that make "trust your own memory with your retirement" responsible
  rather than reckless.

### The methodology (how the course works, and how we know it worked)

- **Hands-on first.** Every session ends at a keyboard (or in front of the
  viewer). Concepts are introduced *because* the student is about to need them,
  not before.
- **High interaction.** Sessions run live on **Discord** (voice + screen-share +
  text), capped small, with structured student↔teacher and student↔student
  exchanges baked into the timetable (pair work, "explain it back", live
  polls). See [`methodology.md`](./methodology.md).
- **Instrumented for feedback.** Collecting real-usage feedback is the
  pilot's primary deliverable. Each session has a pre-flight check, in-session
  signals, and a post-session form ([`feedback/`](./feedback/)). The textbook
  and slides carry margin hooks ("⚑ feedback") at the spots we most expect to
  confuse.
- **Accessible but not dumbed-down.** We assume comfort with Bitcoin basics
  (seeds, BIP39, public-key signatures) and general technical literacy, but we
  do not assume cryptography, Rust, or fractal mathematics. Depth is offered in
  optional "Going deeper" boxes, never required to keep up.

---

## Who this is for

- **Assumed background:** familiarity with Bitcoin and adjacent tech — what a
  seed phrase is, why self-custody matters, roughly what hashing and public-key
  signatures do. Comfort installing software and using a terminal at a basic
  level.
- **Not assumed:** cryptographic theory, fractal geometry, Rust/Python,
  information theory. Every such idea is introduced from zero when first needed.
- **Cohort size:** small by design (target **6–12** per cohort) so the
  interaction and feedback loops are real, not performative.

---

## What's in here

```
course/
  README.md          ← you are here (course design: problem/solution/methodology)
  syllabus.md        Session-by-session map (5 sessions), outcomes, prep, timing
  methodology.md     The Discord format, interaction patterns, feedback collection
  community/
    DISCORD.md       Server rules to pin, plus the settings and failure modes
  feedback/          Feedback instruments (pre-course, per-session, post-course)
  style/
    greatwall.sty    Shared brand style (palette, fonts, boxes) for all LaTeX
  textbook/
    textbook.tex     Succinct course textbook (one chapter per session)
  slides/
    gwtheme.tex      Shared Beamer theme (brand look + \gwtitle/\punch/\memeslot)
    session1.tex     Session 1 slide deck (Beamer) — the format-locking deck
    session2.tex     Session 2 slide deck
    session3.tex     Session 3 slide deck
    session4.tex     Session 4 slide deck
    session5.tex     Session 5 slide deck
  assets/
    README.md        What images/memes to drop in (kept out of git until cleared)
  Makefile           Build the PDFs (textbook + each slide deck)
```

### Build

```bash
cd course
make            # builds textbook.pdf and every slides/*.pdf
make textbook   # just the textbook
make slides     # just the decks
make clean      # remove LaTeX aux files
make distclean  # also remove built PDFs
```

Requires a TeX Live (or MacTeX) installation with `pdflatex`, `latexmk`,
`tikz`, `pgfplots`, and `beamer` — all in `texlive-full`. The CI/host used for
the repo does not currently ship a LaTeX toolchain, so PDFs are built locally by
the author; only sources are versioned (see [`.gitignore`](./.gitignore)).

---

## Format choice (and why LaTeX)

We begin with a **succinct textbook + slide decks, both in LaTeX**, because that
is the format the author is fastest in and because it versions cleanly as plain
text alongside the rest of `great-wall-docs`. The textbook is the durable
reference; the slides are the live, deliberately *un-boring* teaching surface
(artistic license, humor, and memes are expected — see
[`assets/README.md`](./assets/README.md) and the Session 1 deck). Nothing here
forecloses later moving to web slides or a hosted handbook; the content is the
asset, the format is replaceable.

---

## Sources of truth

This course **teaches** the system; it does not redefine it. When the course and
a design doc disagree, the design doc wins and the course is the bug. Primary
references, all in `great-wall-docs` (or `great-wall-core`):

| Topic | Source |
|-------|--------|
| Protocol (chained `0.3.0`), encoding, Argon2 chain | `great-wall-core/DESIGN.md`, `great-wall-core` `README.md` |
| Four Properties, TKBA, ecosystem, inheritance | `great-wallet/ARCHITECTURE.md` |
| Threat model & assumptions | `great-wallet/THREAT_MODEL.md` |
| Economic case (the "security tax") | `justification-and-economics/JUSTIFICATION.tex` |
| UX principles ("sober, but game-like"; instrument-not-app) | `great-wall-ux/SCOPE.md`, `great-wall-ux/TECH_STACK.md` |
| Open questions / roadmap | `next-steps/` |

> **Version note.** The course tracks chained protocol **`0.3.0`** (mandatory
> text-only stage 0 + one 32-bit point per later stage). Some ecosystem docs
> (`ARCHITECTURE.md`) still use the earlier *stage-1 canonical / stage-2
> perturbed* vocabulary; where the course needs the broader ecosystem (training,
> inheritance) it uses those parts and flags the stage-0/chain terminology
> difference explicitly so students are not confused.

## License

Same as the rest of the repository: dual-licensed
[Apache-2.0](../LICENSE-APACHE) or [MIT](../LICENSE-MIT) at your option.
