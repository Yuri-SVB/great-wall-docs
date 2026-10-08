# Changes in v2

Zenodo concept DOI resolves to this version; v1 (`10.5281/zenodo.22778481`)
remains citable at its own DOI. Baseline for the comparison below is the v1
release.

Two kinds of change. First, a correction to the registry coding in §7: ours,
arithmetic rather than interpretive, and it moves every figure in the same
direction. Second, §2 names the adversary's belief regime and §4 gains a
conjecture that belongs to this paper's register rather than the companion's.
No classification moves and no stipulation is withdrawn.

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


## §2 names the belief regime, and this paper works in the Bayesian one

The companion's v5 splits what was a single buried stipulation into two: NNPP,
the epistemic impossibility that binds every attacker, and the *belief regime*,
the modelling choice about what the attacker does with it. The regimes are
`WDY^dog`, which pins the posterior on "an undisclosed copy remains" at 1 and
never moves it, and `WDY^Bay`, which carries a prior and updates. They are
orthogonal to `(W,c,t)`.

§2 restates the pair and says which one this paper uses. **The Spiral is a
`WDY^Bay` phenomenon, and that is not a convenience.** A bar must hold against
the attacker who cannot be moved, so the Race is argued against `WDY^dog`. But
what the Spiral describes is a denial *losing its informational value*, and a
denial can only lose value for an attacker who would otherwise have updated on
it. Against `WDY^dog` there is nothing to deplete, because nothing was ever
going to be believed. The same split explains the division of labour the two
papers already observed on other grounds: the Race prices the outcome, against
the attacker who does not update; the Spiral prices the duration, against the
one who does.

## §4 gains the Scheherazadian bargain, as a conjecture

A `WDY^Bay` attacker who has updated his way to being satisfied that he holds
everything may still not release, because a released holder with a feasible path
is a competitor: detention buys the same assurance as the terminal move at a
fraction of the judicial disutility. Gray-area vulnerability therefore prices
**custody as collateral on the holder's own abstention** — and the conjecture is
that the holder, having run the same arithmetic, volunteers for it. *Take me
with you, and you will know I am not racing you.*

**What is traded is non-racing, and the section says so before drawing the
analogy.** The same captivity makes a second thing possible — more hours of
coercion may extract more than a released holder would ever have surrendered —
and the two must not be run together. That second thing is real and it is this
paper's duration mechanism, but in it the two parties want opposite things and
the holder volunteers for nothing. The bargain is the one case in which the
interests *align*: the holder keeps his life, and the attacker collects the
pivotality increment π that the terminal move would have bought him — a holder
in custody is a holder not racing — at a judicial disutility below `c`. Nothing
is disclosed to buy it. What the holder supplies is being held.

It is fenced: a lead-in saying it is a conjecture and that nothing else rests on
it, and a statement that there is no empirical evidence of any particular
instance. The silence is over-determined by this paper's own §6 — a headline
records that a holder was held for eleven hours, never whether those hours went
on interrogation or on waiting for a path to clear — which is why it is set down
rather than withheld.

The section is explicit about what the name does and does not carry. The analogy
holds on exactly two things: volunteering into custody to avert a killing, and
custody accepted in place of the terminal move in exchange for something — the
king buying the end of the story, the attacker the same race advantage at a lower
judicial price.

**The remote delegate is not an escape, and the section says so deliberately.**
An earlier draft argued the opposite — that custody cannot deliver what it is
bought for, since by NNPP the attacker can never rule out an access-dominating
delegate beyond his reach. That reasons in the holder's favour, which is the
wrong direction for an *a fortiori* model, and it is empirically false besides:
abductions happen, so real attackers proceed, on a good guess. Custody without a
remote party able to lock its owner out has plain advantages over custody with
one; many holders choose it for that reason; under Kerckhoffs the attacker knows
both; and where subjugation is fast a delegate may not learn of the encounter in
time to intervene. Pricing that probability is more machinery for a weaker bar,
so the attacker proceeds as though there is none.

It is then not a reprieve, on two counts. It **strengthens** the Criterion
rather than softening it, since it converts a robbery into a kidnapping. And the
**alignment expires**, which is now set out formally. Writing `R` for the racer
set and `p_A(S)` for the attacker's probability of prevailing against `S`, the
three moves separate: holding and the terminal move both buy `p_A(R\{V})`,
release buys `p_A(R)`. The first two differ only in price and tenure —
**detention rents what the terminal move buys outright**. With `κ` the
per-period cost of a hold, undiscounted, there are three pairwise comparisons
and so two horizons: the hold beats release while `κT < πW` and beats the
terminal move while `κT < c`, so it runs to the earlier of `πW/κ` and
`T* = c/κ`. The Lemma's condition is exactly the switch between them — `πW > c`
iff `T*` is the earlier — and the bargain lives only in that half, since only
there is there a killing for the holder to avert. In the other half the attacker
may still detain, but on his own account, with nothing offered and nothing
agreed. Where the bargain lives, the holder buys a postponement of at most
`c/κ`; absent new information an attacker who expects at the outset to hold past
`T*` does better to kill at once. The hold has one end that is not the terminal
move — the attacker completing the spend, after which `π = 0` — but it turns on
his residual latency, and by NNPP release never becomes free on the evidence the
holder supplies. `π` is defined relationally where it is first used, and
reconciled with the `(1−p_A)W` form the borrowed Lemma states. Scheherazade's payment is
renewable and hers to withhold, which is how she reaches night 1001; what the
holder supplies is supplied by the attacker's own act of holding him, so he has
no lever and nothing to renegotiate with. In the book she is pardoned on the
thousand and second morning; the registry records no counterpart to that
morning.

The route does not escape the Spiral. It feeds into it by a second road: the
Spiral's duration is epistemic deadlock, this is a strategic hostage problem,
both produce the same observable, and §6's first mechanism is why no registry
column will ever separate them.

## On deposit

Post 006 and its four translations carry a fence saying the conjecture is "not
in the paper, with no DOI behind it". True until this version and the
companion's v5 are deposited, false the moment they are. Rewrite that fence in
the same week the deposit happens.


## §2's route list contradicted the corollary on its own next line

"Clearing the bar **while holding all four** leaves two routes" is false of the
second route. The companion's Cor. 2 says R2 makes custody *shared*, at the cost
of a trusted party, so the remote delegate spends Property 2 — and Cor. 3, which
the line cited, is what says the tacit route is the only one that keeps all
four. The scoping clause is dropped, the two-route count now cites Cor. 2, and
each route carries what it costs. Found while checking §4's new delegate
paragraph against the companion; it predates that paragraph.


## §4.1, second pass

Four corrections, all Yuri's.

**`r` was used and never defined.** The discount rate appeared in "the `r=0`
case" with nothing introducing it. Both papers now just say no time preference
is modeled.

**"The hold runs until T*" implied the hold always happens.** It does not: the
attacker holds iff his arithmetic at the moment says so. And the consequence of
saying it properly is a concession the section had been refusing — **where he
does hold, the holder is alive who would otherwise be dead, and that is a real
reprieve**, bounded at `c/κ` and priced in the attacker's parameters. "It is not
a reprieve, on two counts" became "What it buys, and what that costs". The
second count is the one that does the work: the killing being postponed is one
the gray band created, so the concession is the charge against the band rather
than a defense of it.

**The holder's willingness is not a free variable in the idealized model.** The
adversary is granted complete subjugation and the holder's full cooperation, so
an abduction happens iff the attacker chooses one. The volunteering is not a
mechanism of that model at all — it means something only as one moves toward the
real encounter, which is a second and better reason the conjecture lives in this
paper and in the Bayesian regime.

**The no-delegate simplification moved to the companion**, as its `rem:nodelegate`
— see that paper's changelog. It was stated here as "the attacker for whom the
bargain is most attractive", which undersells it: pinning the delegate's
probability at zero maximizes assessed pivotality and so the payoff of *every*
move the Lemma prices. The bar is DR-safety, not bargain-safety. §4.1 keeps a
two-line pointer.

Also: "the Spiral's duration is epistemic deadlock" in the closing became "the
abduction's duration", since the sentence contrasts two mechanisms producing one
observable, and the observable is the abduction.


## §4.1, third pass: the prose stays here, the arithmetic goes to the companion

The section was cut back to prose. The three-move table, `π` defined
relationally, the two horizons `πW/κ` and `T* = c/κ`, and the bounded-reprieve
derivation now live only in the companion's `rem:scheherazade`, which is the
right home for them: this paper's register is duration and the reader it is
written for, and an optimal-stopping calculation in the middle of a conjecture
was carrying more apparatus than the claim needs. The entries above describing
that material as §4's remain accurate about what was argued and when; they are
wrong about where it ended up. The companion's pointer was corrected to match —
it had promised that this paper "works the three moves out in full".

What stays here: the bargain, the tale, the two things the analogy holds on,
the two the model settles first (the undemonstrated delegate, and the holder's
preference being no free variable under complete subjugation), the concession
that the trade also buys the attacker longer coercion, and the closing on the
two roads to one observable.

**Added: a worked hypothetical.** The holder offers an exit route, names an
alarm and offers to disable it, and the attacker takes the bargain with the
terminal move still to hand. It is there to show the one thing the idealized
model cannot: that the holder's preference can be load-bearing once the
attacker is one whose assessment moves, because what the holder volunteers is
intelligence a real attacker, mid-encounter, might not have noticed, thought to
extract, or been able to act on in time.
