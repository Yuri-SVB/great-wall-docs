# The Discord server — rules and setup

Two parts. [House rules](#house-rules) is the text to pin in
`#welcome-start-here`, written to be read by a student. [Running it](#running-it)
is the operator's half: server settings, the reasoning behind each rule, and the
failure modes to watch.

The course runs live on Discord ([`../methodology.md`](../methodology.md)), so
the server is not a marketing channel that happens to exist. It is the
classroom, the office hours, and the feedback corpus.

---

## The problem the rules exist to solve

**A room full of people learning to protect their bitcoin is, viewed from
outside, a list of people who hold bitcoin.**

This is not a hypothetical. It is the exact mechanism both papers document: a
target list assembled out of records that nobody created for that purpose.
Breaches, tax databases, exchange data, social media — and now, a voluntary
sign-up sheet where the qualifying question is "do you care enough about
protecting your bitcoin to attend five sessions about it?"

The self-selection is sharper than a leaked database. A hacked exchange dump
tells an attacker someone once held. This tells them someone holds *now*, cares,
and is technical enough to be worth the effort.

Three consequences follow, and they shape every rule below.

1. **The membership list is the asset to protect, not the chat log.** Discord
   shows the member list to every member by default, and handles are frequently
   linkable to other servers, GitHub accounts and real names.
2. **The operator becomes a custodian.** If the server is compromised, or an
   account with elevated permissions is, the list leaks — and the person who
   published two papers about target lists will have assembled one. That is the
   reputational tail risk, and it is larger than the upside of any single
   cohort.
3. **Saying this out loud is the differentiator.** Every other Bitcoin Discord
   has rules about spam. Having rules about *not becoming a target list*, with
   the reasoning attached, demonstrates the thesis instead of asserting it. The
   rules are an argument.

---

## House rules

> Pin this in `#welcome-start-here`. Written for students; keep the reasoning
> sentence on rule 1, it does more work than the rule.

**Welcome. Before you post, six things.**

**1. Never post amounts, balances, addresses, or where you live.** Not yours,
not approximately, not as a joke, not in DMs. A room full of people learning to
protect their bitcoin is, from outside, a list of people who hold bitcoin — the
exact kind of list this course is about. Let's not build a better one. If a
question can only be answered by saying what you hold, it's the wrong question,
and I'll say so rather than answer it.

**2. Pseudonyms are welcome.** No real name is required, ever, by me or anyone
else. Nobody gets to ask, and "just curious" is asking.

**3. Screenshots: test setups only.** Post fractals freely in
`#show-your-fractal` — that channel exists because the images are genuinely
beautiful. But post from practice entropy, never from a region you intend to
use. Your region is part of your secret, and a screenshot of it is a screenshot
of part of your key.

**4. I will never DM you first.** Not to offer help, not about payment, not
about a cohort, not ever. Anyone who does is impersonating me. Screenshot it,
post it in `#q-and-a`, and I'll ban them. This will happen; it happens to every
Bitcoin server.

**5. No trading, no referrals, no "I can recover your wallet", no paid
"security consultants" recruiting in the channels.** Removal without discussion.

**6. Disagreement is the point.** Session 5 asks you to critique the system and
name what would stop you trusting it with real money. Do that in the channels
too. This is a pilot, and being told precisely where it's wrong is the most
valuable thing you can give it.

**On real funds:** the course uses test entropy only. Never a real seed, never
real money, not even to demonstrate. The implementation is a prototype.

---

## Running it

### Server settings that matter

| Setting | Value | Why |
|---|---|---|
| Invite link | **Never expire, unlimited uses** | Discord defaults to 7 days / 25 uses. A link on the website that silently dies is a funnel that stops working without telling you. |
| Verification level | **Medium** (verified email, registered >5 min) | Blocks throwaway spam accounts without demanding a phone number. Do not raise to High — phone verification excludes exactly the privacy-minded people this course is for. |
| DMs from server members | **Off**, server-wide | The single highest-value setting. It removes the impersonation and scam-DM vector structurally instead of by rule. |
| 2FA for moderators | **Required** | The membership list is the asset. Treat moderator accounts accordingly. |
| `#show-your-fractal` | Slowmode, and read the images | The one channel where a rule can be broken invisibly. See below. |
| Member list | Visible — and that is unavoidable | Discord gives no way to hide it from members. Say so in the rules rather than implying a privacy you cannot deliver. |

### What to actually watch

**Rule 3 is the one that gets broken by accident.** Someone posts a genuinely
lovely fractal that happens to be the region they just set up with. They will
not realise, and nobody else will either. Skim `#show-your-fractal` rather than
trusting the rule, and when you delete one, say why in the channel — publicly
and without naming anyone. Each catch teaches the rule better than the pin does.

**Price negotiation does not belong in a shared channel.** Cohort scheduling
does; what each person paid does not. In a room of 6–12 it surfaces fast, and
the person who paid more remembers it longer than the person who paid less. Fix
a public number per cohort, or move the conversation to DM — but not both
inconsistently.

**The archive is a feedback corpus and a liability at once.**
`methodology.md` treats the channels as material to mine between sessions,
which is right. It also means the server accumulates a searchable record of who
asked what about protecting their coins. Consider a retention policy before
cohort 2, not after.

### What not to do

- **No entry fee for the pilot.** A 6–12 seat cohort at $2 raises $24, so the
  fee cannot be revenue — it can only be a filter, and it is a weak one. Worse,
  it converts students into customers who are owed a finished course, at the
  exact moment the README asks them to accept version-0 drafts. Charge from
  cohort 2.
- **No mass-tagging `@everyone`** for anything but a session starting. The
  post-mortem on the first blog post applies here too: mass notification
  suppresses engagement and puts people under obligation.
- **No public member-count milestones.** "We just hit 100 members!" is an
  advertisement for the size of the list.
