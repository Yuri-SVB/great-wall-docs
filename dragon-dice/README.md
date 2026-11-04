# dragon-dice — design documents

**Entropy from real dice that anyone can audit.** Rolls of physical dice
become a canonical JSON whose SHA-512 is the secret; a Bayesian estimate
says how much entropy they carry if the dice may be biased.

Status: in development. Depends on nothing else in the ecosystem.

| Document | Covers |
|---|---|
| [`../great-wallet/ARCHITECTURE.md`](../great-wallet/ARCHITECTURE.md) §9 | Role and design |
| The repository's `doc/FORMAT.md` | The rolls format (`dragon-dice/1`), its canonical form and vectors |
| The repository's `doc/ADVANCED.md` | Advanced mode: prior, entropy measure, bound, custom dice, how many rolls |

Implementation: [github.com/Yuri-SVB/dragon-dice](https://github.com/Yuri-SVB/dragon-dice)
