# Changes in v5

Zenodo concept DOI resolves to this version; each earlier version remains citable
at its own DOI.

| Version | DOI | Published |
|---|---|---|
| v1 | `10.5281/zenodo.22018892` | 19 August 2026 |
| v2 | `10.5281/zenodo.22287553` | 3 September 2026 |
| v3 | `10.5281/zenodo.22549552` | 6 September 2026 |
| v4 | `10.5281/zenodo.22778256` | 15 September 2026 |

Baseline for the comparison below is v4. One kind of change: the adversary gains
a belief coordinate that was previously implicit, and one conjecture is admitted
under it. No result changes, no classification moves, and no number is touched.

## The adversary's belief was a buried stipulation; it is now a coordinate

Through v4 the model carried a single sentence doing load-bearing work. After
NNPP, a `\noindent` paragraph said the attacker is *uniformly distrusting* —
that he "always defaults to assuming that whatever NNPP posits might exist does
in fact exist" — and justified it by ruling out the one alternative on offer, a
gullible attacker who believes the victim.

That paragraph conflated two different objects, and a reviewer who noticed would
have been right to say the paper assumes its conclusion.

**NNPP is an epistemic impossibility.** It binds every attacker: no disclosure
settles a negative existential, whatever either party would prefer. Nothing
about behaviour follows from it.

**Uniform distrust is a behavioural stipulation** laid on top of NNPP. It is a
modelling choice. It happens to be the right one, for the reason v4 gave, but
the reason has to be given rather than folded into the principle.

v5 states NNPP without the behavioural clause and gives the choice its own
definition, with two named regimes that are **orthogonal to the `[W,c,b,t]`
rungs** — either regime composes with any rung:

| | Posterior on "an undisclosed resumable copy remains" | Role |
|---|---|---|
| **dogmatic**, `WDY^dog` | pinned at 1, unconditionally | the *a fortiori* instrument; every bar in this paper is proved against it |
| **Bayesian**, `WDY^Bay` | carries a prior, updates on the encounter, never reaches 0 | duration and the shape of real encounters — the companion's register |

The object `WDY^dog` always posits is named: the **cornucopia**, a residual
stash of no bounded size that the holder can always be squeezed for once more.
Its own absurdity states it best — the holder may surrender the
twenty-one-millionth coin and still be asked where the rest is. It is coherent
exactly *because* NNPP holds: no evidence could refute the posit.

`WDY^Bay` is what updates. Fluent initial input to a time-gated derivation is
evidence that the bulk is operationally unreachable, and the posterior moves on
it; the attacker then chooses among release, continued coercion and the terminal
move by expected utility. By NNPP it never reaches certainty of release.

### Why the dogmatic regime needs `t`, which v4 never said

`WDY^dog` with an unbounded coercion window **decides nothing**. The cornucopia
is by construction still out there, so release forfeits it and the terminal move
closes the only channel to it. Such an attacker neither releases nor kills; the
encounter simply runs.

The budget `t` is what makes the regime decidable, and this is the substantive
reason `t` is pinned at `t_reg` rather than sent to infinity. v4 gave only the
formal reason (unbounded coercion walks any time-gate to completion, the same
category error as `b → ∞`). Read `WDY^dog[W,c,b,t]` as: *interrogate for `t`; if
a gray outcome stands open when `t` expires, enact the terminal move iff
(1−p_A)W > c.* The belief is frozen; the decision is still priced.

Stated as the instrument it is: **if a setup admits no gray outcome against
`WDY^dog` with W → ∞ and c → 0, it admits none against any attacker at all.**

`rem:worstcase` now names the regime in the worst-case identity, which previously
read as if plain WDY were fixed by the payoff coordinates alone.

## A second belief, also resolved conservatively: the undemonstrated delegate

`rem:nodelegate` joins the belief apparatus, right after the regimes. By NNPP
the attacker can no more rule out an access-dominating delegate than an
undisclosed copy, and the model does not have him price that probability:
**unless dominance has been *demonstrated* to him, he proceeds as though there
is none.**

It belongs here and not in the conjecture that first needed it, because the
reach of the argument is wider than the conjecture. Pinning that probability at
zero maximizes the attacker's assessed pivotality, and so the assessed payoff of
*every* move the Lemma prices — the terminal move and detention alike. The bar
at stake is DR-safety, not the safety of any one substitute move. A design that
clears the Criterion against an attacker who believes himself unopposed clears
it against one who suspects a delegate.

It also pays for itself where it sits: **it is why R2 turns on demonstration
rather than on existence.** A delegate who merely exists leaves the assessed
pivotality untouched and the holder exactly as pivotal as before. What clears
the Criterion is dominance the attacker can *check* (`rem:verifiable-dominance`),
which is what moves the belief. `def:gray`'s "gray but safe" is that case and
only that case. Stated this way the simplification supports R2 instead of
sitting in tension with it.

The field agrees: abductions happen, so real attackers proceed. Custody with no
remote party able to lock its owner out has plain advantages over custody with
one, many holders choose it for that reason, under Kerckhoffs the attacker knows
both, and where subjugation is fast a delegate may not learn of the encounter in
time to intervene.

## A conjecture: custody as the cheaper substitute

§3.3 gains `rem:scheherazade`, fenced on both sides — a lead-in saying it does
not follow from the Lemma and that nothing later rests on it, "conjecture" in
the remark's own title, and a closing sentence recording that there is no
empirical evidence of any particular instance.

A `WDY^Bay` attacker satisfied that he holds everything may still not release,
because a released holder with a feasible path is a competitor: detention buys
the same assurance as the terminal move at a fraction of the judicial
disutility. A gray outcome therefore prices not only the holder's elimination
but **custody, as collateral on his own abstention** — and the conjecture is
that the holder, having run the same arithmetic, volunteers for it.

**What is traded is non-racing, and the remark says so explicitly**, because
the captivity makes two different things possible and they are easy to run
together. More hours of coercion may extract more than a released holder would
ever have surrendered — real, but there the two parties want opposite things and
the holder volunteers for nothing. That is the Spiral's duration mechanism and
belongs to the companion. The bargain is the other case, the only one in which
the interests *align*: the holder keeps his life, and the attacker collects the
same win probability the terminal move would have bought him — a holder in
custody is a holder not racing — at a judicial disutility below `c`. Nothing is
disclosed to buy it; what the holder supplies is being held.

Three things are then said in the same breath, because the misreading is
available and costly:

- **It does buy a reprieve, and the paper now says so.** Nothing obliges the
  attacker to rent: he holds only where his own arithmetic says so. Where he
  does, the holder is alive who would otherwise be dead. Claiming otherwise was
  an overclaim, and an overclaim is what a reviewer pulls on. What is true is
  that the reprieve is **bounded** — at most `c/κ`, priced in the attacker's
  parameters, ended by the terminal move unless his own path completes first,
  and not the holder's to extend.
- **The concession is the charge, not a defense.** The killing being postponed
  is one the gray band created. A design clearing the Criterion leaves no racer
  to remove, hence no terminal move to be reprieved from, hence nothing for a
  kidnapping to substitute for. The misreading — that a gray outcome may save a
  life — gets the sign right and the baseline wrong. The band buys the holder at
  most `c/κ` and bills him a kidnapping for it.
- **The holder's willingness is not a free variable in the idealized model.**
  Under complete subjugation the attacker meets no resistance and enjoys full
  cooperation, so an abduction happens iff he chooses one. The volunteering is
  therefore not a mechanism of that model at all; it means something only as one
  moves toward the real encounter, where the attacker's assessment can be moved
  and the offer is information rather than consent. A second reason the bargain
  is the companion's subject.
- The alignment **expires**, and this is stated formally. Detention and the
  terminal move buy the attacker the *same* win probability, `p_A(R\{V})`, and
  differ only in price and tenure: **detention rents what the terminal move buys
  outright.** With `κ` the per-period cost of a hold, undiscounted, there are
  three pairwise comparisons and so two horizons — `πW/κ` against release and
  `T* = c/κ` against the terminal move — and the hold runs to whichever binds
  first. The Lemma's condition is exactly the switch between them: `πW > c` iff
  `T*` is the earlier. The bargain lives only in that half, since only there is
  there a killing for the holder to avert; in the other half the attacker may
  still detain, but on his own account. Where it does live, the holder buys a
  postponement of at most `c/κ`, set by the attacker's costs.
- The hold has **one** end that is not the terminal move: the attacker
  completing the spend, after which `π = 0` and release is free. It turns on his
  residual latency, not on anything the holder can do once held, and by NNPP
  release never becomes free on the evidence the holder supplies. (An earlier
  draft said "no natural end state", which is too strong, and said it in
  dogmatic-regime language inside a Bayesian section.)
- **The time-gate consequence was stated inverted and is fixed.** By `def:gray`
  a gray outcome requires the gate outstanding at release to exceed what is left
  of `t`; a gate the attacker can walk to completion inside the window leaves a
  clear success, `π = 0`, and nothing a hold could buy. The band that carries
  the consequence is `def:timegate`'s **weak** one — a remainder at release past
  what is left of `t` — where the attacker's own completion of the gate ends the
  race, after a delay the design has published under Kerckhoffs. He waits it out
  while `κ` times the remainder stays under `c`, and reverts to the terminal
  move past the same `T*`.

  **So neither band is a defense.** A longer gate does not buy safety; it buys a
  longer kidnapping and then a killing. What escapes both moves is a seized
  state that reaches nothing at all, `p_A = 0` — R1 and the tacit route — which
  is why `def:timegate` grades time-gating as a mechanism and not a strength.
  Note that the *first* repair of this paragraph was itself wrong in the same
  direction, calling "a residual beyond `t` that also exceeds `c/κ`" the
  defense; past `c/κ` is where the attacker kills, which is worse, not safer.

  The inverted form came from the project's working notes and is also in post
  006 in five languages. Both need the correction.

The bargain itself — the tale, what the analogy holds on, where it breaks — is
a `WDY^Bay` subject and is developed in the companion's §4 rather than here.

## One notation fix

`cor:disclosure` used `b` for the number of resumable copies the holder keeps,
colliding with the feasibility bound `b` of the priced adversary two pages
earlier. The copy count is now `m`, with `m̂` its lower-bound estimator, and the
corollary says explicitly that it is not the feasibility bound.

## On deposit

The conjecture is in the paper from this version on. Post 006 and its four
translations carry a fence saying it is "not in the paper, with no DOI behind
it" — true until this version is deposited and false the moment it is. That
fence is to be rewritten in the same week the deposit happens, not after.
