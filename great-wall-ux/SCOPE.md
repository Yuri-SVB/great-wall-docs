# great-wall-ux — Scope

This document fixes the scope of the `great-wall-ux` library within the
Great Wall ecosystem: what belongs inside this repo and — equally
important — what does not. It is the authoritative reference, vendored
into every consuming repo via the `great-wall-docs` submodule so all
sides see the same definition at all times.

For the ecosystem-wide context, see
[`great-wallet/ARCHITECTURE.md`](../great-wallet/ARCHITECTURE.md). For
the chosen rendering and platform stack, see
[`TECH_STACK.md`](./TECH_STACK.md).

---

## One-line definition

`great-wall-ux` is **the visual and interaction layer** of the Great Wall
fractal encoder: everything the user sees, points at, or scrolls through
when they are working on or with a Burning Ship fractal. The
determinism-critical engine itself stays in `great-wall-core`.

---

## Guiding UX principle: sober, but game-like

A core goal of this library is to **mitigate the mental toil of
memorisation through a pleasant experience**. The interface should be
*sober* — it never competes with the fractal for attention, and it
carries no gimmickry, gamified nagging, or vanity metrics — yet it
should *feel like a game*: tactile, responsive, and quietly rewarding to
operate, so that practice feels closer to play than to drill. Controls
favour direct, physical affordances (e.g. a rotary hue **wheel** the
user clicks to turn, rather than a dropdown). This principle informs the
concrete interaction choices below; where a feature could be either a
chore or a small pleasure, choose the pleasure.

---

## In scope

The library owns the following responsibilities. They are grouped by
concern; the grouping is documentation-only and does not constrain the
internal module layout.

### Rendering

- Fractal rendering: viewport, zoom, pan, resampling.
- Escape-count coloring: a **fixed log transform** mapping escape
  counts onto the palette index, and a **single base palette** ("Classic",
  inherited from `great-wall-core`) available in **six hue rotations** at
  60° spacing. No other transforms and no other palette families are
  offered — see [`TECH_STACK.md`](./TECH_STACK.md) §"Locked sub-decisions"
  for the rationale (function before aesthetics; ossifying the scheme
  set so users cannot accidentally chain incompatible mappings against
  their trained visual memory).
- Stage-aware rendering: canonical fractal (stage 1) vs. user-perturbed
  fractal (stage 2, parameterised by `(o, p, q)`).
- Overlays: point markers, crosshairs, leaf rectangles.
- **Debug-mode** bisection-area visualisation, gated behind an explicit
  flag because surfacing it during normal use would teach the user
  explicit, verbalizable facts whose memorisation undermines TKBA (see
  `great-wallet/ARCHITECTURE.md` §"Tacit Knowledge-Based Authentication").

### Interaction

- Input handling — pointer, keyboard, touch, gamepad — abstracted across
  desktop and mobile.
- Select-mode (click-to-decode) workflow on each stage's viewport.
- Pan/zoom gestures with deterministic mapping back to fractal
  coordinates.
- **Live brightness control as a tacit surface.** Brightness falloff is
  always on; the brightness offset is adjusted *during navigation* by
  `L` + mouse scroll in fine 0.1 steps, reset to a fixed default each
  session and never persisted or displayed. The fine granularity is
  deliberate — it turns the adjustment into a recognition skill the
  user acquires tacitly (see [`TECH_STACK.md`](./TECH_STACK.md)
  §"Locked sub-decisions / Brightness modulation").
- Hue selection via a clickable **rotary wheel** on a control panel that
  snaps through the six hue offsets — the intended affordance for the
  locked Classic × 6 palette set.
- Practice-session UX primitives reusable by `celestial-peace-nf-core`'s
  training flow (point-by-point confirm, hesitation timing surface, grade
  picker chrome).

### Platform abstraction

- A single rendering and input surface that runs on **desktop first,
  mobile next, web further ahead** — see [`TECH_STACK.md`](./TECH_STACK.md)
  for how Flutter realises this ordering.
- Display-density and DPI handling.
- Lifecycle plumbing (pause/resume, background/foreground) so practice
  sessions and ongoing renders are not lost on app switch.

### Assets and theming

- The Classic base palette (inherited from `great-wall-core`) and its
  six hue rotations are the entire palette surface (see
  [`TECH_STACK.md`](./TECH_STACK.md) §"Locked sub-decisions"). The
  set is a frozen visual vocabulary — once it ships in a tagged
  release its escape-count → RGBA mapping is never silently changed.
  There is no user-extensible palette loader and no toggle for the
  escape-count transform.
- Iconography and typography tokens for the chrome that surrounds the
  fractal canvas.

#### Console palette ("Gunmetal") — rationale

The app's console (the message/help surface that floats over the foot of
the viewer) is styled as a translucent, cool, **near-neutral blue-grey**
("Gunmetal"): background `0xE6131519` (~90% opaque), cool off-white text
`0xFFE9EDF2`, and a brighter same-cast accent `0xFFB8C2CC` for headers,
the divider and the top edge. The reasoning, recorded so the decision can
be revisited:

- **Near-neutral, because the fractal owns the colour.** The six fractal
  schemes are single-hue and *fully saturated*. Any saturation in the
  chrome would harmonise with one scheme and clash with its complement, so
  the panel must read as scheme-agnostic. A low-chroma grey is the only
  colour that sits neutrally against all six.
- **…but not a perfect grey, because materials aren't.** A dead-neutral
  `R=G=B` reads as *abstract* — the colour equivalent of a flawless
  machined plane; perfect symmetry tends toward the brutalist /
  uninteresting. Real materials carry a faint cast (dye lot, resin, oxide),
  and the eye reads that small asymmetry as evidence of *substance*. So the
  channels are offset only a few levels (a whisper of blue) — enough to say
  "made of something," far too little to count as a hue. This serves the
  "instrument, not an app" principle (see
  [`great-wallet/ARCHITECTURE.md`](../great-wallet/ARCHITECTURE.md#guiding-ux-principles)).
- **Translucent, so the fractal bleeds through.** The console overlays the
  canvas rather than taking a layout row (stable layout — the viewer never
  resizes). ~90% opacity keeps text crisp while letting the fractal's
  motion register faintly behind the glass.
- **Temperature-matched text.** Cool background ⇒ cool-white text; a
  warm-on-cool pairing reads as "printed on" rather than "one material lit
  by one source."
- **Accent by brightness, not hue.** Emphasis (headers, active state) uses
  a *brighter tint of the same cast*, never a saturated colour — keeping
  the chrome scheme-agnostic on every fractal palette.

Alternatives considered along the temperature axis (all equally valid,
same low-chroma discipline): Slate-teal (cooler), Graphite (almost
neutral), Bakelite (warm red-brown), Olive-drab (green), Tube-amber (warm
yellow). Gunmetal was chosen for the "precision instrument / late-90s
gadget" feel; Bakelite is the documented fallback for a warmer,
better-worn-personal-device read.

### Accessibility

- Full accessibility — semantic labels, focus order, screen-reader
  compatibility — for the chrome that surrounds the canvas (buttons,
  dialogs, settings, grade pickers, progress indicators).
- The fractal canvas itself is exposed as a single opaque interactive
  node with no inner structure or content description. Describing
  canvas contents to assistive technology would surface
  coercion-relevant information about the user's points and is
  rejected by design.

### Internationalisation

- All user-facing strings routed through `flutter_localizations` /
  `Intl` from day one. English `.arb` is the baseline; additional
  languages ship as data, not code.

---

## Out of scope

These belong to sibling repos and must not be re-implemented here.

- **Fractal arithmetic, bisection, encoding, decoding, Argon2.** All of
  this lives in `great-wall-core`'s Rust engine. `great-wall-ux` calls
  the engine through its public API for escape counts and
  encode/decode results; it never duplicates the math.
- **Spaced-repetition scheduling, vault serialisation, vault
  encryption.** These belong to `celestial-peace-nf-core`. The UX
  library provides reusable widgets and interaction primitives that
  the training flow composes; the scheduler state and vault format are
  not its concern.
- **Time-lock puzzles, Lightning Network, inheritance flows.** Anything
  TLP-, LN-, or `phoenix-scroll`-shaped is invisible to this library.
- **Key derivation, BIP39, BIP32.** Never handled in the UX layer.
- **Persistence of user secrets.** The library is stateless with
  respect to anything coercion-resistant. It may cache view-state
  (last viewport, last palette) but never entropy, points, or derived
  material.
- **App-level orchestration.** Wiring the four `great-wallet` modes
  (Setup / Train / Accelerate / Inherit) together is `great-wallet/app`'s
  job, not this library's.

---

## Dependency posture

- **Imports from:** `great-wall-core` only — for escape counts and the
  encode/decode entry points. Calls cross the Rust FFI exposed by the
  core repo.
- **Imported by:** `great-wallet/app` (and, transitively, any sibling
  that composes UX primitives — currently the training flow in
  `celestial-peace-nf-core` reuses pieces of this library through the
  app rather than via a direct dependency).
- **Submodules:** none. As with every other library in the ecosystem,
  the consuming app pins versions; this repo pins nothing.

This matches the dependency matrix in
[`great-wallet/ARCHITECTURE.md`](../great-wallet/ARCHITECTURE.md)
(row: `great-wall-ux → great-wall-core`).

---

## Non-goals worth naming explicitly

- **No bespoke rendering engine.** The Burning Ship is computed by the
  Rust core; this library does not maintain a parallel fractal
  implementation, even for previews.
- **No platform-specific fork.** A single codebase targets desktop,
  mobile, and (later) web. Platform-conditional code is the exception,
  not the structure.
- **No coercion-resistance leakage surface.** Any feature that would
  surface explicit, verbalizable facts about the user's encoding — leaf
  rectangles in non-debug mode, hover tooltips that name decoded bits,
  recently-visited point trails — is rejected by default.
- **No telemetry, crash reporting, or analytics — ever.** The library
  does not phone home and contains no opt-in pathway for either.
  Anything that exfiltrates viewport state or interaction patterns
  could leak coercion-relevant information; the only safe posture is
  to ship without the surface at all.
- **No logs of fractal coordinates, escape counts, or decoded bits.**
  The canvas pipeline is non-logging by construction. Logging exists
  for chrome-level events only and never includes coordinate or
  bit-level data.
