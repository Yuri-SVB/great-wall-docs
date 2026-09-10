# CPNF — scheduler core (Step 1)

The spaced-repetition memory engine that consolidates a user's tacit recall of a
Great Wall fractal setup.

Pure Dart, UI-free, FFI-free, and **clock-injected**: nothing in the package
reads the wall clock. The consuming app supplies the real clock, the setup to
validate recall against, and the recognition UI.

## What Step 1 implements

Per `next-steps/cpnf-step1-scheduler.md`:

| Piece | Role |
|---|---|
| `Clock`, `FakeClock` | Injected time, and a deterministic substitute for tests |
| `Grade`, `CardKind`, `MemCard`, `ReviewQueue` | The card model — point cards and fact cards |
| `MemSchedule` | Conservative SM-2 scheduling |
| `honestGrade` | Forces a grade to reflect memory rather than outcome |
| `buildDeck` | The card set for a setup: N point cards plus fact cards |

**A card holds only SM-2 schedule state.** A point's answer stays in the
encrypted setup and is read solely to *validate* a recall attempt — the deck is
not a second copy of the secret.

## Scheduling

Conservative **SM-2** (P. A. Woźniak, SuperMemo, 1990 —
[archive](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2)), with
the canonical E-Factor update and lapse handling. The four-button per-grade
interval multipliers are a deliberate deviation from the original and are
documented as such in the source.

## Grades measure memory, not outcome

`honestGrade` exists because the two diverge. A success by luck, a guess, giving
up, a hint, or a brute-force bailout are all forced to `Again`. A scheduler fed
outcomes rather than recall would lengthen intervals on the strength of
successes the user could not repeat — which, for a setup whose whole purpose is
retention under pressure, is the failure that matters.

## Not in Step 1

The review-session flow, encryption-at-rest, and the TLP-gated / graduation /
inheritance lifecycle. See `cpnf-lifecycle-and-deck.md`.

## Testing and consumption

Pure Dart, no Flutter:

```sh
dart pub get
dart test
```

Add as a path or git dependency; the app provides the real clock:

```dart
import 'package:celestial_peace_nf_core/celestial_peace_nf_core.dart';

final schedule = MemSchedule(appSystemClock); // app supplies a Clock impl
final due = schedule.queue(cards);
final card2 = schedule.grade(card, honestGrade(succeeded: true, proposed: Grade.good));
```
