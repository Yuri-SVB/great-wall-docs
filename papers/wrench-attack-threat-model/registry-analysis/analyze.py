#!/usr/bin/env python3
"""
Reproducible keyword coding of the jlopp/physical-bitcoin-attacks registry.

The registry records each incident only as (date, victim, location, headline);
it has no structured duration or outcome field. We therefore code the free-text
HEADLINE by keyword. Coding is coarse and categories overlap; results are
directional, not an epidemiological study. See README.md for caveats.

Usage:
    curl -sSL https://raw.githubusercontent.com/jlopp/physical-bitcoin-attacks/master/README.md -o registry.md
    python3 analyze.py registry.md
"""
import re
import sys
from collections import Counter

CATEGORIES = {
    "killed/murdered (lower bound)":
        r"kill|murder|\bdead\b|shot dead|\bbody\b|\bdies\b|fatal|beheaded|dismember",
    "kidnap/hostage/ransom (long-hold)":
        r"kidnap|abduct|hostage|held captive|held hostage|ransom",
    "armed robbery at gunpoint (short-hold)":
        r"gunpoint|at gunpoint|armed|robbed|robbery|mugg",
    "home invasion / break-in / raid":
        r"home invasion|break-?in|broke into|burglar|raid|stormed|invaded (his|her|their) home",
    "torture / physical violence":
        r"tortur|beaten|\bbeat\b|stabb|pistol.?whip|assault|mutilat|finger|iron|burn|hammer|drill",
    "ATM/BTM/machine (not holder coercion)":
        r"\bATM\b|\bBTM\b|machine|kiosk|vending",
}


def load(path):
    rows = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.startswith("|")]
    out = []
    for r in rows:
        if re.match(r"\|\s*:?-", r) or "Date" in r:
            continue  # header / separator
        cells = [c.strip() for c in r.strip("|").split("|")]
        if len(cells) >= 4:
            out.append(tuple(cells[:4]))  # (date, victim, location, headline)
    return out


def main(path):
    inc = load(path)
    n = len(inc)
    print(f"TOTAL incidents: {n}\n")

    yr = Counter()
    for d, *_ in inc:
        m = re.search(r"(19|20)\d\d", d)
        yr[m.group(0) if m else "?"] += 1
    print("Per-year:")
    for y in sorted(yr):
        print(f"  {y}: {yr[y]}")

    print("\nHeadline keyword coding (categories overlap; share of all incidents):")
    for label, pat in CATEGORIES.items():
        c = sum(1 for *_, h in inc if re.search(pat, h, re.I))
        print(f"  {c:4d}  {100*c/n:5.1f}%  {label}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
