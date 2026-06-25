# great-wall-ux — Tech Stack

This document records the tech-stack decision for `great-wall-ux` and
is the authoritative reference, vendored into every consuming repo via
the `great-wall-docs` submodule so all sides see the same stack
commitment at all times.

For what the library is responsible for, see [`SCOPE.md`](./SCOPE.md).
For the ecosystem context this stack lives inside, see
[`great-wallet/ARCHITECTURE.md`](../great-wallet/ARCHITECTURE.md).

---

## Decision

**Dart + Flutter** is the chosen rendering and platform-abstraction stack
for `great-wall-ux`. A single Flutter codebase covers the platform
ordering committed in the architecture doc — **desktop first, mobile
next, web further ahead** — without per-platform forks.

The pygame prototype is treated as a reference implementation only; it
will not be carried into the library's first tagged release.

---

## Why Dart/Flutter

The decision was made against the following criteria, in order of weight.

### 1. One codebase across the platform ordering

The architecture commits to desktop first, mobile next, web further
ahead. Flutter ships first-class engines for all three (Linux / macOS /
Windows, iOS / Android, and Web via CanvasKit — see *Locked
sub-decisions* below). A single Dart codebase covers the entire
ordering without the per-target forks that would otherwise be implied
by mixing, say, pygame on desktop with a native mobile UI and a web SPA.
This was the deciding factor.

### 2. Deterministic, GPU-accelerated 2D rendering of the canvas

The fractal canvas is the central widget. Flutter's Skia-backed
`CustomPainter` / `Canvas` API plus its `FragmentProgram` shader support
give us:

- Direct control of the fractal raster. The Rust core produces a raw
  **escape-count** buffer (single channel); great-wall-ux uploads it as a
  texture and a fragment shader turns counts into pixels (see *Locked
  sub-decisions / Color pipeline*). The core never emits colored pixels.
- Cheap layered overlays — point markers, crosshairs, debug-mode leaf
  rectangles — composited over the raster without leaving the GPU path.
- A consistent rendering model across every target platform, so visual
  regressions are platform-independent.

### 3. Clean FFI to the Rust core

`great-wall-core`'s determinism-critical engine is Rust behind a C ABI
(see `great-wall-core/DESIGN.md`). Dart's `dart:ffi` plus the
`flutter_rust_bridge` ecosystem give a low-overhead, type-safe bridge to
that ABI from every Flutter target, including web (via wasm-bindgen on
the Rust side). The UX layer's call sites — `escape_count`, encode,
decode — map directly onto the existing FFI surface; no new C shim is
needed.

### 4. Input model that survives the desktop → mobile transition

Flutter's gesture arena unifies pointer, touch, mouse, and trackpad
events under one model. Pan/zoom of the fractal viewport, select-mode
clicks/taps, and the practice-session interaction primitives can be
authored once and behave correctly on touch and pointer devices without
parallel code paths.

### 5. Lifecycle and accessibility plumbing

Background/foreground transitions, DPI scaling, screen-reader hooks, and
high-contrast theming are first-class in Flutter on every target. The
training flow's "don't lose an in-progress practice session on app
switch" requirement (see [`SCOPE.md`](./SCOPE.md)) is satisfied by the
framework rather than re-implemented per platform.

---

## Why not the alternatives considered

- **Continue with pygame.** Best-in-class for the desktop prototype but
  no first-class mobile or web story. Carrying it forward would force a
  second stack for the next two platform tiers, which is exactly what
  the single-codebase criterion above is meant to prevent.
- **Native per-platform (SwiftUI / Jetpack Compose / WinUI / web SPA).**
  Maximally idiomatic on each target but multiplies the
  determinism-sensitive surface (input mapping, viewport math) by the
  number of platforms. Each port becomes a place where the bisection's
  pixel-to-coordinate contract can drift.
- **React Native / Expo.** Strong mobile and web story but its 2D-canvas
  story for the fractal raster is weaker than Flutter's Skia path, and
  desktop support — explicitly the first tier — is community-grade
  rather than first-party.
- **Tauri + a web frontend.** Solid desktop story and small binaries
  but the mobile path is immature and the canvas pipeline depends on
  the host webview's capabilities, which varies per platform. Web
  performance for full-viewport fractal blits is not competitive with
  Skia.
- **Qt / QML (PyQt or PySide).** Mature desktop and reasonable mobile,
  but the web story is essentially absent, and the licensing /
  distribution model is heavier than the rest of the ecosystem's
  permissive MIT-or-Apache posture.

Flutter is the only candidate that scored acceptably on all five
criteria above.

---

## Implications

- **Language inside `great-wall-ux`:** Dart. No Python in this repo.
- **Build artefacts:** Flutter library targets (`flutter_package`)
  consumed by `great-wallet/app`'s Flutter shell. Standalone
  executables, where useful for development, are produced by the same
  Flutter toolchain.
- **Rust FFI:** hybrid — `flutter_rust_bridge`-generated bindings for
  the control plane, raw `dart:ffi` against a thin C ABI for the
  per-frame pixel-buffer path. The Rust core stays untouched; only
  the bindings layer is added on the Dart side. See *Locked
  sub-decisions* for the split.
- **Testing:** Dart-side unit tests (`flutter_test`) for widgets and
  interaction; integration tests via `integration_test` on each target
  platform's CI.
- **Pygame prototype:** kept as a reference for behavioural parity
  during the port; not shipped, not maintained beyond the porting
  window, not pinned by `great-wallet`.

---

## Locked sub-decisions

The following finer-grained choices sit underneath the top-level
Dart/Flutter decision and are recorded here so they are not
re-litigated.

- **Web renderer: CanvasKit.** The fractal canvas requires full Skia
  pixel parity with desktop and mobile; the HTML/WASM renderer's
  lighter download is not worth the divergence in the
  determinism-sensitive blit path. The larger initial download is
  accepted as part of the web tier's cost.
- **Threading model: two-tier.** A long-lived UI isolate handles
  Flutter rendering and gesture arena; a Rust-side thread pool
  (managed inside the core crate, exposed across FFI) runs
  `escape_count` and encode/decode work. The UI isolate dispatches
  work units to the Rust pool and receives results via FFI callbacks;
  no per-call Dart isolate spin-up.
- **Platform floors: conservative.** Android API 24+ (Nougat),
  iOS 14+, macOS 11 Big Sur+, Windows 10 1809+, modern desktop Linux
  (glibc 2.31+ / Ubuntu 20.04-era), and the last two stable versions
  of Chrome, Edge, Firefox, and Safari. Older targets are not
  supported.
- **FFI: hybrid.** `flutter_rust_bridge` covers the control plane
  (encode, decode, parameter setup, lifecycle). The hot pixel-buffer
  path — the per-frame `escape_count` blit feeding the canvas — uses
  raw `dart:ffi` against a thin C ABI to avoid bridge overhead and
  copies on the per-frame critical path.
- **Render back-pressure: low-res then refine.** When the user's
  pan/zoom outruns the Rust pool, a downsampled (1/2 or 1/4)
  viewport is rendered immediately and replaced with the full-res
  result when ready. This preserves smooth motion under load at the
  cost of brief blurriness — the established pattern from
  map-style viewers.
- **Escape-count transform: fixed log, no toggle.** The escape-count
  index passed to the palette is `log2(1 + n)` (normalised against
  `log2(1 + max_iter)`), and nothing else. The pygame prototype's
  per-keystroke cycle through Identity / Square / Cube / Exp / Sqrt /
  Cbrt / Log is not carried forward. Rationale: function before
  aesthetics — dog-fooding established log as the most legible
  transform across the full escape-count range, and any toggle is a
  way for the user to land on a different mapping than the one they
  trained on without realising it. The library does not even expose
  the transform as a parameter.
- **Palette set: single hue × 6, brightness-ramped.** The entire palette
  surface is a **constant-hue ramp**: within any one scheme the hue is
  **fixed** and the saturation is **full**, and only **brightness** varies —
  brightness ramps with the (fixed-log) transformed escape count. The same
  scheme is offered in **six hues evenly spaced around the wheel**
  (0°, 60°, 120°, 180°, 240°, 300°), named by hue, with **green the
  default** (a green-on-black terminal allusion). Switching hue is an
  explicit, labelled wheel action, not a cycle-on-keypress. Rationale,
  in order of weight:
    1. **One perceptual dimension.** Hue variance *within* a scheme reads
       as arbitrary and competes for attention; fixing the hue makes
       **brightness** the single dimension the user's visual cognition
       tracks to judge how much detail is visible and to locate the next
       reference point. This is the same "function before aesthetics"
       logic that fixes the escape-count transform, and it composes with
       the always-on brightness modulation below.
    2. **Anti-confusion / anti-chaining.** A small number of
       visually-distinct, named hues means the user cannot drift
       between schemes by accident, and cannot unknowingly chain
       different mappings across sessions in a way that would
       degrade recognition of paths they have memorised.
    3. **Circadian / sleep-hygiene latitude.** Many users (including
       the protocol author) prefer cooler hues by day and warmer /
       red-shifted hues at night. Six hues cover that span without
       inflating the option set.
    4. **Color-vision accessibility.** A handful of well-separated
       hues gives users with color-blindness or other color-perception
       differences a meaningfully better chance of finding a hue whose
       brightness ramp works for them than a single fixed hue would.
  Once a tagged release ships, the six hues' escape-count → RGBA mappings
  are not silently changed — the user's visual memory is treated as an
  API surface, per the palette stability invariant below.

  *History:* an earlier revision locked this surface to the **Classic**
  multi-hue base (inherited from `great-wall-core`) rotated into six
  variants. That was superseded — before any tagged release — by the
  single-hue, brightness-ramped scheme above, on the "one perceptual
  dimension" rationale; the six-hue wheel and its anti-chaining /
  circadian / accessibility rationale are retained.
- **Color pipeline: GPU fragment shader, in great-wall-ux.** The
  escape-count → pixel mapping (log transform → palette lookup →
  brightness modulation) runs entirely in a Flutter `FragmentProgram`
  inside this library; `great-wall-core` returns only the raw
  single-channel escape-count buffer and never emits colored pixels.
  This is the division of labour fixed by
  `great-wallet/ARCHITECTURE.md` ("color schemes, lighting effects …
  do not touch the engine"); it is restated here because an earlier
  deliberation had tentatively placed coloring in the core and it is
  now settled the other way. Rationale:
    1. **Live adjustment is free.** Brightness offset and hue rotation
       are changed *during navigation* (see *Brightness modulation*
       below); as shader uniforms / a swapped palette LUT they cost
       nothing per frame and never re-rasterise. The expensive Rust
       `escape_count` re-runs only when the viewport actually moves.
       Coloring in the core would force a round-trip — and would drag
       viewport zoom and the live brightness offset (interaction
       state) into the engine, which the architecture separates ux to
       prevent.
    2. **Determinism is unaffected.** Only escape counts and the
       pixel-to-coordinate mapping feed the bijection, and both stay
       bit-deterministic in Rust regardless of where coloring runs.
       Color is display-only; sub-perceptual GPU floating-point
       differences across devices cannot move a recognition boundary.
       Cross-platform *appearance* identity is guaranteed by
       specifying the formulae here, not by executing them in Rust.
    3. **No shipped second renderer.** The pygame viewer is
       reference-only and not shipped; the sole production renderer is
       Flutter, so there is no running engine-side coloriser to stay
       byte-consistent with.
- **Brightness modulation: always-on, tacit live control.** Each
  pixel's color is scaled by the sigmoid-like "cave-exploration"
  dimming curve inherited from `great-wall-core`
  (`viewer.py` / `constants.py`):

      factor = B / (B + 2^(n − beo) / z²)      then  rgb *= factor

  with falloff base `B = 16`, raw escape count `n`, zoom `z` (derived
  from the viewport), and brightness-exponent offset `beo`. High
  escape counts dim, zooming in brightens, and `beo` slides which
  escape-count band is lit. Locked properties:
    - **Always on, no toggle.** The prototype's `L`-key on/off toggle
      is dropped, for the same "function before aesthetics" reason the
      transform toggle is dropped.
    - **`beo` is reset to a fixed default at the start of every
      session** and is **never persisted** — consistent with the
      no-stored-secrets posture (a persisted offset would be one more
      thing coercion could extract).
    - **Live adjustment via `L` + mouse scroll**, in fine steps of
      **0.1** (down from the prototype's coarse 1.5). The small step is
      deliberate: it makes the during-navigation brightness adjustment
      a *recognition* skill rather than a few coarse presets. The user
      acquires tacit knowledge of "what each scene looks like at the
      brightness where just enough detail is visible to locate the
      next reference point" — too much information to recollect and
      reproduce, but not too much to recognise. (Compare learning to
      walk an unfamiliar route in a city whose language you cannot
      read: you procedurally learn to recognise alien scenery you
      could never verbally describe; asked to recite the landmarks "in
      a vacuum" you cannot — much as one reliably recognises a coin
      without being able to describe it.) The 0.1 step is a starting
      point, expected to be optimised empirically during dog-fooding.
    - **No on-screen readout of `beo`.** The prototype's
      "Brightness offset +N.N" status message is removed; surfacing
      the value would convert a tacit skill into an explicit,
      verbalizable fact and weaken TKBA.
- **Accessibility: chrome-only.** Buttons, menus, dialogs, settings,
  grade pickers, progress indicators, and all surrounding chrome are
  fully accessible (semantic labels, focus order, screen-reader
  compatible) from day one. The fractal canvas itself is exposed as
  a single opaque `interactive` node with no inner structure or
  content description — describing it would leak coercion-relevant
  information about the user's points.
- **Internationalisation: `Intl` from day one.** Every user-facing
  string is routed through `flutter_localizations` / `Intl` with an
  English `.arb` file from the first commit. Additional languages
  ship by adding `.arb` files; no code change required.
- **State management library:** intentionally undecided. The library
  exposes plain widgets and controllers; the consuming app
  (`great-wallet/app`) picks its own state-management approach.

---

## Invariants

The following are hard, non-negotiable properties of the library.
Any change that violates one of these is a breaking change to the
ecosystem's coercion-resistance posture, not a normal library
revision.

- **No telemetry, no crash reporting, no analytics — ever.** The
  library does not phone home, does not collect usage data, and
  contains no opt-in pathway for either. Anything that exfiltrates
  viewport state, interaction patterns, or grade outcomes could
  leak coercion-relevant information; the only safe posture is
  to ship without the surface at all.
- **No logs of fractal coordinates, escape counts, or decoded
  bits.** The canvas pipeline is non-logging by construction. The
  logging facility, where present, exists for chrome-level events
  (button presses, navigation, errors that do not include
  coordinate data) only.
- **Tacit-only navigation controls.** Controls whose *setting* is part
  of the user's tacit recall — currently the brightness offset — are
  never displayed as a value, labelled, logged, or persisted. Their
  state lives only as ephemeral session state. Surfacing such a value
  would convert tacit recognition into explicit, verbalizable
  knowledge and weaken TKBA.
- **Pixel-to-coordinate determinism.** Given identical viewport
  state — centre `(re, im)`, zoom, device-pixel-ratio, palette,
  escape-count transform — the pixel-to-coordinate mapping is
  bit-deterministic across CPU/GPU build, OS, and device. This
  is enforced by golden tests and is a load-bearing property of
  the bisection's pixel-to-coordinate contract; without it,
  decoded points would drift between platforms.
- **Palette stability.** Once a tagged release ships, each of the six
  single-hue, brightness-ramped schemes has a frozen escape-count →
  RGBA mapping. Tweaks ship as new named variants, never as silent
  updates to existing ones. Users' visual memory of a scheme is a UX
  dependency treated as an API surface.
- **No alternative escape-count transforms, no extra palettes.** The
  log transform and the single-hue × 6 set are the entire surface;
  re-introducing a transform toggle or a user-extensible palette
  loader is a breaking change to the ecosystem's TKBA posture
  (users can no longer be confident which mapping they trained on)
  and not a normal library revision.

---

## Open follow-ups

Genuinely undecided items, to be settled in their own sessions or
in the relevant PRs:

- Repo layout (single Flutter package vs. workspace with separate
  `_test_support` package).
- License (expected to follow the ecosystem's dual MIT / Apache-2.0
  posture; pending confirmation).
- Frame-rate target and animation budget (60 fps floor across all
  targets is the working assumption).
- View-state cache location per platform (last viewport, last
  palette — non-secret data, per-platform standard locations).
