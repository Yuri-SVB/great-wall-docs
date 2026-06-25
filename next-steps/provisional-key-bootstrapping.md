# Next steps — Bootstrapping the consolidation window (the provisional-key paradox)

> Captured from design discussion. **Deferred / to-revisit:** the paradox itself
> is intrinsic to the protocol and is recorded here as a design consideration;
> the *form* the provisional key takes is an open UX/security choice, not yet
> built. Ties to `great-wallet/ARCHITECTURE.md` §celestial-peace-nf-core (the
> "graduation" milestone) and `great-wallet/THREAT_MODEL.md` (the provisional key
> is transient attack surface, live only during consolidation).

## The paradox
The protocol carries an inherent chicken-and-egg dependency at onboarding:

- to **secure** a stash with a setup, the user must already hold its entropy in
  tacit memory (stage-1 recall is what gates the vault TLP);
- to **memorize** that entropy, the user must train against the setup across the
  spaced-repetition consolidation window.

Neither side precedes the other cleanly. Logically, therefore, **at least one
provisional key must be kept externally** for the duration of the consolidation
window — from first generation until the `celestial-peace-nf-core` feature
signals **graduation** (memory consolidated; risk of loss-by-forgetting now
negligible).

## Self-standing after graduation
Once consolidated, the setup **stands on its own legs**: the setup's own entropy
supplies its own TLP gate (stage-1 recall unlocks the vault), so the protocol is
self-securing and the provisional key can — and should — be **destroyed**. The
provisional key is thus strictly *transient*: a bootstrap crutch that is live
only during consolidation, **not** a permanent backup. (Permanent
loss/incapacitation is covered separately by the inheritance protocol,
`phoenix-scroll`.)

## Candidate forms for the provisional key
The provisional key could be realized in various forms; each trades off the
desired properties differently:

1. **External password management.** Lowest effort; inherits the manager's own
   trust assumptions and deletion guarantees.
2. **Printed QR code on paper.** Held fully offline, then disposed of after
   graduation either by **physical destruction** (shredding/burning) or by
   **colouring in the white pixels** so the code is rendered uninformative.
   Cheap and air-gapped; deletion is physical and directly verifiable.
3. **External media (e.g. SD card).** Highly portable — easy to keep on one's
   person and **guard 24/7**; deletion relies on secure-erase discipline for the
   medium.

## Desired properties (selection criteria)
- **ease of guarding** — small and portable enough to keep in custody 24/7;
- **effective deletion** — provably/irreversibly destroyable once it has served;
- **low effort** — must not burden onboarding;
- **low cost.**

**Revisit:** which form(s) to recommend or ship as the default onboarding path,
and how the app should prompt for provisional-key creation at generation and,
crucially, for its destruction at graduation.
