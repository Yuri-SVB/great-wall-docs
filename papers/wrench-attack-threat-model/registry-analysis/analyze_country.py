#!/usr/bin/env python3
"""
Country cut of the jlopp/physical-bitcoin-attacks registry.

Same coding as analyze.py -- the CATEGORIES regexes are imported from it rather
than restated, so the country numbers are directly comparable to the global
table in the manuscript. Adds two things analyze.py does not do:

  * a country-vs-global comparison of each category, so a modality skew is
    visible rather than having to be eyeballed across two runs;
  * a NEW axis, "who was coerced" -- holder vs. family member / associate.
    This one is not in the manuscript and is not comparable to anything
    published; it exists because it bears directly on the R2 (remote-delegate)
    route: if a large share of incidents reach the holder through someone close
    to them, then "remote" delegates who are spouses or relatives are inside the
    attacker's reach, and R2 is illusory for them.

Usage:
    curl -sSL https://raw.githubusercontent.com/jlopp/physical-bitcoin-attacks/master/README.md -o registry.md
    python3 analyze_country.py registry.md France
"""
import re
import sys
from collections import Counter, defaultdict

from analyze import CATEGORIES, load

# NEW axis -- not part of the manuscript's published coding.
PROXIMITY = {
    "family member / partner involved":
        r"\bwife\b|\bhusband\b|spouse|partner'?s|\bfamily\b|daughter|\bson\b|"
        r"mother|father|parents|\bchild|children|relative|girlfriend|boyfriend|"
        r"grandmother|grandfather|\bwidow\b",
    "associate / colleague / employee involved":
        r"associate|colleague|employee|co-?worker|business partner|co-?founder|"
        r"\bfriend\b|acquaintance|counterparty",
    # The sharp one: the person seized is NOT the holder, but a relative held to
    # reach them. This is the hostage-token mechanism of the manuscript's fifth
    # property, and it is what makes a spouse-or-relative "remote delegate"
    # (R2) illusory -- such a delegate is demonstrably within reach.
    #
    # !! THIS IS A SCREEN, NOT A CODING. It over-fires and every hit must be read
    # before it is counted. On the 2026-08-14 snapshot it surfaced 16 candidates
    # of which 4 were false positives -- most instructively an Osaka case where
    # "Son of <CEO>" named a PERPETRATOR, not a victim; elsewhere a relative who
    # merely called the police, a family robbed collectively with no proxy
    # structure, and a victim who turned out to hold the coins himself. The
    # audited figure was 12/352, not 16/352. Never quote the raw screen.
    "PROXY VICTIM -- relative seized to reach the holder":
        r"(father|mother|son|daughter|wife|husband|parents?|child(?:ren)?|family|relative)\s+of\s+"
        r"|\'s\s+(father|mother|son|daughter|wife|husband|parents?|child)"
        r"|extort\w*\s+.{0,40}from\s+(his|her|their)\s+\w+"
        r"|blackmail\s+.{0,30}(his|her|their)\s+\w+"
        r"|for\s+(his|her|their)\s+\w+\'s\s+(money|crypto|bitcoin)",
}

MONTHS = ("January February March April May June July August September October "
          "November December").split()


def year_of(d):
    m = re.search(r"(19|20)\d\d", d)
    return m.group(0) if m else "?"


def month_of(d):
    for i, name in enumerate(MONTHS, 1):
        if d.startswith(name):
            return i
    return None


def code(rows, pat):
    return sum(1 for *_, h in rows if re.search(pat, h, re.I))


def pct(a, b):
    return 100.0 * a / b if b else 0.0


def main(path, country):
    allrows = load(path)
    rows = [r for r in allrows if country.lower() in r[2].lower()]
    n, N = len(rows), len(allrows)
    if not n:
        sys.exit(f"no incidents matched location containing {country!r}")

    print(f"=== {country} cut of the registry ===")
    print(f"{n} of {N} incidents  ({pct(n, N):.1f}% of the global dataset)\n")

    # ---- trend, country vs global -------------------------------------------
    cy, gy = Counter(year_of(r[0]) for r in rows), Counter(year_of(r[0]) for r in allrows)
    print(f"{'year':6} {country[:12]:>12} {'global':>8} {'share':>7}")
    for y in sorted(gy):
        if y == "?":
            continue
        print(f"{y:6} {cy.get(y,0):>12} {gy[y]:>8} {pct(cy.get(y,0), gy[y]):>6.1f}%")

    # ---- monthly detail for the two live years ------------------------------
    live = [y for y in sorted(cy) if y.isdigit() and int(y) >= 2025]
    if live:
        print(f"\nmonthly, {country} ({'/'.join(live)}):")
        bym = defaultdict(Counter)
        for d, *_ in rows:
            y, m = year_of(d), month_of(d)
            if y in live and m:
                bym[y][m] += 1
        for y in live:
            line = " ".join(f"{bym[y].get(m,0):>2}" for m in range(1, 13))
            print(f"  {y}  {line}   (Jan..Dec, total {sum(bym[y].values())})")

    # ---- modality, country vs global ---------------------------------------
    print(f"\nheadline coding -- {country} vs global (categories overlap, do not sum to 100%)")
    print(f"{'':52} {country[:10]:>10} {'global':>10}   skew")
    for label, pat in CATEGORIES.items():
        c, g = code(rows, pat), code(allrows, pat)
        cp, gp = pct(c, n), pct(g, N)
        arrow = "  " if abs(cp - gp) < 3 else ("UP" if cp > gp else "DOWN")
        print(f"  {label:50} {cp:>9.1f}% {gp:>9.1f}%  {arrow} {cp-gp:+.1f}pp  (n={c})")

    # ---- proximity: who was reached ----------------------------------------
    print(f"\nwho was coerced -- NEW axis, not in the manuscript's published coding")
    for label, pat in PROXIMITY.items():
        c, g = code(rows, pat), code(allrows, pat)
        print(f"  {label:50} {pct(c,n):>9.1f}% {pct(g,N):>9.1f}%  (n={c})")
    proxy_pat = PROXIMITY["PROXY VICTIM -- relative seized to reach the holder"]
    proxy = [r for r in rows if re.search(proxy_pat, r[3], re.I)]
    if proxy:
        print(f"\n  the {len(proxy)} proxy-victim cases in {country} (audit them, then cite them):")
        for d, _v, _l, h in proxy:
            print(f"    {d[:20]:22} {h[:96]}")

    both = sum(1 for *_, h in rows
               if any(re.search(p, h, re.I) for p in PROXIMITY.values()))
    gboth = sum(1 for *_, h in allrows
                if any(re.search(p, h, re.I) for p in PROXIMITY.values()))
    print(f"  {'ANY third party named':50} {pct(both,n):>9.1f}% {pct(gboth,N):>9.1f}%  (n={both})")

    print("\nCaveats: coding is on the one-line headline only; categories overlap; the "
          "registry is a media/convenience sample, so deterred, unreported and privately "
          "settled cases are structurally absent, and coverage is English-biased. The "
          "fatality figure is a FLOOR, not an estimate. The proximity axis is coarse: a "
          "headline that does not name a relative is not evidence that none was involved.")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else "France")
