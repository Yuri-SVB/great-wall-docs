# France cut of the registry — findings

**Snapshot:** `jlopp/physical-bitcoin-attacks` `README.md`, branch `master`, fetched **2026-08-14**.
**352 incidents; 61 with France in the location column.**
**Reproduce:** `python3 analyze_country.py registry.md France` (raw output in `france-cut.txt`).

Coding reuses `analyze.py`'s `CATEGORIES` verbatim, so every category number here is directly
comparable to the global table in the manuscript. One axis is new and is flagged as such.

---

## 1. Scale and trend

| Year | France | Global | France share |
|---|---:|---:|---:|
| 2017–2024 | ~1/yr | 12–42/yr | 0–8% |
| **2025** | **22** | 85 | **25.9%** |
| **2026** (to Aug) | **34** | 54 | **63.0%** |

**61 of 352 incidents — 17.3% of the entire global registry**, from a country with about 0.9% of
world population. France is the largest national cluster in the dataset by a wide margin, and
**nearly two thirds of everything recorded worldwide in 2026 is French.**

⚠️ **Do not present the 63% as a pure incidence claim.** The registry is a media/convenience sample
with English-language bias, and French wrench attacks became a sustained national news story after
the Balland kidnapping in January 2025. Intense domestic coverage plausibly raises the rate at which
French cases *enter the registry at all*, independently of how many occur. The honest statement is:
**France dominates what is recorded**; how much of that is incidence versus visibility is exactly the
question someone with non-public French data could answer and this dataset cannot.

## 2. Monthly 2026 — the curve turns after June

```
2026   Jan  Feb  Mar  Apr  May  Jun  Jul  Aug
        8    4    8    4    4    4    1    1
2025   Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
        3    1    0    0    4    2    1    3    1    2    2    3
```

A steady 4–8/month through June 2026, then a sharp break to 1 in July and 1 in August. That is
**consistent with** the French prosecutions reported in 2026 (88 charged, including minors) having a
deterrent effect.

⚠️ **It is consistent with, not evidence of.** Registries lag: an incident must be reported, archived
and submitted before it appears, so the two most recent months are *always* undercounted. The July
break is sharp enough to be interesting and soft enough that it must be re-checked in October.
**This is the single most useful thing on this page to put in front of someone tracking French
crypto crime** — they may already know whether the drop is real.

## 3. Modality — France is skewed toward exactly the attack the paper models

| Category | France | Global | Skew |
|---|---:|---:|---:|
| **kidnap / hostage / ransom (long-hold)** | **57.4%** | 39.5% | **+17.9pp** |
| **armed robbery at gunpoint (short-hold)** | **8.2%** | 28.7% | **−20.5pp** |
| home invasion / break-in / raid | 11.5% | 11.4% | +0.1pp |
| torture / physical violence | 16.4% | 23.3% | −6.9pp |
| killed / murdered *(floor)* | 1.6% *(n=1)* | 5.1% | −3.5pp |
| ATM/BTM (not holder coercion) | 0.0% | 3.7% | −3.7pp |

**This is the theoretically important finding.** The manuscript uses modality as its proxy for
*duration* — gunpoint and home-invasion headlines stand in for short holds, kidnap/hostage/ransom for
long ones. France is not merely having more attacks; it is having **long holds**, which is precisely
the regime where the Deadly-Race Lemma bites: a long hold gives the attacker time to work a
"feasible but slow" recovery path, and release-then-race is the operative endpoint. A gunpoint
robbery is much closer to a clean loss.

⚠️ **The obvious counter:** the same media dynamic that inflates French entry into the registry
would also favour *kidnappings over muggings*, since kidnappings are more newsworthy.

**There is an internal check, and the skew survives it.** Taking the long-hold:short-hold ratio
(K:G) by jurisdiction:

| Jurisdiction | n | Kidnap | Gunpoint | K:G |
|---|---:|---:|---:|---:|
| Brazil *(small n)* | 12 | 75.0% | 8.3% | 9.0 |
| Spain *(small n)* | 8 | 62.5% | 12.5% | 5.0 |
| **France** | **61** | **57.4%** | **8.2%** | **7.0** |
| India *(small n)* | 12 | 58.3% | 33.3% | 1.8 |
| Canada | 18 | 44.4% | 27.8% | 1.6 |
| *Global* | *352* | *39.5%* | *28.7%* | *1.4* |
| **United States** | **59** | **28.8%** | **40.7%** | **0.7** |
| Russia *(small n)* | 10 | 30.0% | 50.0% | 0.6 |

**France and the United States are the two largest national subsets, near-identical in size (61 vs
59), with inverted compositions — a tenfold difference in K:G.** The media-inflation story explains
a *level* (the registry over-counts drama everywhere) but not this *ordering*: it would have to
claim French reporting is ten times more kidnap-selective than American, in a market at least as
heavily covered. The ordering also tracks plausible real-world causes — the gunpoint-heavy end is
the US and Russia, the kidnap-heavy end France, Brazil and Spain.

⚠️ **Two confounds survive.** Outside France and the US the subsets are too small to argue from.
And the coding runs on English-language headlines, several translated — if French sources reach for
"kidnapped" where American ones reach for "robbed at gunpoint," part of this spread is vocabulary
rather than events. **That is a good question for him**, and one he can answer from French-language
sources that this coding cannot see.

France's fatality rate reads *lower* (1.6% vs 5.1%) — consistent with professionalised
kidnap-for-ransom being economically rather than lethally motivated — but **n = 1**, so it is noise.
Do not use it.

## 4. ⭐ Who gets seized — the proxy-victim finding

New axis, not in the manuscript's published coding. Coded on the headline; all nine French cases
were read individually and none is a false positive.

| | France | Global |
|---|---:|---:|
| family member / partner named | **36.1%** | 15.9% |
| associate / colleague / employee named | 3.3% | 4.0% |
| **PROXY VICTIM — a relative seized to reach the holder** | **14.8%** *(n=9)* | **3.4%** *(n=12)* |

⚠️ **The global figure is the audited one, not the screen's.** The keyword screen surfaced **16**
candidates worldwide; reading each one individually discards **four**:

| Rejected | Why |
|---|---|
| 2022-06, Osaka | *"Son of Mitsubishi Electric CEO + 7 men kidnap, torture gym member"* — "son of" names a **perpetrator**, not a victim. |
| 2025-07-15, Ahmedabad | The trader himself was assaulted; the father appears only as the person who called police. |
| 2025-09-28, Tierp | A family robbed collectively; no proxy structure stated. |
| 2025-11-26, Vienna | The son revealed **his own** wallets; being a mayor's son is incidental. |

**Twelve survive. France holds nine of them — 75% of every verified case worldwide — at 4.3× the
global rate.** The audit strengthened the contrast rather than weakening it: all nine French cases
survived, all four rejects were non-French. The nine:

| Date | Case |
|---|---|
| 2023-08-24 | Father of a Malta-based gaming influencer kidnapped |
| 2025-01-01 | Crypto influencer's father kidnapped on New Year's Eve |
| 2025-05-01 | Father of a crypto millionaire abducted; €5M demanded; finger severed |
| 2025-05-13 | Attempted abduction of a crypto exchange CEO's daughter |
| 2025-10-01 | Woman and two children threatened to blackmail her husband |
| 2025-12-01 | Father of a Dubai-based crypto entrepreneur kidnapped |
| 2025-12-12 | 17-year-old kidnapped to blackmail his older brother, a trader in Dubai |
| 2026-01-14 | Couple kidnapped for their son's €8M in cryptocurrency |
| 2026-01-25 | 74-year-old kidnapped to extort cryptocurrency from his son |

### Why this matters to the argument

**It is the hostage-token mechanism, observed.** §`sub:hostage` derives the fifth property — no
hostage token — from the theory. These nine cases are the empirical instance: the attacker does not
need the holder's cooperation to be *possible*, only to be *compelled*, and a relative is the
compulsion. A holder in this position has no cryptographic move at all.

**It puts a number on the objection from the talk.** Asked *"why not a remote co-signer holding a
necessary-but-insufficient share?"*, the answer given was that it breaks the self-custody premise and
that Balland shows remote coercion happens anyway. The proxy data sharpens that into something
quantitative: **R2 clears the bar only when the delegate is genuinely beyond reach, and in France the
most natural choice of delegate — a spouse, a parent, an adult child — is inside the attacker's reach
in one case out of seven.** Not an argument against R2; an argument about *who is allowed to be the
delegate*, and evidence that the usual answer fails.

⚠️ **The coding is coarse in one direction only.** A headline that does not name a relative is not
evidence none was involved, so 14.8% is a **floor**. It cannot be inflated by the coding, only
understated.

---

## What to do with this

**For the September call.** Sections 2 and 4 are the material — the July/August break he may be able
to confirm or refute from non-public sources, and the proxy-victim cluster, which is his beat stated
in numbers he probably does not have in this form. Lead with the caveats; an analyst trusts the
person who volunteers the confound first. **Ask more than you tell:** does the drop hold; does French
non-public data show the same long-hold skew; is proxy victimisation a French tactic or a French
reporting artefact.

**For the manuscript.** The proxy-victim number belongs in the empirical-grounding subsection as
support for the fifth property, and the France long-hold skew is worth a sentence: the model's
operative regime is where the incidents are concentrating.

**Before anything is published or quoted**, re-fetch and re-run — the registry changes weekly, and
these numbers are a 2026-08-14 snapshot.
