# great-wall-ux — orbit-protocol redesign plan

> **Status: planning.** Companion to
> [`core-orbit-redesign-plan.md`](core-orbit-redesign-plan.md): what the Dart/Flutter
> UX layer must add to drive the canonical **orbit** protocol
> ([`coercion-resistant-orbit-protocol.md`](coercion-resistant-orbit-protocol.md)).
> The UX never duplicates engine math (per
> [`../great-wall-ux/SCOPE.md`](../great-wall-ux/SCOPE.md)); every derivation below is
> an FFI call into the `0.4.0` core. This doc plans **interaction, not cryptography**.

## 0. One-paragraph delta

Today the UX renders **one perturbed fractal per stage** and collects **one point**
(`Stage.stage2` + `StageParameters(o,p,q)` in `lib/src/stages/stage.dart`). The orbit
protocol makes a stage a **board of `s_i` fractals** on which the user places `s_i`
points, of which any `t_i` reconstruct the stage; it roots the whole setup in a
**Namtso date** instead of a text label; and it adds three lifecycle flows the current
UX has no surface for — **setup pathway / level-up**, **retirement (bury `o_i`)**, and
**forgiving TLP-deck review**. The sober, game-like principle and the "never display or
log coordinates" invariant carry over unchanged and, if anything, tighten.

## 1. Stage model: single-board → multi-board (`s_i` fractals)

- Generalise `Stage`/`StageParameters` from one `(o,p,q)` to an **ordered set of
  `s_i` boards**, board `j` parameterised by `theta_i_j` (an FFI `bs_theta(o_i, j)`
  result). The existing perturbed render path is reused per board; only the *count* and
  *navigation* change.
- **Board navigation** within a stage: the current `T`-cycles-stage interaction extends
  to a two-level cursor (stage → board). Sober audio cues already exist
  (`nav_stage.wav`, `change_point.wav`, `select_point.wav`) — add a board-level cue
  rather than overloading stage-level ones.
- **Point placement** per board is the current select-mode click + validation
  (`leaf_area_source.dart`, contraction rejection) — unchanged per board.

## 2. Shamir shares: primary vs forgetting-resistance

- The UX must express the **`t_i`-of-`s_i`** structure: `t_i` **primary** points
  (positive abscissae) are required; the optional `(s_i − t_i)` **forgetting-resistance**
  points (negative abscissae) are opt-in extra boards the user MAY memorise for recall
  insurance.
- Surface this as a per-stage **"required vs. safety-net"** distinction in the setup
  wizard — never expose Shamir shares or the polynomial as such (that would re-open the
  sub-threshold oracle the whole design forbids). The UX shows *boards to point at*, not
  algebra.
- Reuse `StageCountSlider` as the pattern for a **points-per-stage** control bounded by
  the canonical `(s_i, t_i)` tiers read over FFI (`bs_setup_tiers`) — the UX must not
  invent tier values.

## 3. Root: Namtso date input replaces the stage-0 text field

- Replace the `[A-Z0-9-]` stage-0 entropy field with a **date picker → `σ`** flow: the
  user enters a memorable date, the app calls Namtso `harvest(date) → σ`
  ([`namtso-app-and-api.md`](namtso-app-and-api.md)), and displays the **receipt**
  (block heights/hashes — non-secret) as reassurance. The date is treated like any
  stage-0 material: recalled, never written in the clear.
- The old text label survives only as an optional **pepper/export-label** affordance,
  clearly demoted from "your secret" to "a tag."
- **Local-first / cloaking:** prefer local-node or offline-headers harvest; if a remote
  source is used, apply Namtso date-cloaking (fetch a coarse interval) — the UX should
  default to the privacy-preserving path and only fall back with a visible notice.

## 4. New lifecycle flows

### 4.1 Setup pathway & level-up (spec §7)

- A **wizard** walks Setup 1 → 2 → 3 → 4 as progressive builds (each prefix valid).
  Support the **skip-to-Setup-2** option (memorise the first deep stage's third point up front,
  economise on the later rekey) and the standard **one-point-at-a-time level-up**.
- Every orbit change is a **rekey event**: the UX MUST prompt "this changes `K` — you
  must move funds for it to take effect," and MUST NOT present a level-up as free.
- Encourage the **≥ 2-deep memorised** target so an emergency retirement of the
  lowest (least-deep) in-use stage is seamless.

### 4.2 Retirement (bury `o_i`) 

- A guarded **"retire compromised level"** flow that publishes `o_i` on-chain (new de
  facto `σ`) and re-roots a fresh setup. Must state the cost plainly: a **permanent,
  privacy-revealing chain artifact** tied to the event — an emergency lever, not a
  routine button. Double-confirm; never trigger implicitly.

### 4.3 Forgiving TLP-deck review (spec §8, CPNF integration)

- Practice/review is delivered by the **TLP-gated deck**, not by exposing shares. The
  UX drives the [`celestial-peace-nf-core`](../next-steps/cpnf-lifecycle-and-deck.md)
  scheduler over an **enumerated sub-deck** honouring the §8 invariants: stage-0 points
  (or the three in-use shallow points) always included; include `o_i` when a payload
  holds all-but-≤1 of a stage; never let a sub-deck trigger a deadly-race; keep `K`
  `≥ 64*`.
- These invariants are **security-load-bearing** and belong in core/wallet enforcement;
  the UX renders the resulting deck and must **refuse to construct** a deck the layer
  below flags as invariant-violating rather than silently proceeding.

## 5. Invariants that tighten

- **No coordinate leaks, extended.** The `StageParameters(<redacted>)` and
  "no logs of `(o,p,q)`" rules now also cover `o_i`, `theta_i_j`, `Sh_i`, `p_i_j`, the
  Namtso date, and `K`. Add lints/tests mirroring `stage.dart`'s redacted `toString`.
- **Ephemeral-only orbit state.** `o_i` renders *every* board of a stage — so a live
  `o_i` is coercion-accelerating (spec §3). The UX holds orbit state in RAM only, wipes
  on stage advance / backgrounding / session end, and never persists it (the stored
  orbit stays TLP-gated at the wallet layer, never plaintext).
- **Rekey honesty.** No UI path may imply an orbit change took effect without the
  on-chain rekey.

## 6. Test & sequencing

1. Multi-board `Stage`/`StageParameters` model + `bs_theta` FFI binding + widget tests
   (board navigation, per-board validation) — no new crypto in Dart.
2. Namtso date→`σ` intake + receipt display + cloaking default.
3. Setup-pathway wizard (incl. skip-to-2) with rekey prompts; tier values from
   `bs_setup_tiers`.
4. Retirement flow (double-confirm, cost disclosure).
5. TLP-deck review surface wired to `celestial-peace-nf-core`, refusing invalid decks.
6. Redaction/ephemeral-wipe lints + tests across the new state.

Steps 1–2 unblock everything else; 3–5 can proceed in parallel once the multi-board
model lands. All engine math stays in `0.4.0` core — this layer only renders and
sequences.

## 7. Open items

- Exact board-navigation gesture/audio grammar for two-level (stage→board) cursors.
- How much of the §8 deck-invariant enforcement lives in wallet vs. is surfaced as UX
  affordances (recommend: enforce below, *render* above).
- Whether the demoted text label is worth keeping at all, or folded entirely into an
  "advanced pepper" screen.
