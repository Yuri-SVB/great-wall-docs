# Next steps — Canonical island & "entropy crystals" (gamified highlight)

> Working design note captured from discussion. The cryptography is unchanged:
> this is a **visual / UX** layer on top of the existing island machinery. The
> term "canonical island" is **not** otherwise defined in the docs (searched);
> this note proposes its working definition.

## 1. Definition (proposed)

The **canonical island** of a stage is the single distinguished island inside
that stage's **leaf area** — the leaf rectangle as the bisection algorithm
deterministically produces it (which also fixes its *canonical zoom*; at base
zoom the leaf is typically sub-pixel). It is singled out by a deliberately
simple, deterministic criterion so encode, decode, and the UI all agree.

**Criterion.** Over the algorithm-given leaf area, take **all islands the
discovery algorithm finds** there and sort them by:

1. **Pixel count, descending** — the biggest island. (Equivalently `flood_area`
   when comparing across resolutions; within one leaf at one resolution it is
   just pixel count.)
2. **PRNG discovery order, ascending** — the order in which the algorithm's
   seeded SplitMix64 discovery found them.

The **first** island in that sort is canonical.

**This is selected in core, not ux.** The island set *and* its discovery order
are produced by `great-wall-core`'s deterministic discovery (seeded from the
bisection path). ux cannot reproduce the PRNG order without re-porting the whole
discovery algorithm, so **core must select the canonical island and expose it**
(see §3). The earlier "smallest-barycenter, no-FFI, ux-side" idea was wrong:
barycenter is unnecessary once discovery order is the tie-break, and ux has no
access to that order.

**Shape = the island's whole point set, rendered as tiled cells.** Core hands ux
the canonical island's **every discovery point** plus the discovery grid spacing
`pixel_delta`. Each point is the centre of a `pixel_delta × pixel_delta` cell;
ux draws the union of those cells. This is exact and resolution-correct: at the
leaf's canonical zoom the cells tile into a solid island, when zoomed out they
collapse to a speck, and when zoomed *in* past discovery resolution they go
blocky but never gappy.

**Why not flood the display raster.** An earlier design flooded the on-screen
escape-count raster from the points. That fails in practice: the display raster
is rendered at a **low iteration cap** (`renderMaxIter`, 64) and packs escape
counts into a **byte** (`(count % 255) + 1`), so an island whose true escape
count is ≥ the cap (or ≥ 255) is indistinguishable in it — its pixels read as
"inside the set". The points core already provides *are* the authoritative shape,
so tiling their cells sidesteps the raster (and all escape-count matching)
entirely.

**Bounded by the leaf.** Core's flood (recovering the point set) is clipped to
the leaf rectangle, and ux clips the drawn cells to the leaf box too — a stray
cell can never balloon the island across the view.

**Canonical zoom for stable images.** The cell tiling is exact, so there is no
"unstable crystal" wobble in the render. Where a single *stable thumbnail* is
wanted (the stage-tab crystal, §5), render at the leaf's **canonical zoom**,
fixed by the bisection algorithm.

- **Not the encoder's island `score`.** `great-wall-core/DESIGN.md` already
  defines `scoreⱼ = log₂(good_total_area / flood_areaⱼ)` — an *inverse-area*
  weight used for the weighted-median split, so it favours the **smallest**
  islands. The canonical island is the opposite end (biggest), used **only for
  visualisation**, never for the encoded bits.

## 2. Why — "collecting entropy crystals"

Selecting a stage's point should feel **palpable and game-like** (per
`great-wallet/ARCHITECTURE.md` §"Guiding UX Principles" — *sober, but
game-like*). The canonical island is the per-stage "**entropy crystal**": upon
selecting it, it lights up, as if the user is *collecting crystals to build their
cryptographic key*. This turns an abstract bit-encoding into a tangible,
rewarding act and gives each stage a memorable visual anchor.

## 3. Interface — core/FFI addition (implemented)

Selection is core-side, so the core↔ux boundary must carry the canonical island's
identity. **Implemented** in `great-wall-core` as a small handle-based FFI family
(`rust_engine/src/ffi.rs`, Python wrapper `burning_ship_engine.canonical_island`):

- `bs_canonical_island_compute(leaf rect, params, o,p,q, path) → *handle`
- `bs_canonical_island_found(handle) → 0|1`
- `bs_canonical_island_meta(handle, *escape, *pixel_count, *pixel_delta, *bbox[4])`
- `bs_canonical_island_num_points(handle) → n`
- `bs_canonical_island_points(handle, *buf, len)` — `n × (re i64 LE, im i64 LE)`
- `bs_canonical_island_free(handle)`

A handle is used because the **point set is variable-length**: compute once, then
read metadata and copy the points without re-running discovery.

- **Input:** the leaf rect + bisection `path` (both already returned by
  `bs_decode_full`), plus the same discovery params / `o,p,q` / `rng_seed` used
  for the decode.
- **Behaviour** (`discovery::canonical_island`): runs `discover_islands` fresh
  over the leaf rectangle (no inherited seeds — the leaf is never itself split,
  so its island set is defined solely by this discovery), applies
  `discovery::select_canonical_index` (largest `pixel_count`, ties → earliest
  discovery order), then **re-floods from that island's deterministic interior
  seed** (`Island::seed_re/seed_im`, the flood start — pure, so it reproduces the
  island exactly) to recover **all** its points, bounded by the leaf.
- **Output:** the canonical island's **escape count**, **all its discovery
  points**, the **`pixel_delta`** grid spacing, its **bounding box**, and
  **pixel count**.

ux then renders the island's *shape* by **tiling cells** (great-wall-ux
`CanonicalIslandHighlight` → `FractalCanvas._rebuildIslandMask`): each point is
the centre of a `pixel_delta`-sized cell, mapped to the current viewport's pixel
rect and filled flat white, clipped to the leaf box. No display-raster flood and
no escape-count matching — correct at every zoom. There is deliberately **no
ux-side selector** — the authoritative pick is core's. (`islandFromSeeds` /
`seedPixelNear` remain as exported raster-flood primitives but are no longer on
the highlight path.)

## 4. Highlight rendering (the "white" ask) — open

Render the canonical island **highlighted on selection**. Styling options (the
"render it white" request, with alternatives):
- **Flat white fill** — simplest; risks blowing out the island's own texture.
- **White glow / outline + low-opacity fill** — reads as "lit crystal" while
  keeping the shape's detail. *(Recommended.)*
- **Dim everything except the island** — inverts the emphasis; very "crystal in
  the dark", but a larger visual change.

**Decided:** rendered in **great-wall-ux** (a `FractalCanvas` overlay), styled as
**flat white**. (The app consumes great-wall-ux as a submodule, so the change is
synced there.)

### Scale & resolution (load-bearing — this is what made it actually visible)

Two facts about the geometry, learned by exercising the engine end-to-end:

- **Resolution.** At the *encode* discovery resolution (`encodeParams.minGridCells`
  = 4096, a ~64×64 grid over the leaf) the biggest island is only a **3–30-pixel
  speck** — invisible. The app therefore resolves the canonical island at a much
  finer grid (`EncodingConstants.canonicalIslandMinGridCells` = 2²⁰ ≈ 1.05M),
  which yields **15–15000 cells** (a real shape) while staying under the engine's
  flood cap (`maxFloodPoints` = 50000). This is a pure visualisation override; it
  never touches encoded bits. Cost ≈ 220 ms per stage (one-off; a candidate to
  move off the UI isolate later).
- **Framing.** The biggest island is only **~0.5–40 % of the leaf's** extent (it
  varies a lot by seed) and sits on a *different*, smaller island than the
  encoded point. So framing the **leaf** leaves the crystal a few pixels at most.
  Focus instead frames the **union of the point and the island's cells**
  (`SetupController.focusTargetAt`): the crystal fills a good fraction of the view
  *and* the white point marker stays on screen. Measured over many seeds at the
  0.5 focus ratio this gives a clearly visible crystal (hundreds–tens-of-thousands
  of lit pixels) for essentially all of them; a genuinely tiny island (e.g. 15
  cells far from the point) stays small — *some crystals are just small*.

At base/shallow zoom the leaf itself is sub-pixel, so the crystal only appears
once the stage is **focused** (or the user zooms in to the point); at all other
zooms only the point marker shows.

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

- **Decided:** style = **flat white** (per discussion); render location =
  **great-wall-ux** (`FractalCanvas` overlay, via `CanonicalIslandHighlight`).
- **Decided:** selection = pixel count, then PRNG discovery order (core-side).
- **Decided:** shape = **all the island's discovery points tiled as
  `pixel_delta` cells**, clipped to the leaf — *not* a display-raster flood
  (which fails at `renderMaxIter` 64 / `% 255` byte packing). Correct at every
  zoom; no escape-count matching.
- **Done (core):** the `bs_canonical_island_*` handle family exposes escape count
  + **all discovery points** + `pixel_delta` + bbox + pixel count.
- **Done (app + ux):** `great-wallet` binds the family and caches one
  `CanonicalIslandHighlight` per stage (memorise flow only); great-wall-ux tiles
  the cells flat white in `FractalCanvas._rebuildIslandMask`.
- **Done (scale):** discovery resolved at ~1M grid (`canonicalIslandMinGridCells`)
  so the island is a real shape; **focus frames the point+island union** so the
  crystal is actually visible (the leaf is ~100× too big). See §4 "Scale".
- **Remaining:** reuse the cell mask for the stage-tab crystal at canonical zoom
  (§5); decorative-shell count/opacity — dogfooding (§6); consider moving the
  ~220 ms discovery off the UI isolate.
