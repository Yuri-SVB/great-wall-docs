# CPNF — Step 1 implementation brief (scheduler core only)

> **What this is.** First-steps implementation of `celestial-peace-nf-core`
> ("Celestial Peace: Never Forget"), the spaced-repetition training that
> consolidates a user's tacit recall of their fractal setup. This brief covers
> **only Step 1**: a pure, conservative SM-2 scheduler, an injected clock, the
> card/queue model, and a review-session loop that drills each stage's point
> recall plus the explicit fact cards. **No TLP vault, no graduation gate, no
> inheritance** — those are later steps (see "Out of scope" and the full
> lifecycle in [`cpnf-lifecycle-and-deck.md`](cpnf-lifecycle-and-deck.md)).
>
> Ground truth: `great-wallet/ARCHITECTURE.md §4 celestial-peace-nf-core`,
> `cpnf-lifecycle-and-deck.md`, and
> `chained-protocol-size-and-ux-roadmap.md §3`. This brief narrows them to a
> buildable first slice.

## 0. Hard invariants (read first — non-negotiable)

1. **Points-at-rest: encrypted, never cleartext.** Store the true point encrypted
   inside the deck (provisional key pre-graduation; own-legs key post-graduation)
   — CPNF needs it to grade recall. Encryption is what preserves tacitness /
   coercion-resistance: pre-graduation the external provisional prop guards it;
   post-graduation the key is derived from the very secret the point encodes, so
   decrypting it already presupposes reproducing it. Storing it grants an attacker
   nothing. Likewise never write bits, `(o,p,q)`, or bisection paths in
   **cleartext**, and never emit any of them to logs/telemetry.
2. **Exercise validity: highlight OFF during a point card.** Never render the
   canonical-island highlight while the user is attempting to locate a stage's
   point, and decrypt the stored point only to *validate* their located point,
   never to display it. This is **not** a security measure — it protects the
   **validity of the memorization exercise**: showing the answer first would test
   recognition of a freshly-drawn marker, not genuine recall.
3. **Fact cards are drillable as explicit facts.** `m`, `N`, salts, export salts,
   download provenance, and miscellaneous reminders are parameters/labels, **not
   the tacit seed** — storing/quizzing them (encrypted at rest) does not weaken
   coercion-resistance. Asymmetry: `m` exact (mismatch ⇒ every fractal breaks);
   `D` also exact here (approximate-memory recovery is *adjust-`D`-on-open-setup*,
   roadmap §3a — not a scheduler concession).
4. **No wall-clock reads outside the injected `Clock`.** Never call
   `DateTime.now()` in scheduler or session code — only `Clock.now()`. Both a
   determinism/testability requirement and an auditability one.
5. **Uniform encryption (Step 1).** Every card in a deck is encrypted under the
   same key as the setup (provisional key in this phase). No per-card security
   tiering (the salt-vs-pepper nuance is deferred — see the lifecycle note).

## 1. Placement & shape

- Implement as **UI-free pure Dart**: no Flutter imports, no `dart:io` clock, no
  FFI in the scheduler itself. This is the logic the architecture assigns to
  `celestial-peace-nf-core`.
- **Recommended location for Step 1:** `great-wallet/app/lib/src/mem/`
  (package-shaped module, extractable into the `celestial-peace-nf-core` repo
  later with no API change).
- The **app** supplies: the setup (decrypted from the provisional-key ciphertext
  via the existing class-A secure load), the real `Clock`, and the recognition UI
  that drives point validation through `great-wall-core`.

## 2. Data model

```dart
/// Injected time source. Real impl wraps the system clock; tests inject a fake.
/// NOTHING in mem/ may read time except through this.
abstract interface class Clock { DateTime now(); }

enum Grade { again, hard, good, easy }

enum CardKind {
  point, // one stage's point recall; stored point (encrypted) grades the attempt
  fact,  // explicit recall: m, N, salt/pepper, export salt, provenance, misc
}

/// Persisted per-card SM-2 state (itself encrypted with the deck). For point
/// cards the "answer" (the true point) lives in the encrypted setup, not here.
class MemCard {
  final String id;          // "point:3", "fact:m", "fact:N", "fact:salt", ...
  final CardKind kind;
  final int stageIndex;     // point cards; -1 otherwise
  final String factId;      // fact cards: "m" | "N" | "salt" | "export:2" | ...

  double easeFactor;        // SM-2 EF, starts 2.5, floored at 1.3
  int repetitions;          // consecutive non-lapse reps
  int intervalDays;         // current scheduled interval
  DateTime due;             // next review (computed via Clock)
  int lapses;
}

class ReviewQueue { final List<MemCard> due; } // due <= clock.now(), oldest first
```

**Card set for a setup with `N` stages:** `N` point cards + one fact card each
for `m`, `D`, `salt/pepper`, download-provenance, every user-defined export salt,
and any optional miscellaneous reminders.

## 3. Scheduler — conservative SM-2 (`MemSchedule`)

Classic SM-2, tuned conservative (err toward *more* frequent review). **Cite the
authoritative source in both the docs and the code comments** — do not
paraphrase the algorithm from memory:

- P. A. Woźniak, *Optimization of learning* / **SuperMemo SM-2 algorithm**
  (1990): <https://www.supermemo.com/en/archives1990-2015/english/ol/sm2>.

The `EF`, quality-grade, and interval formulas below must match that reference;
any deviation (e.g. the conservative interval floor) should be commented as a
*deliberate deviation from SM-2*, with the reason, so it is never mistaken for
the canonical algorithm.

- **EF:** start `2.5`, floor `1.3`. Map Again/Hard/Good/Easy → SM-2 quality and
  update `EF' = max(1.3, EF + (0.1 - (5-q)*(0.08 + (5-q)*0.02)))`.
- **Intervals:** first success → `1 day`; second consecutive → `6 days`;
  thereafter → `round(interval * EF)`, with per-grade multipliers:

  | Grade | Meaning | Interval effect |
  |-------|---------|-----------------|
  | Again | failed to locate / wrong fact | reset to 1 day, `repetitions=0`, `lapses++` |
  | Hard  | located but slow / many attempts | `interval * 1.2` |
  | Good  | located with reasonable confidence | `interval * EF` |
  | Easy  | located immediately | `interval * EF * 1.3` |

- **Due:** `due = clock.now() + intervalDays` (all time via `Clock`).
- **API:** `MemSchedule(clock)` exposing pure `grade(card, g) -> MemCard`,
  `queue(cards) -> ReviewQueue`, and `freshCard(...)` (interval 0, due now).

`MemSchedule` is **pure given a `Clock`** — fully unit-testable with a fake clock.

## 4. Review-session flow (Step 1 — over the provisional ciphertext, no new vault)

```
decrypt setup from provisional-key ciphertext (existing class-A load)
build ReviewQueue from persisted MemCards + Clock.now()
for each due card, oldest first:
  if point card:
      render the stage (canonical -> perturbed) with island highlight OFF
      user attempts to locate the point; validate via great-wall-core against
        the decrypted setup (match / no-match) -- point never displayed
      derive Grade from match + attempt-count/hesitation
  if fact card:
      quiz the value; m/N/salt/export/provenance graded exact; misc as authored
  card' = schedule.grade(card, grade); persist card' (re-encrypted with the deck)
```

## 5. Acceptance criteria

- [ ] `MemSchedule` pure, UI-free, Flutter-free; time only via `Clock`.
- [ ] Real `SystemClock` + advanceable `FakeClock` both implement `Clock`.
- [ ] Interval ladder: Good → 1d → 6d → `round(6*EF)`; Again resets to 1d, bumps
      `lapses`; EF floors at 1.3, rises on Easy.
- [ ] `N` stages ⇒ `N` point cards + the fact cards of §2.
- [ ] Point cards render with **highlight off** and never display/serialize the
      point in cleartext; the point is read only to validate.
- [ ] Deck at rest is encrypted (provisional key); no cleartext coordinates/bits/
      `(o,p,q)`/paths anywhere; no `DateTime.now()` in `mem/`; no secret logging.
- [ ] `queue()` returns only `due <= clock.now()`, oldest-due first;
      advancing the `FakeClock` makes cards due deterministically.

## 6. Tests

1. Scheduler progression + per-grade multipliers with `FakeClock`.
2. EF update math; floor at 1.3.
3. Lapse handling (Again resets, bumps `lapses`, keeps floor).
4. Queue ordering / due-filtering across clock advances.
5. **Security:** serialized deck has no cleartext coordinate/bit/`(o,p,q)`/path;
   grep/lint: no `DateTime.now()` in `mem/`; no secret fields logged; highlight
   suppressed on point-card render.

## 7. Out of scope (Step 1) — see `cpnf-lifecycle-and-deck.md`

- TLP-gated / own-legs re-encryption, `CPNF-N` key schedule, panic button,
  outsourced squaring, mobile/desktop abort topologies.
- Graduation gate / green-light; provisional-key bootstrapping already exists in
  Setup (don't touch it here).
- Inheritance / phoenix-scroll coupling; background TLP solver + checkpointing.
- Time-to-clear quantitative scoring (maze-rat analogy) — grading refinement, TBD.

Deliver Step 1 as a focused PR: the `mem/` module (clock, model, schedule), the
session-loop wiring, and the test suite above — extractable into
`celestial-peace-nf-core` later with no API change.
