# Syllabus — Great Wall Pilot Course

Five sessions, each ~**90 minutes** live on Discord, plus ~**30–60 min**
of between-session hands-on homework. The arc moves from *why the problem is
real* to *doing a setup yourself*. Each session is a self-contained
**problem → solution → methodology** unit and ends at a keyboard.

> **Pacing note.** This is a pilot. The timings below are hypotheses. One of the
> things we measure is whether 90 minutes is right (see
> [`feedback/`](./feedback/)). Expect to cut or split sessions after cohort 1.

| # | Title | One-line problem it answers | Hands-on payoff |
|---|-------|------------------------------|------------------|
| 1 | **The Wrench in the Works** | Why is conventional self-custody not enough? | Find your own threat profile; install the viewer |
| 2 | **Secrets You Cannot Tell** | What kind of secret survives coercion? | Decode a fractal point by hand; feel "tacit" |
| 3 | **Drawing Inside the Labyrinth** | How does a seed become a point on a fractal? | Encode & round-trip a mini-seed in the viewer |
| 4 | **Building the Wall** | What stops an attacker (or you) from rushing? | Run the Argon2 chain; calibrate a delay |
| 5 | **Living With It** | How is "trust your memory" made responsible? | Full setup run; train, accelerate, inherit |

---

## Learning outcomes (whole course)

By the end, a student can:

1. State the **Four Properties** and explain why conventional approaches each
   miss at least one — and why coercion-resistance is the hard one.
2. Explain **tacit knowledge** and why it, specifically, defeats the wrench
   attack, in their own words and with a worked example.
3. Trace a secret through the **pipeline**: stage-0 text → Argon2 → perturbed
   Burning Ship → bisection encode → point; and back again (decode).
4. Explain *why the wall holds*: memory-hardness, the chain, `p=1`/`t=2`/Argon2d
   choices at a conceptual level, and what "no public fractal" buys.
5. Perform a **real setup** end-to-end on their own device and articulate the
   training, acceleration, and inheritance obligations that make it safe.
6. Critique the system: name its assumptions, its out-of-scope threats, and at
   least one open question they would want answered before trusting it.

---

## Session 1 — The Wrench in the Works

**Problem.** Self-custody's promise ("be your own bank") collides with a
physical reality: a person can be *coerced*. Every conventional defense either
depends on a device/location you can be forced to surrender, on someone else's
cooperation, or on **obscurity** — and obscurity fails structurally as Bitcoin
adoption grows (Kerckhoffs; "maximalism vs. obscurity, choose one").

**Solution (preview).** Name the **Four Properties** Great Wall claims to deliver
*simultaneously* — knowledge-based, individual, non-obscure, coercion-resistant —
and the one-sentence summary: *it's all in your head (1), in nobody else's (2),
the attacker knows that (3), and still cannot rob it (4).* We don't prove it yet;
we earn it over the next four sessions.

**Methodology.** Ground it in data, not vibes: the wrench-attack trend and the
insurance-priced "security tax" from `JUSTIFICATION`. Then make it personal —
each student sketches their own threat profile.

- Outcomes: articulate why obscurity is a *cost*, not a *defense*; list the four
  properties; locate themselves in the threat model.
- Prep: skim textbook Ch. 1; bring a self-custody horror story (yours or a
  famous one).
- Hands-on (homework into S2): install `great-wall-core`, build the Rust engine,
  launch `viewer.py`, just pan/zoom and get lost in a fractal. No goals — play.
- ⚑ Feedback focus: *Did the economic framing land, or feel like a sales pitch?*

## Session 2 — Secrets You Cannot Tell

**Problem.** A secret you can *say* is a secret you can be *made* to say. PINs,
passphrases, seed words, and even "decoy wallet" tricks all reduce, under a long
enough coercion, to something verbalizable — or get the victim hurt for
plausibly hiding more.

**Solution.** **Tacit knowledge** — the knowing-how that you can deploy but
cannot dictate (recognizing a face; riding a bike). Great Wall turns your secret
into recognition-of-a-place on a fractal. You can point at it; you cannot read it
out. This is **TKBA**, the theoretical core of the system, plus the second
ingredient: an *interface gated by an inescapable computation* so an attacker
cannot just say "try again" forever.

**Methodology.** Experience before definition. Students decode a single point by
hand (guided), then try to *describe the location precisely enough for a partner
to find it* — and fail. The failure is the lesson.

- Outcomes: define tacit knowledge; explain why recognition ≠ recall ≠
  verbalizable; explain why a slow gate is required, not optional.
- Prep: textbook Ch. 2; come having played with the viewer.
- Hands-on: pair exercise on Discord — "describe your point to your partner."
- ⚑ Feedback focus: *Did "tacit" click, or stay abstract?*

## Session 3 — Drawing Inside the Labyrinth

**Problem.** "Encode a secret as a point on a fractal" sounds like hand-waving.
How is it *exact*, *lossless*, and *reversible* — and why a fractal at all?

**Solution.** The **bisection bijection**: repeatedly split a rectangle, let the
fractal's island structure pick where to split, and read each bit as a
left/right (or up/down) choice. Same structure ⇒ encode and decode walk the same
tree ⇒ exact round-trip. Why a fractal: it's a deterministic, shared,
infinitely-detailed "codebook" neither party has to store — and the *haystack ≫
needle* property (specifying *which* fractal costs far more than *where* in it).
Determinism via I4F60 fixed-point (no floats) gets a conceptual treatment.

**Methodology.** Build intuition with a 2–3 bit toy by hand on a drawn
rectangle, then scale up live in the viewer; verify the round-trip (BIP39 in →
points → identical BIP39 out) so skeptics see their exact words return.

- Outcomes: explain bisection encode/decode; say why it's a bijection; explain
  *haystack ≫ needle* and why floats are banned.
- Prep: textbook Ch. 3.
- Hands-on: encode a 3-word (32-bit) mini-seed; watch the bisection; decode it
  back.
- ⚑ Feedback focus: *Where did the bijection lose people — the splitting, the
  determinism, or the "why fractal"?*

## Session 4 — Building the Wall

**Problem.** If anyone — even a fully cooperative you — could render the next
fractal instantly, coercion would just wait for it. What makes the secret
*unreachable in a hurry*?

**Solution.** The **memory-hard chain**. Each stage's fractal is derived by an
Argon2 pass over stage-0 text plus all preceding points → SHA-256 → `(o,p,q)`.
It needs gigabytes of RAM and is strictly sequential, so it *cannot be traded for
speed*; and it's chained, so stage *k+1* can't even begin before stage *k*'s
point is fixed. The wall-clock cost compounds. We unpack the design choices
conceptually: **stage 0** as salt (a label that forks whole wallets) or pepper
(stack on a prior secret); why **`p=1`**, **`t=2`**, **Argon2d**; and "**no
public fractal**." Plus the durable-parameter idea: `N` (iterations) is what you
remember; "hours" is just a perishable label on it.

**Methodology.** Make the delay *visceral*: run a (small) calibration live, watch
RAM fill, feel the seconds. Discuss the checkpoint trade-off (and why "save
intermediate" is off by default and your responsibility to shred).

- Outcomes: explain memory-hardness and chaining in plain words; justify
  `p=1`/`t=2`/Argon2d at a high level; explain salt vs. pepper; explain why `N`
  (not wall-clock) is the thing to remember.
- Prep: textbook Ch. 4.
- Hands-on: calibrate a short delay on your device; try a nearby iteration count
  via checkpoints; then securely delete the checkpoint.
- ⚑ Feedback focus: *Did the "why it can't be rushed" argument feel airtight?*

## Session 5 — Living With It

**Problem.** "Stake your retirement on remembering some fractals" raises three
fair objections: *I'll forget; the wall is too slow for me too; and what happens
when I die or can't recall?*

**Solution.** The ecosystem answers each: **Train** (spaced-repetition
consolidation with a measured **graduation gate** — your stash isn't "secured"
until memory is confirmed; the provisional-key bootstrap covers the gap);
**Accelerate** (RSW time-lock puzzles you can outsource to the **jade-clock**
Lightning marketplace *without giving up custody*); **Inherit** (the
**phoenix-scroll** dead-man's switch + opaque taproot fallbacks). Framed by the
UX north-stars: *sober but game-like*, *an instrument, not an app*.

**Methodology.** Do a **complete, real setup** together (small/sub-standard size
for time), then walk each ongoing obligation. Close with an open critique: what
would you want answered before trusting this with real money?

- Outcomes: perform a full setup; explain training/acceleration/inheritance and
  why each exists; name the system's assumptions and at least one open question.
- Prep: textbook Ch. 5; have the viewer working from S3/S4.
- Hands-on: full setup run; configure a (mock) training schedule; sketch an
  inheritance will on paper.
- ⚑ Feedback focus: *After doing it once, does "trust my own memory" feel
  plausible? What's the biggest remaining doubt?*

---

## Mapping to the textbook

| Session | Textbook chapter |
|---------|------------------|
| 1 | Ch. 1 — The Problem |
| 2 | Ch. 2 — Tacit Knowledge & the Four Properties |
| 3 | Ch. 3 — Encoding a Secret into a Fractal |
| 4 | Ch. 4 — The Memory-Hard Wall |
| 5 | Ch. 5 — The Ecosystem: Train, Accelerate, Inherit |

Slides are produced per session (`slides/session1.tex` … `session5.tex`), all
sharing `slides/gwtheme.tex`. All five decks exist in draft; Session 1 set the
format the others follow, and every deck is refined from cohort feedback.
