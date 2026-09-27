# Methodology — How the Pilot Runs

This document fixes *how* the course is delivered: the Discord format, the
interaction patterns that keep it hands-on and high-touch, and — most
importantly for a pilot — **how real-usage feedback is collected**. The content
("what we teach") lives in [`syllabus.md`](./syllabus.md) and the textbook; this
is the operating manual.

> **Pilot prime directive.** Collecting honest, specific, real-usage feedback is
> the single most valuable output of this run. A session where students leave
> confused *and we know exactly where* is a success. A session that "went fine"
> but generated no signal is a failure.

---

## Why Discord

- **Synchronous, low-friction, multi-modal.** Voice + screen-share for teaching,
  text channels for parallel Q&A that doesn't interrupt the flow, reactions for
  instant polls, threads for per-exercise help.
- **Persistent.** Channels archive the whole cohort's questions and stumbles —
  itself a feedback corpus we mine between sessions.
- **Where the audience already is.** Bitcoin/tech-literate learners live on
  Discord; no new tool to onboard.

### Server layout (suggested)

```
GREAT WALL — PILOT
  #welcome-start-here        rules, prerequisites, install guide, schedule
  #announcements             read-only; session links, reminders
  📢 Session Stage (voice)   the live class (teacher screen-shares here)
  #live-chat                 parallel Q&A during the live session
  #q-and-a                   async questions between sessions (threaded)
  #hands-on-help             homework/setup troubleshooting (threaded)
  #show-your-fractal         students post screenshots — community + delight
  #feedback                  links to forms; quick reactions; "one-word check-out"
  #off-topic                 keeps the signal channels clean
```

Roles: `teacher`, `assistant` (monitors `#live-chat` so the teacher can focus),
`pilot-cohort-1`. Keep the assistant role staffed — a second person reading text
chat while one person teaches is the highest-leverage staffing choice.

---

## Anatomy of a 90-minute session

Designed so a student is never a passive recipient for more than ~10 minutes.

| Time | Block | Mode | Purpose |
|-----:|-------|------|---------|
| 0–5 | **Check-in** | poll/reaction | Energy + "what stuck from last time?" 1-word in `#feedback` |
| 5–10 | **Recap + hook** | teacher | Re-state last session's problem→solution in one slide; pose today's problem |
| 10–35 | **Concept I** | teacher + live poll | New idea, ≤10 min talk then a comprehension poll/question |
| 35–45 | **Interaction A** | pair / breakout | Students *do* something with Concept I (decode, describe, predict) |
| 45–70 | **Concept II + demo** | teacher screen-share | The session's core mechanic, shown live in the viewer |
| 70–85 | **Hands-on** | everyone at keyboard | Guided exercise; assistant works `#hands-on-help` |
| 85–90 | **Check-out + feedback** | form + 1 word | Post-session form link; "muddiest point" in one line |

Adapt freely — but keep the **three feedback touchpoints** (check-in, a
mid-session comprehension signal, check-out) in every session.

---

## Interaction patterns (the toolbox)

Pick 2–3 per session; rotate so it doesn't get stale.

- **Live poll / reaction vote.** "Will this point decode to a 0 or a 1?" React 🅰️/🅱️.
  Instant comprehension read; surfaces misconceptions in seconds.
- **Think–pair–share (breakout rooms).** Pose a question, 60s solo, 3 min in a
  voice breakout of 2–3, then 2–3 pairs report back. The backbone of
  student↔student interaction.
- **Explain-it-back.** A student narrates the last concept while the teacher
  drives the viewer. If they can drive your hands, they understand it.
- **Predict-then-run.** Before any demo, students commit a prediction in
  `#live-chat`. Running the demo then *confirms or breaks* it — far stickier than
  watching cold.
- **The skeptic seat.** Each session, one volunteer's job is to attack the claim
  ("but couldn't the attacker just…?"). Rewards critical engagement and mines
  the exact objections real users will have.
- **Show-your-fractal.** Low-stakes sharing in `#show-your-fractal` builds cohort
  identity and gives shy students a non-verbal way to participate.

### Designing for the assumed audience

- **Assume Bitcoin literacy, not crypto theory.** Use seeds/BIP39/signing as
  shared vocabulary; introduce Argon2, bijection, fixed-point, fractals from
  zero. When in doubt, define it — but in a "Going deeper" optional aside, so
  pace holds for those who already know.
- **Accessibility of language.** No equation without a plain-words gloss
  immediately after. Memes and analogies are not decoration — they are the
  on-ramp.

---

## Collecting real-usage feedback (the core deliverable)

Three layers, increasing in depth.

### 1. In-the-moment signals (every session)

- **Check-in / check-out one-liners** in `#feedback` (energy word; muddiest
  point). Cheap, high-response-rate, trend-able across sessions.
- **Live polls.** Each poll result is logged (screenshot or bot export) — these
  are *comprehension data*, not just engagement.
- **`#live-chat` mining.** The assistant flags confusion clusters in real time
  and drops a one-line note in the teacher's running log.

### 2. Structured per-session forms (every session)

A short form (≈3–5 min) after each session — templates in
[`feedback/`](./feedback/). Kept short on purpose: completion rate beats
question count. Each form captures: confidence-before vs. confidence-after on
that session's outcomes, the muddiest point, one thing that worked, pacing, and
(for hands-on) whether the exercise *actually ran on their machine*.

### 3. Course-level instruments (start and end)

- **Pre-course survey** — background calibration (Bitcoin/tech comfort,
  expectations, prior exposure) so we can segment feedback and know who the
  material under/over-shot.
- **Post-course survey** — outcomes self-assessment, Net-Promoter-style "would
  you recommend / would you trust real funds to this," and open critique.

### Margin hooks in the materials

Textbook and slides carry **⚑ feedback** markers at spots we predict will
confuse (the bijection's determinism, why `p=1`, the graduation gate). When a
marker lights up the chat, that's a pre-registered hypothesis confirmed — much
stronger signal than retrospective "was it clear?"

### Turning feedback into changes

- **After each session:** 15-min teacher+assistant debrief; log the top 3
  confusion points and one concrete edit each.
- **After the cohort:** triage all signals into (a) content fixes, (b) pacing
  fixes, (c) tooling/setup fixes. File as issues/commits against this directory.
  The pilot's success metric is *the diff it produces in these materials.*

---

## Logistics checklist (per cohort)

- [ ] Cohort capped at 6–12; assistant assigned.
- [ ] `#welcome-start-here` has prerequisites + the install guide + schedule.
- [ ] Install/setup verified *before* Session 1 (offer an optional "Session 0"
      drop-in clinic — the most common pilot failure is wasted live time on
      `cargo build`).
- [ ] Pre-course survey sent and ≥80% returned before S1.
- [ ] Recording consent agreed (sessions recorded for absent students /
      material improvement; never the students' actual setups or secrets).
- [ ] Feedback forms created from [`feedback/`](./feedback/) templates and linked
      in `#feedback`.
- [ ] **Safety note pinned:** in all hands-on work, use **throwaway/sub-standard
      setups and test entropy only** — never a real seed, never real funds.
      Great Wall's own rule applies in class too: the master secret is never
      shown, written, or shared.
