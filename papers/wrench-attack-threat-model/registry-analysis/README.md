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
- **Accessed:** 2026-08-14.
- **Incidents:** 352.

| Signal (headline keyword coding) | Incidents | Share |
|---|---:|---:|
| Killed / murdered victim (**lower bound**) | 18 | 5.1% |
| Kidnap / hostage / ransom (long-hold) | 139 | 39.5% |
| Armed robbery at gunpoint (short-hold) | 101 | 28.7% |
| Home invasion / break-in / raid | 40 | 11.4% |
| Torture / physical violence | 82 | 23.3% |
| ATM / BTM / machine (not holder coercion) | 13 | 3.7% |

Incidents per year rise from 1 (2014) to a peak of 85 (2025); 2026 is partial
(54 through the access date).

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

## Country cuts — `analyze_country.py`

```sh
python3 analyze_country.py registry.md France
```

Reuses `analyze.py`'s `CATEGORIES` unchanged, so country figures stay comparable to the table above,
and adds a country-vs-global skew column plus a **proximity** axis that `analyze.py` does not have:
was the person coerced the holder, or a relative held to compel one?

**The proximity axis is a screen, not a coding.** It over-fires and every hit must be read before it
is counted — on the 2026-08-14 snapshot it surfaced 16 proxy-victim candidates of which **4 were
false positives** (in one, "Son of \<CEO\>" named a *perpetrator*). The audited count is **12/352
(3.4%)**, and that is the figure the manuscript uses. Never quote the raw screen.

`FRANCE.md` holds the worked France cut, including the audit table and the twelve verified cases.
