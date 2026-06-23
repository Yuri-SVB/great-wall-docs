# Next steps — Canonical island & "entropy crystals" (gamified highlight)

> Working design note captured from discussion. The cryptography is unchanged:
> this is a **visual / UX** layer on top of the existing island machinery. The
> term "canonical island" is **not** otherwise defined in the docs (searched);
> this note proposes its working definition.

## 1. Definition (proposed)

The **canonical island** of a stage is the single **largest-area, most distinct
island** found inside that stage's **leaf rectangle** — a deliberately *simple,
deterministic* criterion so encode, decode, and the UI all single out the same
one.

- **Criterion:** the island with the greatest `flood_area = pixel_count ×
  pixel_delta²` in the leaf rect. For the "distinct" qualifier, optionally
  require it to win by a margin over the runner-up (tunable; default: just the
  max).
- **Not the encoder's island `score`.** `great-wall-core/DESIGN.md` already
  defines `scoreⱼ = log₂(good_total_area / flood_areaⱼ)` — that is an
  *inverse-area* weight used for the weighted-median split, so it favours the
  **smallest** islands. The canonical island is the opposite end (biggest), and
  is used **only for visualisation**, never for the encoded bits.

## 2. Why — "collecting entropy crystals"

Selecting a stage's point should feel **palpable and game-like** (per
`great-wallet/ARCHITECTURE.md` §"Guiding UX Principles" — *sober, but
game-like*). The canonical island is the per-stage "**entropy crystal**": upon
selecting it, it lights up, as if the user is *collecting crystals to build their
cryptographic key*. This turns an abstract bit-encoding into a tangible,
rewarding act and gives each stage a memorable visual anchor.

## 3. Interface — no new FFI required (first version)

ux receives the per-pixel `EscapeCountRaster` and the leaf rect. An island is a
connected equal-escape region, so ux can flood-fill the raster, measure areas,
and pick the largest inside the leaf rect on its own side — **no island object
needs to cross the core↔ux boundary.** (Optional later: core exposes the winning
island's escape-count + an interior seed pixel for a resolution-exact mask.)

## 4. Highlight rendering (the "white" ask) — open

Render the canonical island **highlighted on selection**. Styling options (the
"render it white" request, with alternatives):
- **Flat white fill** — simplest; risks blowing out the island's own texture.
- **White glow / outline + low-opacity fill** — reads as "lit crystal" while
  keeping the shape's detail. *(Recommended.)*
- **Dim everything except the island** — inverts the emphasis; very "crystal in
  the dark", but a larger visual change.

**Where to render is an open architectural decision** (the canvas lives in
`great-wall-ux`; the app consumes it as a submodule): either a new island-mask
overlay in `great-wall-ux`'s `FractalCanvas`, or an app-side `CustomPaint`
overlay over the canvas in `great-wallet`. Decide before implementing.

## 5. Stage-tab "crystal" (bonus)

When a stage is complete / its point is available, the stage tab shows the
collected canonical-island shape **beneath the number** — a tiny thumbnail of the
crystal — so the tab bar reads as a row of collected crystals (progress made
physical).

## 6. Decorative shells — describability hardening (TKBA; tune by dogfooding)

To keep the canonical island **less verbally describable** (TKBA: the point must
stay tacit), render the island together with a few (≈4) **adjacent decorative
escape-count shells** around it, blurring its exact boundary so a coerced user
cannot cleanly say "it's the blob at X". The exact count/styling is **to be
defined by dogfooding** — enough decoration to defeat easy description, not so
much that recognition suffers.

## 7. Open questions

- Tie-breaking when two islands are near-equal in area (the "distinct" margin).
- Render location (great-wall-ux overlay vs great-wallet app-side overlay).
- Whether the highlight is computed ux-side from the raster (first version) or
  core-assisted (exact mask) — start ux-side.
- Decorative-shell count/opacity — dogfooding.
