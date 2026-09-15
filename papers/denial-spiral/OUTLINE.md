# The Denial Spiral — outline for the second paper

**Status:** planning. Nothing has been moved yet. The Deadly Race manuscript is
untouched by this file.

The split follows the *epistemic* boundary, not the mechanism boundary:

- **Paper 1 — The Deadly Race.** What can be derived about *protocols*.
- **Paper 2 — The Denial Spiral.** Why the field *cannot see* the problem.

Both mechanisms are already established as independent: the DR-safe column does not
track the Four Properties, and `cor:spiral-equiv` shows Spiral *depletion* tracks
non-obscurity while Spiral *exposure* is no design property at all.

---

## 1. What moves (already written, in Appendix D)

Appendix D of the FC build is 629 lines against 198 in the body §5. It is already
paper 2 in embryo:

| Material | Current location | Notes |
|---|---|---|
| The self-destruct class in full | D §66–140 | core of paper 2's classification |
| What each vendor claims for it | D §113 | the "who claimed what" ledger |
| Two bluffs the erasure invites | D §141 | |
| Sparrow — vendor-documented naive tier | D §209 | |
| The decoy is sold, and coached | D §234 | the market for obscurity |
| The Obscurity Paradox | D §270 | |
| **The Denial Spiral** | D §298 | the title result |
| The Spiral is not a sixth axis | D §318 | |
| The praxeological reading | D §334 | method section of paper 2 |
| **Obscurity anosognosia — four mechanisms** | D §379 | |
| Registry method and coding tables | D §463 | |
| The proxy-victim finding | D §545 | |
| RATIRL and Balland | D §576 | |

## 2. What moves out of the DR body (frees FC pages)

Measured on the FC body, ~130 of ~1,100 lines, worth roughly **2–2.5 pages**:

| Section | lines | disposition |
|---|---|---|
| §5 Self-destruct (wallet-erase) PINs | 48 | → paper 2 entire |
| §5 Empirical grounding in the registry | 58 | → paper 2 (DR keeps ~1 para) |
| §9 Ethics (disclosure/obscurity argument) | 56 | → split; DR keeps the residual-disclosure part |

That budget covers the DR-safe column (+1 pp) and the two keywords (+1 pp) with
room left over, both of which currently do not fit.

## 3. What paper 1 keeps, compressed

- **One paragraph** where §5.6 now sits: the stipulations ($t$, the murder-cost
  weighing) are empirically grounded in the registry; full coding in paper 2.
- **One paragraph** of the anosognosia argument, because it justifies *"the bar has
  to be derived, because it will not be measured"* — which paper 1 needs. Cite
  paper 2 for the four mechanisms.
- The DR-safe column and the comparison table stay in paper 1.

## 4. What paper 2 needs newly written

1. **Its own model section.** Cannot assume paper 1 is read. Needs: the WDY
   adversary, Kerckhoffs, NNPP, and the naive/weak/strong tiers — compressed to
   ~2 pages, cited to paper 1 for the full treatment.
2. **A framing introduction** that is not "leftovers from the Deadly Race": the
   thesis is that a *norm* is a security-relevant object, that denial credibility
   is a commons, and that the field's own incentives prevent it from measuring the
   damage.
3. **A conclusion** with the adoption prediction stated as such — availability does
   not produce adoption; adoption arrives where conceding is cheap.

## 5. Cross-citation

Both directions, and both are ordinary. One constraint:

- FC is double-blind. Paper 1 cites paper 2 in the **third person** — "[X]
  develops…", never "our companion paper" — and `references-anon.bib` must strip
  the name as it already does. `make anon-check` catches leaks.
- **Sequencing:** put paper 2 on Zenodo with a DOI *before* the FC submission, so
  paper 1 cites a fetchable object. Citing an unavailable manuscript reads badly to
  reviewers.

## 6. Venue

- Paper 1 → FC (SoK track), as planned. No change to the current submission.
- Paper 2 → a security-economics venue; WEIS is the obvious candidate. The
  commons/externality framing is native there, and — per the fourth mechanism's own
  prediction — that room contains nobody with a shipped duress PIN to defend, which
  is where adoption is predicted to arrive first.

## 7. Sequencing and risk

Do **not** restructure under the FC deadline. Appendices do not count against the
20-page limit, so the current submission is already "paper 1 plus supporting
material" and needs no change. Write paper 2 properly afterwards, using Appendix D
as its draft rather than carving it out under time pressure. Leave the combined
preprint at its existing DOI; give paper 2 its own when ready.

## 8. Titles

Paper 1 keeps *The Deadly Race* and its current subtitle — once it is about one
thing, the subtitle problem dissolves. Paper 2 is *The Denial Spiral*.
