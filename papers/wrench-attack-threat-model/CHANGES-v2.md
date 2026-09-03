# Changes in v2

Zenodo concept DOI resolves to this version; v1 (`10.5281/zenodo.22018892`) remains
citable at its own DOI. Baseline for the comparison below is the v1 release of
19 August 2026.

Four kinds of change: corrections to claims v1 got wrong, arguments added or
strengthened, a repair to the provenance and reproducibility of the cited record,
and a rebuilt treatment of BitVault. The classification of every design is
unchanged; what changed is what the paper is willing to assert, and on what
evidence a reader can check it.

## Corrected

**The proxy-victim finding is not the hostage token.** v1 called the field cases
where an attacker coerces a relative or associate "the hostage token of §3.7
observed in the field". They are a different mechanism. The hostage token is a
*seizable object* the protocol requires, which devicelessness removes by leaving
no such object; a proxy victim is a *person*, whom no custody design renders
unseizable. What the subset shows is clause D7 failing, not the hostage token in
the wild. §3.7's scope narrows with it, from immunity to indirect coercion to
immunity to indirect coercion *through a seizable token* — a qualifier that is
load-bearing.

**64\* is not the softest number.** v1 described 64\* as "the softest number handed
to the attacker". The softest number is plain cheap 2^64 at the feasibility
border; the star denotes memory- and depth-hardness, which makes 64\* harder, not
softer.

**32\* is stated as feasible.** Neither S1 nor S2 settles the star at 32 bits, so
the feasibility line now says outright that 32\* is feasible: memory-hardness alone
does not lift a single 32-bit stage over the floor, which is why no orbit link
commits fewer than 64 bits.

**The Coldcard precedent is softened.** v1 claimed more about what the vendor's
guidance shows than the guidance supports; the epistemic claim now matches the
source.

**Observation weakened to realisation.** The entropy-health analogy said a holder
"cannot observe from outside" whether custody is sound; it now says a holder
"might not realise", which is what the analogy actually needs.

## Added and strengthened

**The uniformly-distrusting simplification is stated, not implied.** §2 now says
explicitly why the model does not let the attacker read truthfulness off a
terrorized victim's demeanour: the alternative is a nightmarishly complex bluffing
game, and the one competing simplification — a gullible attacker — is trivially
sub-NNPP and sub-Kerckhoffs, hence useless as a threat model. Erring toward
distrust is the only valid choice and is what makes the model *a fortiori*. The
passage also says plainly that the paper will not encourage real users to bet
their stashes, and their lives, on a bluff landing.

**The decoy is sold, and coached for credibility.** A new remark records that the
decoy is not merely tolerated but marketed: a Spanish-language consultancy lists a
decoy wallet among paid tiers as protection against coercion, and published
guidance coaches the performance, instructing that the decoy balance be
*believable*. That instruction is the naive tier stated as a training objective.

**The effort budget already exists, and is being misspent.** §7 pairs the
dice-rolling adoption precedent with that market: holders already pay for
consulting that builds a decoy. Effort tolerance is not a constant of the
population, and it is already being spent — on the one of the two methods that
theory and the record jointly condemn.

**A perceptual oracle is worth its price only on the tacit route.** A new remark
condenses what were three separate treatments of geography-gated, delegate-gated
and obscure oracles into one argument: the oracle's price buys exactly the
conjunction of the Four Properties, so a variant that relaxes one of the four has
spent the price on the benefit it gave up, and is dominated by the plain protocol
that yields the rest. The obscure variant fails twice over and is not merely
dominated but ineffective.

**Acts versus omissions on the remote-delegate route.** v1 used the Balland case to
argue that a human delegate always fails, since coercion routes through the victim
and a humane delegate pays. That holds where the delegate must *do* something — an
act is self-verifying. It does not transfer where the delegate must *abstain*:
abstention has no verifiable permanence, and by NNPP the delegate cannot be made to
demonstrate that no retained means of cancelling exists. The incentive inverts with
it, and the section records the cost, so the route reads as an honest trade rather
than a solution.

**A fifth avenue against the geographic route.** Burgling one gating site and
keeping what he takes: a token K needs but the attacker cannot use alone is
leverage rather than a route — a hostage token held against the victim for the
rest.

**A vendor documents the regress.** Coldcard's own firmware guidance, for the case
where the duress wallet is disbelieved, advises escalating to the brick PIN — the
manufacturer contemplating an informed attacker and recommending an irreversible
erasure performed with the victim still in the room. Two further admissions on the
same page are now quoted. The first concedes the decoy is distinguishable to an
attacker who verifies, and offers as remedy not a repair but a request, that
readers report revealing sequences so the vendor can "cover them up better" — that
is obscurity stated as a maintenance programme, and the clearest statement we have
found of what non-obscurity rules out, since what is defended is not
indistinguishability but the current state of the disclosure backlog. The second
offers the denial move outright: the holder may say the duress PIN was set once and
since forgotten — a proposition about the holder's own knowledge, which NNPP says
the holder cannot close. Escalation and denial are the document's two exits, and
both are the naive tier.

**Obscurity anosognosia.** A new remark names why the crisis resists diagnosis. Two
censoring mechanisms compound: obscurity does not advertise itself, so no victim's
exposure to an obscurity-dependent design is on record, and a homicide is reported
as a homicide, so the enactments most diagnostic of the Lemma are the least likely
to be counted. The numerator is censored by how the terminal event is classified,
the covariate by what vendors do not say. The structure is that of anosognosia —
one cause, two effects, the second concealing the first. The remark draws no
empirical claim, because it cannot, which is the point: the diagnosis is not
available from the data by waiting, and that is the argument for deriving the bar
rather than measuring it. Four passages now defer to it, including the registry's
own statement of its limits.

**The coached decoy defeats itself in aggregate.** Publicised training raises the
prior that a fluent denial was rehearsed: once the attacker knows credibility is
taught and sold, fluency stops being evidence of truth and becomes evidence of
coaching. The remedy degrades the thing it sells, and not only for its customers —
a holder who never trained now denies into an attacker who discounts fluent denial
generally, so the cost falls on people who bought nothing. It is the Obscurity
Paradox run backwards, and it answers the decoy-market remark's own concession that
a better-rehearsed lie helps at the margin: in aggregate it does not.

**The Obscurity Paradox is stated once.** It was developed twice, in §3 and §5;
§3 now names it and defers, and the argument lives in one place.

## Provenance and reproducibility

**The empirical analysis did not reproduce, and now does.** This is the most
consequential correction in v2, and it is ours rather than a vendor's. The attack
registry is a living document, and `registry-analysis/README.md` told reproducers
to fetch its `master` branch. That branch has moved: it now yields 355 incidents
rather than the 352 the paper reports, so the figures in the empirical subsection
could not be reproduced as shipped. The analysis is now pinned to commit
`9a4a62a` of 13 August 2026, the last change before the stated access date, and
that commit reproduces 352 and every sub-figure exactly. The snapshot is committed
alongside the script — the registry is public-domain, so redistribution is
unambiguous — with its SHA-256 recorded and an OpenTimestamps attestation anchored
in **Bitcoin block 965345**. The body now cites the registry at that commit rather
than at an access date.

**Every cited web page has a third-party capture.** Twenty-one archive.today
permalinks are recorded, each in the bibliography entry for its source, and
indexed in `sources/ARCHIVE-RECORD.md`. Several of these citations are vendor
documentation that §5 classifies in ways its vendors would not choose, and none of
it is version-controlled upstream; a page can be revised or withdrawn without
notice, and the citation then no longer supports the sentence resting on it.

**Fifteen of those pages also have a local snapshot**, under `sources/web/`, with a
manifest of URLs, fetch times and SHA-256 digests timestamped into Bitcoin block
965345. The two layers are kept because they fail differently: an archive service
can go dark, whereas a local snapshot plus an anchored hash depends on no service
and holds the page body as text, so a later revision can be diffed rather than
merely detected. Two pages have a capture but no snapshot, both sites having
declined automated retrieval.

**Sources that live in git are pinned by commit** rather than archived, which is
stronger: anyone can verify a pin against upstream without trusting a copy of
ours. That covers the registry at `9a4a62a` and Coldcard's `pin-entry.md` at
`7fc656a`, the latter carrying the direct quotations above. Both quotations, and
the three added in v2, were verified against that commit.

**The cited livestream is timestamped by digest.** A capture of the page is not a
capture of the video, and the recording is too large to belong in the repository,
so `sources/` records the SHA-256 of two offline downloads and timestamps that
record. What this proves is narrow and is stated as such: the downloads came
through a third-party service, so each is a re-encode whose digest has no
canonical relation to the original. Provenance for the citation rests on the
capture; the stamp only lets a copy produced later be matched against a record
fixed at a known date. That attestation is anchored in **Bitcoin block 965356**.

Two citations to Blockstream's help centre now use the canonical paths its
retired article URLs redirect to, and the three remaining short archive links are
replaced by dated permalinks, which name a capture rather than resolving to
whatever a short code currently maps to.

## BitVault, rebuilt

**The architecture.** v1 described cancellation as routed to the owner's alert
wallet, referred to coercing "the cancel key", and put the spend behind only a
delay with keys on the seized device. The alert endpoint holds no spending or
cancellation key, and the rest does not hold either. Per the B-SSL concept
whitepaper of 11 October 2025, spending paths carry timelocks: a primary needing a
custodian co-signature behind a configurable 2 h–15 d relative CSV, a one-year
fallback on the user's own two keys, and a three-year custodian path, the last two
with no gatekeeper. The delay is a maturation from funding, not a window on a
request, and the multi-year locks are absolute and do not re-arm.

**Cancellation is not reversal.** A rejection stops a pending authorisation. Once
the required signatures and timelocks are satisfied the transaction cannot be
reversed.

**Reclassified.**

| Property | v1 | v2 |
|---|---|---|
| Knowledge-based | ✗ | **?** |
| Individual custody | ✓ | **✗** |
| Non-obscurity | ✗ | **?** |
| Coercion resistance | ✗ | ✗ |

Individual custody fails in both directions: the optional off-chain gatekeeper can
deny the user the quick path by declining to release the custodian's co-signature,
and past the three-year lock a custodian and that gatekeeper can spend together.
Knowledge-based is undetermined because nothing in the construction forbids running
it from memorized seeds. Non-obscurity is undetermined because obscurity does not
advertise itself: the deadly-race exposure is plain enough on the published policy
that a Kerckhoffs-aware design would not ship it, so the design suggests an
attacker assumed ignorant of it, while the only other reading is an attacker
assumed willing to coerce but not to kill — a wager on his murder cost staked on
the holder's life.

**The finding, as two cases.** Before the one-year date the attacker coerces both
user keys and kills, the only party who would tell the gatekeeper to withhold being
the victim, so removal is what buys settlement. After it he coerces both and spends
at once, ungatekept. v1's claim that the attacker faced a slow path while a
released victim held a fast one is withdrawn: there is no fast path for the victim,
since the primary path needs the custodian's co-signature. The victim is pivotal as
the witness, not as a racer.

**Sources.** No authoritative specification is published. The vendor describes the
product as "100% Open Source," but its code link resolves to an organization with
no public repositories, and its documentation and audit are served through a gated
document-sharing service. The account rests on the vendor's pages, the
self-attributed concept whitepaper hosted outside the vendor's own links, and
correspondence of 26–27 August 2026 (all accessed 1 September 2026); they do not
agree in every particular. Snapshots accompany each, and `sources/` keeps the
whitepaper with an OpenTimestamps attestation anchored in Bitcoin block 965103.

This bounds what is claimed and is **not** an allegation. We have no evidence that
any material was withdrawn, and observed none at any earlier time.

The "publicly verifiable, making kidnapping attempts pointless" formulation is no
longer carried on the vendor's site and is treated as a former formulation the
company has acknowledged as too categorical.

## Other

The Jade Clock is renamed the **Flying Turtle** throughout, matching the design
documentation it cites.

The AFT 2024 wrench-attack citation, which v1 carried with `author = {Anonymous}`
and a stub venue, is completed: Ordekian, Atondo-Siu, Hutchings and Vasek, LIPIcs
vol. 316, 24:1–24:24, with editors, publisher and DOI.

Nine references are new: the B-SSL whitepaper, Coldcard's trick-PIN and PIN-entry
documentation, Trezor's wipe-code documentation and the declined
concealment request, the Flying Turtle module, the consultancy service listing, the
passphrase guide that coaches the decoy, and the self-custody programme.

LaTeX build artifacts committed to v1 by mistake are untracked.

Overfull lines are cleared: a full-width table opened an indented paragraph, so
the paragraph indent pushed it past the right margin, and the remaining cases were
inline math with no legal breakpoint.

## Relation to the conference submission

This version and the anonymised conference submission share their argument but are
no longer identical in content. The submission is bound by a twenty-page limit;
this version is not, and carries material that did not fit — chiefly the two
further Coldcard admissions above, and the fuller treatment of the two fielded
cases, which the submission compresses. Where the two differ, this version is the
more complete statement.

## Attribution

The architectural description of BitVault is the company's; the classification
drawn from it is the author's, and is relative to this paper's threat model.
