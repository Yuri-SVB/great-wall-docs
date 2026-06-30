# Next steps — Canonical island & "entropy crystals" (remaining polish)

> **Implemented and moved.** The canonical-island machinery — definition and
> deterministic selection (core), the tiled-cell shape, scale/framing, the
> `bs_canonical_island_*` / `bs_leaf_areas_*` FFI, the `E` in-view enumeration,
> and the Setup/overlay wiring (cross marker, selection frame) — now ships and is
> documented as a reference feature in
> [`great-wallet/ARCHITECTURE.md` → *Canonical-Island Highlighting ("entropy
> crystals")*](../great-wallet/ARCHITECTURE.md#canonical-island-highlighting-entropy-crystals).
> This note now tracks only the polish that is **not** yet implemented.

## 1. Stage-tab "crystal" thumbnail (bonus)

When a stage is complete / its point is available, the stage tab shows the
collected canonical-island shape **beneath the number** — a tiny thumbnail of the
crystal — so the tab bar reads as a row of collected crystals (progress made
physical). Reuse the existing per-stage cell mask, rendered once at the leaf's
**canonical zoom** (fixed by the bisection algorithm) for a single stable
thumbnail.

## 2. Decorative shells — describability hardening (TKBA; tune by dogfooding)

To keep the canonical island **less verbally describable** (TKBA: the point must
stay tacit), render the island together with a few (≈4) **adjacent decorative
escape-count shells** around it, blurring its exact boundary so a coerced user
cannot cleanly say "it's the blob at X". The exact count/styling is **to be
defined by dogfooding** — enough decoration to defeat easy description, not so
much that recognition suffers.

## 3. Performance follow-up

The per-stage canonical-island discovery (≈ 220 ms at the ~1M visualisation
grid) and the `E` scan currently run on the UI isolate. Moving the heavy
discovery off the UI isolate is a candidate optimisation once the polish above
lands.
