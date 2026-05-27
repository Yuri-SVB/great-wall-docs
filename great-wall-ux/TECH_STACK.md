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
`CustomPainter` / `Canvas` API gives us:

- Direct pixel-level control for the fractal raster (the texture is
  produced by the Rust core; Flutter blits it).
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
- **Palette pipeline: JSON assets.** Palettes ship as JSON files in
  `assets/`, parsed at startup. Users (and downstream apps) can drop
  in additional palettes without recompiling. Both user-facing docs
  and contributor docs MUST carry a prominent warning that non-official
  palettes change the escape-count → colour mapping and can degrade
  recognisability of paths the user has memorised. The official
  palette set is a deliberate visual vocabulary; defectors cannot
  replicate it trivially without retraining users' visual memory.
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
- **Pixel-to-coordinate determinism.** Given identical viewport
  state — centre `(re, im)`, zoom, device-pixel-ratio, palette,
  escape-count transform — the pixel-to-coordinate mapping is
  bit-deterministic across CPU/GPU build, OS, and device. This
  is enforced by golden tests and is a load-bearing property of
  the bisection's pixel-to-coordinate contract; without it,
  decoded points would drift between platforms.
- **Palette stability.** Once an official palette ships in a
  tagged release, its escape-count → RGBA mapping is frozen
  forever. Tweaks ship as new named palettes, never as silent
  updates to existing ones. Users' visual memory of a palette is
  a UX dependency treated as an API surface.

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
