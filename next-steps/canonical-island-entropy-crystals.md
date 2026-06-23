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

**Shape = union of all the island's points, not one seed.** Core hands ux the
canonical island's **whole point set** (every flood-filled discovery point), and
ux re-floods from *all* of them at display resolution and **unions** the result.
A single representative seed was rejected: (a) any "pick one point" rule (e.g.
nearest-barycenter) needs an arbitrary tiebreak; (b) more importantly, display
resolution ≠ discovery resolution, so one seed's flood can miss parts of the
shape — a finer pixel size splits a thin neck, a coarser one merges a neighbour.
Flooding from the full set is robust to this and only *cheaply* redundant (most
points re-flood into the same component; a shared `visited` set visits each pixel
once).

**Bounded by the leaf.** Every flood — in core (to recover the point set) and in
ux (to render) — is **clipped to the leaf rectangle**, so a stray escape-count
plateau can never balloon the "island" across the whole view.

**"Unstable crystals" (tolerated Easter egg).** Because connectivity is
resolution-dependent, a highly irregular island can flood to a visibly different
shape at different zooms. That minor glitch is **kept as a feature** — *some
entropy crystals are unstable*. Whenever a *stable, canonical image* is needed
(e.g. the stage-tab thumbnail, §5), render at the leaf's **canonical zoom**,
which is fixed by the bisection algorithm.

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
- `bs_canonical_island_meta(handle, *escape, *pixel_count, *bbox[4])`
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
  points** (the seed set), its **bounding box**, and **pixel count**.

ux then renders the island's *shape* at display resolution via `islandFromSeeds`
(great-wall-ux): it maps every core seed to a raster pixel (`seedPixelNear` snaps
any that display-drift left a step off the escape count), floods the **union** of
all seeds **clipped to the leaf box**, and paints it flat white. There is
deliberately **no ux-side selector** — the authoritative pick is core's.

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
- **Decided:** shape = **union of all the island's discovery points**, flooded
  at display resolution and **clipped to the leaf** (not one representative
  seed); resolution-dependent "unstable crystals" tolerated, canonical-zoom for
  the stable image.
- **Done (core):** the `bs_canonical_island_*` handle family exposes escape count
  + **all discovery points** + bbox + pixel count; ux (`islandFromSeeds`) floods
  the union, leaf-clipped, and paints flat white.
- **Remaining (app):** `great-wallet` must bind the `bs_canonical_island_*`
  family, frame the leaf at its canonical zoom, and pass
  `CanvasOverlays.canonicalIsland` (seed set + leaf bounds + escape count) to
  `FractalCanvas`; then reuse the mask for the stage-tab crystal (§5).
- Decorative-shell count/opacity — dogfooding (§6).
