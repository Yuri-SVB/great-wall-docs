# The Deadly Race — formal wrench-attack threat model (LaTeX manuscript)

First LaTeX manuscript of the coercion-resistance paper: a formal threat model
for physical-coercion ("wrench") attacks, the Deadly-Race impossibility chain,
the No-Gray-Area design bar, and the Great Wall orbit construction that clears
it.

## Files

- `main.tex` — the manuscript.
- `references.bib` — bibliography.
- `Makefile` — build target.

## Build

```sh
make          # -> main.pdf
make clean    # remove build artifacts
```

Requires a TeX distribution with `pdflatex` and `bibtex` (TeX Live / MiKTeX).

## Provenance

Lifted and expanded from the design record; normative sources:

- `papers/deadly-race-coercion-resistance.md` — the paper skeleton this
  manuscript realizes.
- `great-wallet/THREAT_MODEL.md` — the lemmas and the deadly-race framework.
- `next-steps/coercion-resistant-orbit-protocol.md` — the orbit construction.
- `papers/timechain-salt.md` — the companion Namtso salt primitive.

Naming for citation: the **Deadly-Race Lemma** (Villas Boas' Lemma) and the
**No-Gray-Area / Deadly-Race Principle** (Villas Boas' Principle).

> Status: first draft. Parameters, framing, and wording are expected to evolve
> alongside the protocol.
