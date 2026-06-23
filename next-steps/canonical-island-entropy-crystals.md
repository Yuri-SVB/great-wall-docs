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
identity. **Implemented** in `great-wall-core` as the FFI entry point
`bs_canonical_island` (`rust_engine/src/ffi.rs`, Python wrapper
`burning_ship_engine.canonical_island`):

- **Input:** the leaf rect + bisection `path` (both already returned by
  `bs_decode_full`), plus the same discovery params / `o,p,q` / `rng_seed` used
  for the decode.
- **Behaviour:** runs `discover_islands` fresh over the leaf rectangle (no
  inherited seeds — the leaf is never itself split, so its island set is defined
  solely by this discovery) and applies `discovery::select_canonical_index`
  (largest `pixel_count`, ties → earliest discovery order).
- **Output:** the canonical island's **escape count**, a **guaranteed-interior
  seed point** (fractal coords — the flood-filled pixel nearest the barycenter,
  stored on `Island::seed_re/seed_im` so it stays inside non-convex islands),
  its **bounding box**, and **pixel count**. Returns `0` when the leaf holds no
  island.

ux then renders the island's *shape* at display resolution by flood-filling the
displayed `EscapeCountRaster` from that seed at that escape count (the per-pixel
raster suffices for the **render**, just not for the **selection**).
`islandFromSeed` (great-wall-ux) is that render primitive; `seedPixelNear` snaps
the core seed onto the matching pixel if display-resolution drift lands it a
pixel or two off. There is deliberately **no ux-side selector** — the
authoritative pick is core's.

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
- **Done (core):** `bs_canonical_island` exposes escape count + interior seed +
  bbox + pixel count; ux flood-fills the seed and paints flat white.
- **Remaining (app):** `great-wallet` must bind `bs_canonical_island`, frame the
  leaf at its canonical zoom, and pass `CanvasOverlays.canonicalIsland` to
  `FractalCanvas`; then reuse the mask for the stage-tab crystal (§5).
- Decorative-shell count/opacity — dogfooding (§6).
