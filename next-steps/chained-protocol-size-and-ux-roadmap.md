# Next steps — chained-protocol size range & UX roadmap

> Captured from design discussion during the one-point-per-stage protocol
> update. These are **deferred / to-revisit** items: the enabling code (all
> BIP39 sizes 32–256, hard cap at 256, one fixed Argon2 iteration count per
> setup) has shipped; the items below are intentionally not built yet. Each
> notes the decision it may revisit.

## 1. Beyond the 256-bit cap — "advanced pepper" chaining
The implementation hard-caps at 256 bits / 24 words / 8 stages
(`constants.MAX_ENTROPY_BITS`), because one more stage is the same marginal
mental effort for diminishing returns — the better lever past 24 words is more
between-stage Argon2 iterations, not more stages, and interfaces should advise
this. A user with a specific reason to exceed 256 bits could instead **manually
combine keys from multiple setups**. As of protocol `0.3.0` the **stage-0 text
field is exactly this pepper primitive**: set *pepper = the result of a previous
setup* (its master-secret export) and feed it in as stage-0 text, so setups
compose. **Revisit:** whether/when to lift the cap, and the exact pepper
semantics. (The Argon2id master-secret carry-over in §4 is the natural
primitive.)

## 2. Per-stage Argon2 iteration count — currently fixed (official)
**Official policy (now):** a *single* Argon2 iteration count is fixed at setup
and applied to **every** stage, to prevent parameter explosion. Interfaces
should encourage choosing it deliberately in advance. **Revisit:** allowing the
iteration count to vary per stage (e.g. heavier derivations deeper in the
chain). Kept fixed for now for simplicity and predictability.

## 3. Iteration UX — per-setup on-device calibration of N (OFFICIAL)
**Decision (official).** Calibrate the single iteration count `N` **per setup,
on the user's own device**, against a chosen **target wall-clock duration**: the
interface offers a few targets, micro-benchmarks a few Argon2 passes at the
selected memory profile, and solves for the `N` that hits the target. CLI keeps
a raw `--iterations` for the low-level reference path.

**Implemented and documented as reference.** The GUI ships this as an `Alt+D`
calibration dialog (worker-isolate benchmark = 1 warm-up + median of N timed
passes, cancellable, determinate progress bar + ETA; target presets; per-stage
vs all-stages scope; default ×2 safety margin behind an Advanced *"leave
unchanged if unsure"* expander; Apply writes the solved `N`; CLI keeps
`--iterations`). The full implemented detail now lives as reference docs in
[`great-wallet/ARCHITECTURE.md` → *Calibrating Argon2 duration → Implementation —
on-device calibration of `N`*](../great-wallet/ARCHITECTURE.md#calibrating-argon2-duration).
The rest of this section is the design rationale behind that feature.

**Framing — time is a perishable label on a durable parameter.** `N` (and `m`)
are exact and reproducible; "hours" is only a human label. Recovery reproduces
the digest from `N`, so hardware progress (esp. AI-driven memory-bandwidth
gains) changes only *how long a given `N` takes*, never correctness, entropy
security, or the OOM gate. The only thing that degrades is the absolute
coercion *delay*, and it does so gracefully and symmetrically (attacker and
defender speed up together for sequential, p=1 memory-hard work). On-device
setup calibration removes dev-time and cross-hardware staleness; only the true
setup→recovery temporal drift remains, and it is harmless to correctness.

**Memorizing N (and m) + graceful recovery.** `N` is the **user's
responsibility to memorize** (needed for hard recovery if the device/setup is
lost); so is the memory profile `m`. Two complementary mitigations:
1. **Stored, recognizable intermediates.** The protocol gracefully supports
   storing the sequence of intermediate derivation results, so an approximate
   memory of `N` suffices — the user *recognizes* the correct one (checkpoint
   trial-and-error). In this design `N` and `m` are the *only* inter-stage
   unknowns (the per-stage `o,p,q` are derived from them and the prior points),
   so this is the whole story today; §5 is the **same** recognition mechanism
   generalized to a larger parameter space, recovering any forgotten inter-stage
   parameter once the parameter set expands (not a separate mitigation).
2. **Celestial-Peace-Never-Forget (CPNF) training.** `celestial-peace-nf-core`
   should **also train explicit recall of `N` and `m`** (alongside the tacit
   point-recognition it already drills), so hard recovery is smooth. This is
   *safe*: unlike the point locations (which must stay tacit / recognition-only
   to remain coercion-resistant), `N` and `m` are derivation **parameters, not
   the secret** — an adversary who learns them still has no points. Asymmetry to
   respect: `m` must be recalled **exactly** (wrong profile → wrong Argon2 digest
   → every derived fractal breaks); `N` only **approximately** (mitigation 1
   closes the gap). See `great-wallet/ARCHITECTURE.md` §celestial-peace-nf-core.

**Conservative setting + TLP/jade-clock for per-session flexibility.** Manuals
and UX should induce users to pick the derivation time **conservatively (e.g.
2×)**, then rely on a **TLP / `jade-clock`** layer to freely adjust the
*effective per-session* delay — the RSW time-lock puzzle re-imposes a tunable
(and outsourceable) delay on top of the fixed `N`. See
`great-wallet/ARCHITECTURE.md` (tlp-core, jade-clock).

**Business angle — a technical problem begs a business solution.** The
unavoidable perishability of time-calibration *enhances the value of the
(paid) `jade-clock` feature*: because absolute delay drifts with hardware,
a marketplace that lets users re-impose and tune real per-session delay via
TLPs becomes more valuable over time, not less. Track this under
`justification-and-economics` / `great-wallet`.

## 4. Amendable setups — truncate early / extend later, with carry-over
The modular chain should let a setup's **number of stages** be amended after the
fact (the iteration count stays fixed, §2):
- **Truncate:** a user who started greedy (say aiming for 24 words) may, at the
  6th stage (18 words, i.e. partway), recalibrate cost/benefit and **stop
  there**, keeping the prefix as the final secret.
- **Extend:** the same user may later **upgrade** the setup and add a few more
  stages.

To support this elegantly, at *any* stage boundary the UI should be able to:
- **copy the words so far without displaying them** (clipboard only), and
- **copy the master-secret export** — `Argon2id` over the setup transcript so
  far (stage-0 text ‖ N ‖ per-stage params ‖ per-stage leaf-centre coordinates,
  up to the exporting stage) with **the exporting stage's own text label appended
  to the message** and a **fixed salt `b"greatwall"`** (same style as the
  inter-stage chain) — for a blind carry-over into another wallet or as the
  pepper of a downstream setup. Available at every non-0 stage and **not**
  contingent on completing later stages (see DESIGN.md → *Master-Secret Export*).

As of `0.3.0` this **replaces** the earlier `SHA512(words_so_far ++ user_salt)`
button: the salted SHA-512 digest is superseded by the Argon2id export, which
tolerates large peppers/outputs without entropy collapse. Generalize the export
to **every** stage boundary (today's default takes only the first 32 characters
of the 1024-byte output; full output behind advanced options is a TODO). This is
also the primitive behind the §1 pepper idea.

## 5. Forgotten inter-stage parameter — recover by recognizing the fractal
A large parameter space makes it unlikely that uniformly-distributed
pseudorandom fractals look similar by chance. That gives a practical recovery
path if a user forgets an inter-stage parameter: **store all candidate
sequential fractals and let the user recognize the correct one** — the vastness
of the space should make the right fractal easily identifiable. **Ties to** the
deferred parameter-family expansion in
`research-notes-substrate-hardness.md` (a bigger, well-decorrelated parameter
space both hardens the substrate and makes such recognition reliable).

## 6. Gamification — one more stage = a "level-up"
The modular, one-point-per-stage design naturally reads as a game where adding a
stage feels almost literally like leveling up. The UX effort should deliberately
**exploit that framing** (progression, "level up" per stage, etc.) to make
larger, stronger setups feel rewarding rather than burdensome.
