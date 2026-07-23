# Registry analysis — empirical grounding

Reproducible keyword coding of Jameson Lopp's
[`physical-bitcoin-attacks`](https://github.com/jlopp/physical-bitcoin-attacks)
registry, used for the *Empirical grounding* subsection of the manuscript.

## Reproduce

```sh
curl -sSL https://raw.githubusercontent.com/jlopp/physical-bitcoin-attacks/master/README.md -o registry.md
python3 analyze.py registry.md
```

## Snapshot used in the paper

- **Source:** `jlopp/physical-bitcoin-attacks`, `README.md` (branch `master`).
- **Accessed:** 2026-07-19.
- **Incidents:** 342.

| Signal (headline keyword coding) | Incidents | Share |
|---|---:|---:|
| Killed / murdered victim (**lower bound**) | 18 | 5.3% |
| Kidnap / hostage / ransom (long-hold) | 133 | 38.9% |
| Armed robbery at gunpoint (short-hold) | 93 | 27.2% |
| Home invasion / break-in / raid | 35 | 10.2% |
| Torture / physical violence | 78 | 22.8% |
| ATM / BTM / machine (not holder coercion) | 13 | 3.8% |

Incidents per year rise from 1 (2014) to a peak of 82 (2025); 2026 is partial
(47 through the access date).

## Method and caveats (read before citing)

- The registry has **no duration or outcome field** — only date, victim,
  location, and a one-line headline. All coding is on the **headline text**, by
  the regexes in `analyze.py`.
- **Categories overlap** (a kidnapping may also be violent or fatal) and do not
  sum to 100%. Shares are of all 342 incidents.
- **Convenience / media sample.** Deterred, unreported, and privately-settled
  cases are structurally absent; coverage is English-biased.
- **Survivorship bias.** A homicide is often reported as a homicide, not as a
  "Bitcoin attack", so the 5.3% fatality share is a **floor**, not an estimate.
- **Modality is a proxy for duration**, since duration is not recorded:
  gunpoint/home-invasion headlines stand in for short holds; kidnap/hostage/
  ransom for long holds.
- Figures are **directional corroboration** of a decision-theoretic prediction,
  not a hazard model.
