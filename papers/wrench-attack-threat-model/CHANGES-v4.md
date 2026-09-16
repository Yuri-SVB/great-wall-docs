# Changes in v4

Zenodo concept DOI resolves to this version; each earlier version remains citable
at its own DOI.

| Version | DOI | Published |
|---|---|---|
| v1 | `10.5281/zenodo.22018892` | 19 August 2026 |
| v2 | `10.5281/zenodo.22287553` | 3 September 2026 |
| v3 | `10.5281/zenodo.22549552` | 6 September 2026 |
| v4 | `10.5281/zenodo.22778256` | 15 September 2026 |

Baseline for the comparison below is **v2**, not v4. Versions 3 and 4 shipped
without changelogs, so this document absorbs them; each entry names the version
it landed in, so a reader holding an intermediate deposit can locate themselves.

The largest change is structural: the manuscript is now two papers. Beyond that,
three claims were made rigorous that v2 stated loosely, one vendor-documented
instance of the naive tier was added, a second mechanism was named and given a
fourth censoring mechanism, and the design comparison gained an axis that the
four properties do not generate. No design's classification changed.

## The manuscript is now two papers *(v4)*

**The split.** The obscurity class, the mechanism now called the Denial Spiral, the
praxeological reading, the four censoring mechanisms and the registry method and
coding tables are a companion paper, *The Denial Spiral: How a Norm of Denial
Prolongs Coercion, and Why the Field Cannot Measure the Damage*. The cut is along
the epistemic boundary — protocols here, why the field cannot see them there —
rather than along the boundary between the two mechanisms, because the registry
method and the censoring argument are one subject and belong together.

**What this paper keeps.** The Deadly Race, the No-Gray-Area Criterion, the
reachability dichotomy and trichotomy, the TGPO construction, and the
classification of what is deployed. The obscurity and registry subsections are
compressed to the stipulations they ground and cite the companion for the rest:
the classification section fell from 784 lines to 284. Nothing the argument
depends on was moved out without being restated here.

**What the compression cost, and who pays it.** Four cases that were worked
through in v2 and v3 — the Balland abduction, the RATIRL streamer, the
person-as-hostage subset, and the dominance of short hand-over-now attacks — are
now only in the companion, and this paper cites it for each rather than
paraphrasing. A reader who wants the cases wants the companion.

**Citation.** The companion is cited throughout as `denial-spiral`. Its DOI is
inserted in this version; before it was deposited the entry carried a placeholder.

## Corrected

**"Feasible-but-slower" is replaced by "feasible-but-unfinished"** *(v3)*, in the
abstract and throughout. The old phrasing named a comparison of speeds the model
never makes and cannot make: by NNPP an undisclosed shortcut backup always *might*
exist, so nothing licenses calling $\mathcal{A}$'s path the slower one. The
condition that actually matters is stronger and is now stated as such — the
encounter leaves $\mathcal{A}$ a state *sufficient* for the spend authority but
does not complete the spend within the coercion budget. Deadly-race pivotality
turns on non-completion, not on relative pace.

**The spend authority is a set of states, not a private key** *(v3)*. The prose
had assumed throughout that the stash sits behind a single vanilla address,
conflating the thing $\mathcal{A}$ must reach with one secret. It is now
$\mathcal{K}$, a *set of states* in the same sense as the seizable set $\Sigma$,
and reaching $\mathcal{K}$ abbreviates reaching some element of it. Multisig is the
obvious case the old reading excluded: $\mathcal{K}$ is then every state holding
any $k$ of $n$ shares. Nothing in the argument needed the singleton, and two
places — the four-properties test and the hostage-token remark — depended on not
having assumed it.

**The hostage token needs a necessary *subset*, not a single necessary token**
*(v3)*. The argument assumed any one token from a setup of many would be
necessary, which fails for a sufficiently complex setup. The rigorous condition is
that burgling any subset of geographically distributed tokens that is *necessary*
suffices to present a hostage surface. The corollary tying no-hostage to
devicelessness is unaffected and is now stated as a corollary.

## Added and strengthened

**A vendor documents the naive tier in its own words** *(v3)*. The decoy's duress
framing had been the community's rather than any manufacturer's. One vendor makes
the claim itself: Sparrow's FAQ documents a data-directory flag and adds that the
feature "allows you to store all Sparrow data on removable media making for more
plausible deniability."

The feature does not guard the asset, and the vendor's own best-practice page is
why: it has the seed words backed up separately from the device, "ideally in a
different location," so the concealed directory is neither necessary nor
sufficient for $\mathcal{K}$. A Kerckhoffs attacker coerces the seed backup, loads
it into a wallet of his own, and never touches the concealed medium. What is left
for the medium to do is carry the holder's belief that, having surrendered what was
found, they may now say there is nothing more — a guarantee contingent on the
attacker's ignorance of a *documented* feature, which is the naive tier exactly.
The decoy at least stands between the attacker and the coins; this stands nowhere
near them. The continuation is the one the registry records: the truthful denier is
brutalized alongside the lying one, and the feature adds nothing but the confidence
to make the denial.

**The second mechanism has a name** *(v4)*. The chain running from a norm of
concealment, through attacker disbelief, to further coercion is now the **Denial
Spiral**, and is derived in the companion. It is the Obscurity Paradox run in
reverse, and it prices an encounter's *duration* where the Deadly Race prices its
*terminal move*. A corollary establishes that whether a design depletes the denial
commons is equivalent to its failing non-obscurity, so the Spiral is not a fifth
property and adds no column.

**A fourth censoring mechanism, which survives publication** *(v4)*. Three
mechanisms remove the *evidence*: the exposure covariate is unmeasurable because
obscurity does not advertise itself, the numerator is misclassified because a
robbery whose victim is killed is recorded as a homicide, and the residue is held
by bereaved families with no reason to speak — the third foreclosing the route by
which the first two might have been worked around, since the family was not told
either. The fourth removes the *response*: conceding is privately costly to whoever
concedes while recalcitrance externalizes the cost, which is a commons problem one
level up with the field's own capacity to self-correct as the depleted resource.
Publishing the first three can fix them; publishing the fourth does not, which is
why it is stated separately. The Semmelweis case is cited as the standing
illustration.

**The claim's epistemic status is stated, and the method named** *(v4)*. The
results are *derived*, not measured, and the paper now says why no observation
could settle them: every witness to an enacted case has an interest in the answer,
so the instrument that would test the model is disabled by the mechanism the model
describes. The posture is praxeological — deduction from purposive action, with
history illustrating rather than verifying — and the divergence is stated too,
since $p_A$ is a case probability and Mises denied that numbers belong there.
Mises, Semmelweis and a history of childbed fever are added to the bibliography.

**The design comparison gains a DR-safe column** *(v4)*. The table asks the
criterion directly — can a single encounter leave a state sufficient for
$\mathcal{K}$ without completing the spend — and the answer is not derivable from
the other four properties, which is why the column is there. Rewind forfeits two
properties and is DR-safe nonetheless, clearing by the remote-delegate route, while
BitVault forfeits them and is not. The self-destruct row is the instructive one: it
is **DR-safe and condemned anyway**, because an erasure destroys a path and names
no second racer, so the Lemma does not reach it and the design fails
non-obscurity instead. A no-hostage column is *not* added, being equivalent to
knowledge-based authentication by the corollary above, and neither is a Denial
Spiral column, being equivalent to non-obscurity.

**Keywords** gain *Denial Spiral* and *praxeology* *(v4)*.

## Provenance

**Two Sparrow pages are archived on both layers** *(v3)*, matching the practice v2
established: an independent archive.today capture recorded in the bibliography
entry, and a local snapshot under `sources/web/` covered by the manifest of URLs,
fetch times and SHA-256 digests. Both captures are dated 6 September 2026, later
than the 3 September sweep, and `ARCHIVE-RECORD.md` notes the exception.

**The manifest timestamp is upgraded** *(v3)*. Adding the two snapshots changed
the manifest, so it was re-stamped and the attestation upgraded once confirmed;
it is now anchored in **Bitcoin block 965788**. The prior attestation, anchored in
block 965345, is retained beside it, since it attests the manifest as it stood on
that earlier date and the new stamp does not.

**The registry pin is unchanged** at commit `9a4a62a`. The coding script and its
tables now live with the companion; this paper cites them rather than carrying
them, and the companion's bibliography entry names the directory.

## Other

**Spelling is normalized to American throughout** *(v4)*. Ten British forms had
accumulated in this paper's sections and bibliography by v3 — among them
*authorisation*, *cancelling*, *realise*, *modelling* and *programme* — and the
companion inherited several of them at the split, so both papers were normalized
together. Two
instances are deliberately left as they stand: the Orwell epigraph reads "the few
cubic centimetres inside your skull" and the later callback quotes that phrase, and
changing the spelling inside a direct quotation would be misquotation rather than
normalization.

**The byline is corrected to v4** *(v4)*. It had read "Working paper, v2" since the
v2 release, so the deposits published as v3 and v4 both describe themselves as v2
on their title pages. Files in a published record cannot be edited without a
support request, so those two stay wrong; this corrects the number going forward.
See the note below.

**An editorial placeholder is removed** *(v4)*. The companion's bibliography entry
carried "DOI to be inserted", which the conference submission was printing to
reviewers as "dOI to be inserted" mid-sentence. It is replaced by the companion's
real DOI here, and withheld from the blind build.

**Two stale open items are deleted from the conclusion** *(v4)*. Both were already
discharged in the body — the explicit adversary game making the Criterion a
theorem, and the floor reduction — and §3 says so in terms. Only the richer utility
model, the hardness calibration and the residual-window bound remain open.

## A note on version labels

Two defects in the version record are worth stating plainly, because a reader
trying to cite a specific deposit will meet both.

The **title pages of v3 and v4 say "v2"**, for the reason given above. A citation
to "v2" of this paper is therefore ambiguous across three deposits, and only the
DOI disambiguates them. The table at the head of this document is the authoritative
mapping.

Zenodo's own **version field is unset on v3 and v4**. Where v1 and v2 carry "v1
(2026-08)" and "v2 (2026-09)", the two most recent deposits carry nothing, so
Zenodo distinguishes them only by date and order. Record metadata is editable at
any time, unlike files, so this is correctable in place and should be corrected.

## Relation to the conference submissions

Both papers have anonymized conference builds, and they share their arguments with
the Zenodo versions without being identical in content. Each is bound by a
twenty-page body limit that these versions are not; the Deadly Race submission
sits exactly at twenty and keeps its supporting material in appendices, which do
not count against the limit, while the companion's body is eighteen.

The blind builds withhold the author's name, the repository URLs, the project's
coined code names, and — added in this version — the Zenodo DOIs, whose landing
pages carry the author's name in the byline and would otherwise de-anonymize a
submission in one click rather than one query. The companion's *title* stays in
both anonymized bibliographies, because a citation without it is useless and the
deposit is public under that exact title; stripping the name and the DOI is what
the rule on obvious references asks for, not a guarantee against a determined
reviewer.

Where the two forms differ, these versions are the more complete statement.

## Attribution

The architectural description of BitVault is the company's; the classification
drawn from it is the author's, and is relative to this paper's threat model. Its
classification is unchanged from v2, and the two properties v2 left undetermined
are still undetermined, for the reasons v2 gave.
