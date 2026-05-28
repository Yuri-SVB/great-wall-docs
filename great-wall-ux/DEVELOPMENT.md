# great-wall-ux — Development

How to build, run, and test the library locally. For what the library
does and the locked decisions it implements, see [`SCOPE.md`](./SCOPE.md)
and [`TECH_STACK.md`](./TECH_STACK.md) in this directory.

## Prerequisites

- **Flutter SDK** 3.22+ (bundles Dart). Install via the official guide:
  https://docs.flutter.dev/get-started/install
- Run `flutter doctor` and resolve the toolchain for your target platform.

Per-platform build toolchains (install only what you target):

- **Web** — works out of the box (CanvasKit renderer; see
  [`TECH_STACK.md`](./TECH_STACK.md) §"Locked sub-decisions").
- **Linux desktop** — `sudo apt install clang cmake ninja-build pkg-config libgtk-3-dev`
- **Android / iOS / macOS / Windows** — see `flutter doctor` output.

## Run the example (web)

```bash
flutter pub get
cd example
flutter pub get
flutter run -d chrome
```

## Run the GUI on Linux desktop

One-time setup:

```bash
sudo apt install clang cmake ninja-build pkg-config libgtk-3-dev
flutter config --enable-linux-desktop
flutter doctor            # the Linux toolchain line should now be ✓
```

Then run:

```bash
cd example
flutter pub get           # regenerates linux/flutter/ephemeral
flutter run -d linux      # native GTK window
```

The example ships a Linux runner under `example/linux/`. If Flutter reports
that the Linux platform is not configured for the project, regenerate it with
`flutter create --platforms=linux .` from inside `example/`.

In both web and desktop, the example wires `DemoEscapeCountSource` —
synthetic test data, **not** a fractal — so the colour pipeline, hue wheel,
and `L`+scroll brightness are visible without the `great-wall-core` FFI
binding. Hold **L** and scroll to adjust brightness; click the hue wheel to
rotate the palette.

## Test

```bash
flutter test
```
