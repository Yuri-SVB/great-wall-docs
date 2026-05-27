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

## In scope

The library owns the following responsibilities. They are grouped by
concern; the grouping is documentation-only and does not constrain the
internal module layout.

### Rendering

- Fractal rendering: viewport, zoom, pan, resampling.
- Escape-count to colour transforms (palettes, lighting effects).
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

- Palette definitions and the colour-pipeline contract. Palettes ship
  as JSON assets (see [`TECH_STACK.md`](./TECH_STACK.md)); the official
  palette set is treated as a frozen visual vocabulary — once a
  palette ships in a tagged release its escape-count → RGBA mapping
  is never silently changed.
- Iconography and typography tokens for the chrome that surrounds the
  fractal canvas.

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
