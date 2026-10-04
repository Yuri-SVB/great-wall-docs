# Changes in v2

Zenodo concept DOI resolves to this version; v1 (`10.5281/zenodo.22778481`)
remains citable at its own DOI. Baseline for the comparison below is the v1
release.

One kind of change: a correction to the registry coding in §7. Nothing else in
the paper moves — no argument, no classification, no stipulation. The
correction is ours, it is arithmetic rather than interpretive, and it moves
every figure in the same direction.

## The registry coding was too high, in every row

The registry's headline column is markdown, so each cell carries the headline's
prose and then two URLs: an `archive.is` capture and the original article.
`registry-analysis/analyze.py` matched its patterns against the whole cell. A
URL slug is not evidence about an incident, and several of them contain the very
words the patterns look for.

The clearest instance is also the one that mattered most. A non-fatal home
invasion in **Killingly**, Connecticut, was counted as a killing, because the
original article lives at
`.../police-2-rhode-island-women-charged-in-killingly-home-invasion`. Nobody
died; a town's name matched `kill`.

The script now strips the URLs and codes the prose. Two smaller repairs went in
with it: the fatality pattern gained `\bdeaths?\b`, which it had been missing
(`\bdead\b` matches neither *beaten to death* nor *results in death of owner*),
and the snapshot's $352$ rows were screened for duplicates, which found one — a Spanish case entered twice,
under two dates and two location strings, with both source URLs identical. The
incident count is therefore **351**, not 352.

| Signal | v1 | v2 |
|---|---:|---:|
| Killed / murdered victim *(a floor)* | 18 — 5.1% | **16 — 4.6%** |
| Kidnap / hostage / ransom (long-hold) | 139 — 39.5% | **123 — 35.0%** |
| Armed robbery at gunpoint (short-hold) | 101 — 28.7% | **80 — 22.8%** |
| Home invasion / break-in / raid | 40 — 11.4% | **33 — 9.4%** |
| Torture or physical violence | 82 — 23.3% | **72 — 20.5%** |
| Incidents | 352 | **351** |
| Peak year (2025) | 85 | **84** |

**No claim in the paper turns on the difference.** The fatality share is
asserted as a floor and is still a floor; §7's point is that the terminal move
is attested at all, which 16 deaths attest as well as 18 did. The long-hold
skew that §7 builds on got *larger*, not smaller: France against the United
States moves from a tenfold difference in $K{:}G$ to an elevenfold one, because
the global short-hold share fell further than the long-hold share. The
jurisdiction table is recomputed; the ordering is unchanged.

## Two rows are screens, and are now labelled as such

The paper already said this of the proxy-victim count — a keyword screen
surfaced 16 candidates, four were read and discarded, and §7 quotes the audited
12. The fatality row needed the same treatment and had not had it. A pattern
over a one-line headline cannot tell:

- a victim's death from **an attacker shot by police** (Goiania, June 2025:
  *"Attack failed, 2 attackers were killed by police"* — the victim lived);
- a death from **a plot that was only charged** (Riga, October 2020: *"arrested
  for planning kidnapping and killing"*);
- a death from **a threat** (Mulhouse, May 2026: *"facing death threats"* — the
  victim was found alive);
- one incident from **the same incident entered twice**.

Three ways for the word to be there without anybody in scope dying: aimed at
the wrong person, aimed at nobody yet, aimed as a threat.

So `analyze.py` now reports those three things as screens and prints the hits to
be read. The judgements live in `registry-analysis/audit-9a4a62a.tsv`, one line
each with its evidence, and `--audit` applies them. A reader who disagrees with
one can see exactly which case it is.

The audit also runs in the other direction once, and this is the sharpest
argument for doing it by hand. **Gifu, June 2017** reads *"Woman strangled,
attacker takes 100,000 yen worth of BTC"*. That matches nothing in the fatality
pattern. She died: the source article is titled *bitcoin murder — Nagoya woman
likely killed on evening she went missing*. So a death sits in the registry,
visible to a reader and invisible to the regex. It is a second and narrower
reason the share is a floor than the one §7 gives — the first is that a homicide
is reported as a homicide and never enters the registry at all; this one is a
death that did enter it and still did not get counted.

## What a reader should re-check

Anything quoting v1's numbers. Inside this repository that was
`registry-analysis/README.md`, `registry-analysis/FRANCE.md`,
`registry-analysis/france-cut.txt`, one cross-reference in the companion's §5,
and §1 and the abstract of this paper, all updated here. The registry itself is
Jameson Lopp's and the duplicate row is worth reporting upstream.
