# Next steps — Hard-reset recovery: area narrowing + candidate replay

> Design note. This is the **Hail Mary** that makes a *hard reset* survivable
> when a stage is forgotten. It has no bearing on normal recall or Shamir
> bail-out (those run with the **deck present** and enjoy a cheap per-stage
> oracle). It matters only in the deck-gone hard-reset path — see
> [`jade-clock-outsourced-anonymous-timelock.md`](jade-clock-outsourced-anonymous-timelock.md)
> §9 and [`cpnf-lifecycle-and-deck.md`](cpnf-lifecycle-and-deck.md) §3. **Status:
> not yet implemented.**

## Why this exists

At hard reset there are **no stored fractals and therefore no per-stage oracle**:
the only correctness signal is the terminal AEAD, reached only after resolving the
whole chain. A stage forgotten at depth `j` from the end otherwise costs
≈ `2^(32·j)` guesses, each carried through `j−1` downstream Argon2d^D derivations —
game over for `j > 1` and a raw `2³²` sweep even for `j = 1`.

The only way through is to **replace the missing algorithmic oracle with the
human's spatial recall**, in two parts:

1. **Narrow the candidate space** with partial recall of *where* the point sat
   (this document).
2. **Replay candidates forward** and let the user perceptually recognize the
   correct one by the familiarity of the *next* stage's board (§"Handoff" below).

Feasible for **at most one** forgotten stage per run; chaining across two or more
fans the candidates into a cross-product and multiplies the derivations, throwing
both human-verification and compute feasibility out the window.

## The feature (draft)

Operates on the re-derived fractal for the forgotten stage (canonical-island
highlight **off**, as in Train — this is recall, not recognition).

1. **Include / exclude rectangles.** The user draws rectangles over the fractal to
   **include** or **exclude** area from the brute-force — encoding spatial partial
   recall ("it was up and to the left", "definitely not the center"). The marked
   regions compose to a single candidate region `R = (⋃ include) ∖ (⋃ exclude)`.
2. **Bisection → leaves.** The existing bisection algorithm — the same one behind
   canonical-island discovery and the `E` in-view enumeration (`bs_leaf_areas_*`) —
   **exhausts `R` into its contracted areas / leaves**, the discrete leaf set
   inside `R`. Each leaf ↔ a 32-bit code via the encoder bijection.
3. **Candidate list.** That leaf enumeration **is** the candidate list; each leaf's
   bits are what the next stage is derived from.

This is deliberately **not new cryptography**: it is the `E` enumeration with its
domain swapped from "current viewport" to "user-drawn `R`", plus the forward-replay
handoff. Most of the work is UI + wiring over machinery that already ships.

## Handoff to the perceptual oracle (Hail Mary step 2)

For each candidate leaf from step 3, derive the **next** stage's fractal and present
the rendered boards; the user recognizes which one looks familiar / has a findable
point. A correct guess for the forgotten stage renders a recognizable next board; a
wrong one renders noise. This substitutes the *user* for the missing algorithmic
oracle, and it is intrinsically the user's — an attacker without the spatial recall
cannot invoke it, so it opens **no sub-threshold oracle** (consistent with
[`post-graduation-security-tiers.md`](post-graduation-security-tiers.md) §1).

## Guardrails & considerations

- **Live feasibility budget.** Show `|leaves(R)|` as the user draws, so the
  `2³² → tractable` narrowing is tangible. Warn when the count exceeds either what
  a human can perceptually scan at step 2 **or** the compute budget for the forward
  derivations (`count × cost-to-next-verifiable-point`). The budget, not just the
  geometry, decides whether a run is viable.
- **One forgotten stage per run.** More than one is flagged unrecoverable up front
  (the cross-product / derivation blow-up from §9). Don't offer a multi-stage mode
  that silently becomes infeasible.
- **Recall-gated, grants an attacker nothing.** The narrowing input *is* the secret
  (spatial memory of the point); an attacker lacking it gains no shortcut. This is
  why the feature is safe to ship despite "helping" brute-force — it only helps
  someone who already partially remembers.
- **RAM-only, no leakage.** Runs at hard reset, deck-gone. The region `R`, the
  candidate leaves, their bits/coordinates, and the derived next-stage candidates
  are **transient in-RAM artifacts** — never written to file, log, or clipboard, in
  line with the standing CPNF secret-handling constraints. Wipe after the run.
- **Honest grading unaffected.** A stage recovered this way is still a *bailout* —
  if this path is ever exercised inside a graded flow, the stage grades **Again**
  (it was not unaided recall), same rule as the `H` hint and the error-locator.

## Open questions

- **Rectangle model vs. freeform.** Rectangles are the KISS draft; whether lasso /
  polygon selection is worth it is a dogfooding question (rectangles compose most
  simply with the axis-aligned bisection tree).
- **Include/exclude precedence & overlap** semantics (exclude-wins is the obvious
  default) — pin down when wiring.
- **Off-UI-isolate.** Same performance follow-up as the `E` scan and canonical-island
  discovery (see [`canonical-island-entropy-crystals.md`](canonical-island-entropy-crystals.md)
  §3): the enumeration over a large `R` and the forward derivations should run off
  the UI isolate.
