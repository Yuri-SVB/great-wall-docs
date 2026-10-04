# Registry analysis — empirical grounding

Reproducible keyword coding of Jameson Lopp's
[`physical-bitcoin-attacks`](https://github.com/jlopp/physical-bitcoin-attacks)
registry, used for the *Empirical grounding* subsection of the manuscript.

## Reproduce

The registry is a living document: it gained three incidents between the snapshot
used here and 2026-09-03, so fetching `master` does **not** reproduce the paper's
figures. Use the pinned snapshot, which is committed alongside this README:

```sh
python3 analyze.py registry-snapshot-9a4a62a.md --audit audit-9a4a62a.tsv
```

Without `--audit` the script prints its screens raw, which is what to run when
checking the audit rather than citing it. **The raw screens are not the figures
in the manuscript.** See *The audit* below.

To rebuild that snapshot from the source repository rather than trusting the copy:

```sh
git clone --filter=blob:none https://github.com/jlopp/physical-bitcoin-attacks.git
git -C physical-bitcoin-attacks show 9a4a62a:README.md > registry-snapshot-9a4a62a.md
```

## Snapshot used in the paper

- **Source:** `jlopp/physical-bitcoin-attacks`, `README.md`, commit
  `9a4a62a85ee11dfd5dac4bdb569c45f01738dc91` (2026-08-13), the last change before
  the access date. Released to the public domain by its author.
- **Accessed:** 2026-08-14.
- **SHA-256:** `02782ba8f9e190b431ee673a9411ca8a5dca66d1cedc284b15cd39de5957f2b8`
- **Timestamp:** `registry-snapshot-9a4a62a.md.ots`, an OpenTimestamps attestation
  over that file, anchored in **Bitcoin block 965345**. Verify with
  `ots verify registry-snapshot-9a4a62a.md.ots` (needs a Bitcoin node);
  `ots info` shows the attestation without one.
- **Rows:** 352. **Audited incidents: 351** — one Spanish case is entered twice.

| Signal (headline keyword coding) | Incidents | Share |
|---|---:|---:|
| Killed / murdered victim (**audited; a floor**) | 16 | 4.6% |
| Kidnap / hostage / ransom (long-hold) | 123 | 35.0% |
| Armed robbery at gunpoint (short-hold) | 80 | 22.8% |
| Home invasion / break-in / raid | 33 | 9.4% |
| Torture / physical violence | 72 | 20.5% |
| ATM / BTM / machine (not holder coercion) | 12 | 3.4% |

Incidents per year rise from 1 (2014) to a peak of 84 (2025); 2026 is partial
(54 through the access date).

⚠️ **These replace the figures this file carried until 2026-10-04**, which were
18 / 139 / 101 / 40 / 82 / 13 on 352. Every one of them was too high, and for
the same reason: the headline cell is markdown, so it carries two URLs, and the
regexes were matching those as well as the prose. A slug is not evidence. The
clearest case was a non-fatal home invasion in a town called **Killingly**,
Connecticut, which landed in the fatality count through
`.../police-2-rhode-island-women-charged-in-killingly-home-invasion`. `analyze.py`
now strips the URLs before matching. Anything quoting the old numbers needs
re-checking against these: the manuscript, `FRANCE.md`, and the blog.

## Method and caveats (read before citing)

- The registry has **no duration or outcome field** — only date, victim,
  location, and a one-line headline. All coding is on the **headline text**, by
  the regexes in `analyze.py`.
- **Categories overlap** (a kidnapping may also be violent or fatal) and do not
  sum to 100%. Shares are of all 351 audited incidents.
- **Convenience / media sample.** Deterred, unreported, and privately-settled
  cases are structurally absent; coverage is English-biased.
- **Survivorship bias.** A homicide is often reported as a homicide, not as a
  "Bitcoin attack", so the 4.6% fatality share is a **floor**, not an estimate.
  The audit below gives a second, narrower reason it is a floor: one death is in
  the dataset and not in the pattern, because the headline says *strangled* and
  never says she died.
- **Modality is a proxy for duration**, since duration is not recorded:
  gunpoint/home-invasion headlines stand in for short holds; kidnap/hostage/
  ransom for long holds.
- Figures are **directional corroboration** of a decision-theoretic prediction,
  not a hazard model.

## The audit — `audit-9a4a62a.tsv`

**Two rows of this table are screens and not codings**, and both are labelled as
such by the script. A regex over a one-line headline cannot tell a victim's
death from an attacker shot by police, and it cannot tell one incident entered
twice from two incidents sharing a source article. So `analyze.py` reports the
candidates, a human reads them, and the judgements live in
`audit-9a4a62a.tsv` — one line each, with the evidence, so a reader can
disagree with them one at a time rather than having to take the count on trust.

**Fatality: the screen fires 19 times, and the audited count is 16.** Four out,
one in.

| Verdict | Case | Why |
|---|---|---|
| not a death | Riga, 22 Oct 2020 | *"arrested for planning kidnapping and killing"* — a plot, charged before anything happened |
| not a death | Goiania, 24 Jun 2025 | *"Attack failed, 2 attackers were killed by police"* — the deaths are the attackers', and the victim lived |
| not a death | Mulhouse, 22 May 2026 | *"facing death threats"* — a threat, and the victim was found alive |
| duplicate | Spain, 10 Dec 2025 | the same incident as *Southern Spain, April 2025*: both source URLs identical, headlines two words apart |
| **a death** | Gifu, 17 Jun 2017 | *"Woman strangled"* matches nothing in the pattern, but she died — the source is titled *bitcoin murder — Nagoya woman likely killed on evening she went missing* |

The three rejects are three different ways a word can appear without anybody in
scope dying: aimed at the wrong person, aimed at nobody yet, or aimed as a
threat. No pattern separates them, which is the argument for the screen.

That last row is the whole argument for auditing by hand in one case. It is also
the second reason the share is a floor, and the narrower one: the first is that
a homicide gets reported as a homicide and never enters the registry at all,
and this one is a death that *is* in the registry and still not in the pattern.

**Duplicates: the screen fires once, and the audit agrees once.** The screen
looks for rows sharing a source URL, then scores how similarly they are worded.
Twenty pairs share a URL and nineteen are not duplicates — most of them are one
article covering a series of separate attacks on the same victim, as with the
five Salford attacks on Karl Johnson across 2023, all reported in one
*Manchester Evening News* piece. Only the Spanish pair is the same incident
twice, and the wording score separates it cleanly: 0.93 against a next-highest
of 0.43. **The incident count is therefore 351, not the 352 rows.**

## Country cuts — `analyze_country.py`

```sh
python3 analyze_country.py registry.md France
```

Reuses `analyze.py`'s `CATEGORIES` unchanged, so country figures stay comparable to the table above,
and adds a country-vs-global skew column plus a **proximity** axis that `analyze.py` does not have:
was the person coerced the holder, or a relative held to compel one?

**The proximity axis is a screen, not a coding**, in exactly the sense above. It over-fires and
every hit must be read before it is counted — on the 2026-08-14 snapshot it surfaced 16
proxy-victim candidates of which **4 were false positives** (in one, "Son of \<CEO\>" named a
*perpetrator*). The audited count is **12 of 351 (3.4%)**, and that is the figure the manuscript
uses. Never quote the raw screen.

`FRANCE.md` holds the worked France cut, including the audit table and the twelve verified cases.
