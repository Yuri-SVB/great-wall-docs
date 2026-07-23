# The Deadly Race — formal wrench-attack threat model (LaTeX manuscript)

First LaTeX manuscript of the coercion-resistance paper: a formal threat model
for physical-coercion ("wrench") attacks, the Deadly-Race impossibility chain,
the No-Gray-Area design bar, and the Time-Gated Perceptual Oracle (TGPO) orbit
construction that clears it (the coercion-resistance protocol underlying the
Great Wall / Great Wallet application).

## Files

- `main.tex` — driver: preamble, title, abstract, and `\input` of each section.
- `sections/` — one file per top-level section (`01-introduction.tex` …
  `08-conclusion.tex`), pulled in by `main.tex` in order.
- `references.bib` — bibliography.
- `Makefile` — build target (rebuilds when `main.tex` or any `sections/*.tex` changes).

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

Naming for citation: the **Deadly-Race Lemma** and the **No-Gray-Area Criterion**.

> Status: first draft. Parameters, framing, and wording are expected to evolve
> alongside the protocol.
