# great-wallet — design documents

**The application.** The Dart and Flutter desktop wallet that integrates the
libraries into one product, reaching Rust through FFI.

This directory also holds the documents that describe the ecosystem as a whole,
so `ARCHITECTURE.md` is the right starting point for any component.

| Document | Covers |
|---|---|
| [`OVERVIEW.md`](./OVERVIEW.md) | The four properties, and how the application is used |
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Every component, the dependency graph, the FFI surface |
| [`THREAT_MODEL.md`](./THREAT_MODEL.md) | Adversaries, assumptions, and what each primitive is relied on for |
| [`provisional-key-templates/`](./provisional-key-templates) | Provisional-key bootstrapping material |

Implementation: [github.com/Yuri-SVB/Great-Wallet](https://github.com/Yuri-SVB/Great-Wallet)

## Training modes

How many of a stage's nine maps to memorise is yours to choose: any `r_i` of
them rebuild the stage, and the rest are forgiveness. Three modes, by the maps
`t` memorised per stage:

| Mode | `t` | Extra maps: deep stage / shallow stage | Maturity in about | Effort, first year (moderate = 1) |
|---|---|---|---|---|
| chill | 4 | 1 / 2 | 5 weeks | 1.8 |
| moderate | 5 | 2 / 3 | 1 week | 1 |
| on fire | 6 | 3 / 4 | 1 week | 1.1 |

- **chill:** lighter sessions, but it drags on longer, so it costs more effort
  in all.
- **moderate:** the sweet spot: maturity in a reasonable time.
- **on fire:** a marginal gain at a considerable cost.
- **All three** are best coupled with inheritance (mountain-dynasty) as a backup.

The shallow stage gets one extra map more than a deep one: a deep stage's one
forgotten point is to be found by a 2³² search (minutes on a desktop), which
stage 0's memory-hard bundle rules out.

*Maturity* is a chance of forgetting below 0.001% over a week. These are
estimates from the model — SM-2 with its forgetting curve, lapses simulated, daily
sessions — and they count on parts not built yet (the Star Clock bundles, the
2³² search, credit for early reviews). They wait for real use to confirm or
correct them.

## ⚡ Support

Everything here is free software and free documents. Nothing is gated, no
release is delayed, and there is no paid edition.

If it was worth something to you, there is a Lightning (BOLT12) offer and an
on-chain silent payment address at
**[github.com/Yuri-SVB/SUPPORT](https://github.com/Yuri-SVB/SUPPORT)**,
alongside a dated log of what has actually shipped.
