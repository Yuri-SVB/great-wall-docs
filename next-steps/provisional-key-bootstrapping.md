# Next steps — Bootstrapping the consolidation window (the provisional-key paradox)

> Captured from design discussion. **Status: a first version is implemented**
> in the app's Setup mode — see [§Implemented](#implemented) below. The paradox
> itself is intrinsic to the protocol and is recorded here as a design
> consideration; the *form* the provisional key takes was an open UX/security
> choice, now shipped as a lock-and-key file + compact key (QR / managed
> password / own entropy). Ties to `great-wallet/ARCHITECTURE.md`
> §celestial-peace-nf-core (the "graduation" milestone) and
> `great-wallet/THREAT_MODEL.md` (the provisional key is transient attack
> surface, live only during consolidation).

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

**Revisit:** how the app should prompt for provisional-key creation at
generation and, crucially, for its destruction at graduation (the lifecycle
prompts are not yet wired to the `celestial-peace-nf-core` graduation signal).

## Implemented

The shipped form (app Setup mode, `app/lib/src/setup/`) is a **lock-and-key
split**: the bulky encrypted setup is a *file*; the only secret the user guards
is a compact *key*. Destroy the key and the file is unrecoverable — which is the
point.

### Cryptography
- **AES-256-GCM** (NIST SP 800-38D) authenticated encryption over the serialised
  setup (`SetupVault`: Stage-0 text, `N`/`m`, and per-stage `(o,p,q)` + one leaf
  coordinate — the cheap-decode shortcut that skips re-deriving Argon2).
- The AES key is derived by **Argon2id** (RFC 9106, "second recommended":
  64 MiB, t=3, p=4) over the provisional key + a random per-file salt. A random
  96-bit nonce per file. The envelope is JSON: magic, version, KDF params + salt,
  nonce, ciphertext, GCM tag. KDF params are bounded on load (anti-DoS). A wrong
  key and a corrupt file are indistinguishable (GCM auth) and fail opaquely.

### The key — three KISS forms, two sizes
One key, handled three ways: (1) app-generated → **byte-mode QR** (hand-coloured
onto paper, scanned back, never read); (2) app-generated → **hex, blind-copied**
into a password manager; (3) the user supplies their **own hex** (distrusting the
device RNG). All three are the same raw bytes fed to `Argon2id(key, salt)`.

- **128-bit** (16 bytes / 32 hex) rides a byte-mode QR **v1 (21×21)** at EC-L.
- Optional **256-bit "tin-foil"** (32 bytes / 64 hex) rides a QR **v2 (25×25)**.
- The length is the user's choice and is **never stored**; load accepts either.
  Raw bytes are read from the QR's byte segment, not decoded text, so arbitrary
  key bytes survive intact.

### Forensic-deletion discipline
The key is **never written as a durable digital artifact** by the app — not to a
file, not auto-saved. The paper QR is the air-gapped carrier; destroy it
(shred/burn) or colour in its blank cells at graduation. Clipboard copies warn
that the clipboard is not air-gapped. In memory the key is zeroed after use.

### Hand-fill templates
"Blank templates" exports the two key-independent skeletons (finders, timing,
dark module, the v2 alignment pattern, over a highlighted module grid) as
`128-bit-…` / `256-bit-provisional-key-qr-template.png`. The user prints one,
reveals the on-screen QR, and colours the data cells to match. EC-L tolerates
~2 stray mis-coloured cells.

### Scanning back
- **Mobile/macOS:** `mobile_scanner` (live camera).
- **Desktop (Linux/Windows), best-effort:** `flutter_webrtc` drives the camera
  and pure-Dart `zxing2` decodes grabbed frames; if the camera will not open the
  user falls back to typing/pasting the hex. The decoded key stays only in RAM.

### Keyboard
Setup-screen keys: **F** focus file path · **W** write/save · **O** open ·
**T** blank templates · **Alt+V** reveal/hide sensitive fields. In the Write
dialog: **Q** show QR (press again to switch 128↔256), **Alt+Q** copy the key
(blind), **I** enter your own key, **Esc** close. In the Open dialog: **Q** scan,
**Alt+Q** type the key (32 or 64 hex), **Esc** cancel.
