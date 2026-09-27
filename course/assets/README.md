# Course assets (images & memes)

The slide decks reference images from this directory through an
`\IfFileExists` guard (the `\memeslot{...}` macro in
[`../slides/session1.tex`](../slides/session1.tex)). **If a file is missing, the
deck still compiles** and shows a labelled placeholder box where the image would
go. So you can build the slides today and drop in art later.

## Why images aren't committed yet

Memes and stock art carry licensing/attribution baggage, and the brief calls for
"artistic license, humor and memes." Rather than commit images of uncertain
provenance into the repo, this directory ships **empty** (except this guide).
The author drops in cleared art locally; the slide build picks it up
automatically. Keep anything you add license-clean (your own art, CC0, or
properly attributed) since this repo is dual-licensed and may go public.

## Slots referenced by Session 1

| Filename | Where | Suggested content |
|----------|-------|-------------------|
| `wrench-attack-meme.png` | "The headline that started this" | The classic *$5 wrench* gag — a cheap wrench beating any amount of crypto/encryption. (xkcd #538 is the archetype; use an original riff to stay license-clean.) |
| `skeptic-seat.png` | "The skeptic's seat" | A "but couldn't the attacker just…?" reaction image; playful, not mean. |
| `cake-eat-it.png` | "Have your cake and eat it" | A have-cake-and-eat-it visual; the joke is that the math *actually* allows it here. |

## Slots referenced by Sessions 2–5

| Filename | Session / slide | Suggested content |
|----------|-----------------|-------------------|
| `tacit-face.png` | S2 — thought experiment | "describe your friend's face so I can find them" — brain says *no*. |
| `fractal-zoom.png` | S3 — check-out | A deep `viewer.py` zoom — "there's a whole world down here." Real screenshot ideal. |
| `argon2-ram.png` | S4 — check-out | A RAM meter pinned at 100% — "it's not a bug, it's a wall." |
| `memory-palace.png` | S5 — the feel | Method of loci / memory palace — "your brain already does this." |

All of these are optional: the decks compile with labelled placeholders until the
art exists.

You can add more slots in any deck with:

```latex
\memeslot{my-image.png}{fallback caption shown if the file is absent}
```

## Conventions

- **Format:** PNG or JPG; landscape works best in the `\memeslot` box
  (it fits to `width=\linewidth, height=0.62\textheight, keepaspectratio`).
- **Naming:** lowercase, hyphenated, descriptive (`obscurity-vs-adoption.png`).
- **Resolution:** target ~1600px on the long edge — crisp on a projector without
  bloating the repo.
- **Brand fit:** the deck's accent is Great Wall green `#2F6F4E` and Bitcoin
  orange `#F7931A`; art that plays with those reads as part of the set.
- **Real fractal screenshots** are great here — capture them from `viewer.py`
  and they double as authentic teaching art (and a `#show-your-fractal` seed).

> If you decide to version cleared art, drop it straight into this folder and
> remove its row's "missing" placeholder will vanish on the next `make slides`.
