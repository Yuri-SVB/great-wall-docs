# star-clock — design documents

**RSW time-lock puzzle library.** A pure cryptographic utility: modulus
generation, puzzle creation via the `phi(n)` fast path, sequential solving with
checkpointing, verification, serialization, and device speed calibration.

Status: in development. Depends on nothing else in the ecosystem; consumed by
`celestial-peace-nf-core`, `flying-turtle` and `mountain-dynasty`, which treat
puzzles as opaque payloads.

Its specification lives with the architecture rather than here, since the
component is small and its contract is defined by its consumers:

| Document | Covers |
|---|---|
| [`../great-wallet/ARCHITECTURE.md`](../great-wallet/ARCHITECTURE.md) §2 | Responsibilities, and why RSW rather than Argon2 for this role |
| [`../great-wallet/THREAT_MODEL.md`](../great-wallet/THREAT_MODEL.md) | RSA-2048 factoring hardness; AES-256-GCM for TLP ciphertext |

> [!NOTE]
> Formerly `tlp-core`. Renamed alongside `jade-clock` → `flying-turtle` and
> `phoenix-scroll` → `mountain-dynasty`.

Implementation: [github.com/Yuri-SVB/star-clock](https://github.com/Yuri-SVB/star-clock)

## ⚡ Support

Everything here is free software and free documents. Nothing is gated, no
release is delayed, and there is no paid edition.

If it was worth something to you, there is a Lightning (BOLT12) offer and an
on-chain silent payment address at
**[github.com/Yuri-SVB/SUPPORT](https://github.com/Yuri-SVB/SUPPORT)**,
alongside a dated log of what has actually shipped.
