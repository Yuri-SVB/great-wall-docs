#!/usr/bin/env python3
"""
Reproducible keyword coding of the jlopp/physical-bitcoin-attacks registry.

The registry records each incident only as (date, victim, location, headline);
it has no structured duration or outcome field. We therefore code the free-text
HEADLINE by keyword. Coding is coarse and categories overlap; results are
directional, not an epidemiological study. See README.md for caveats.

Two things this script does that a naive grep over the table does not, and the
first of them changed a published figure:

  * It matches the headline PROSE only, never the markdown URLs beside it. A
    slug is not evidence: a non-fatal home invasion in a town called Killingly
    matched the fatality pattern through
    `.../police-2-rhode-island-women-charged-in-killingly-home-invasion`.
  * It screens for rows that may be the same incident entered twice, by looking
    for a shared source URL, and reports them rather than dropping them. Most
    shared URLs are one article covering a series of separate attacks on the
    same victim, which is not duplication.

The fatality row is a SCREEN, not a coding, and so is the duplicate list. The
pattern cannot tell a victim's death from an attacker shot by police or from a
plot that was only planned. Run with --review, read every hit, and quote the
audited count and never the screen. analyze_country.py's proximity axis carries
the same warning, and README.md records both audits.

Usage:
    curl -sSL https://raw.githubusercontent.com/jlopp/physical-bitcoin-attacks/master/README.md -o registry.md
    python3 analyze.py registry.md [--review] [--audit audit-9a4a62a.tsv]

--audit applies a hand audit of the screens, so the table it prints is the one
the manuscript quotes. The judgements live in the .tsv, one line each with its
evidence, because a regex cannot make them and a reader has to be able to
disagree with them one at a time.
"""
import re
import sys
from collections import Counter

CATEGORIES = {
    "killed/murdered (SCREEN — hand-audit before quoting)":
        r"kill|murder|\bdead\b|\bdeaths?\b|\bbody\b|\bdies\b|fatal|beheaded|dismember",
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

FATALITY = next(iter(CATEGORIES))
LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")


def prose(headline):
    """The headline's words, with the markdown URLs and the link label removed."""
    return LINK.sub(lambda m: m.group(1), headline).replace("(original link)", " ").strip()


def load(path):
    rows = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.startswith("|")]
    out = []
    for r in rows:
        if re.match(r"\|\s*:?-", r) or "Date" in r:
            continue  # header / separator
        cells = [c.strip() for c in r.strip("|").split("|")]
        if len(cells) < 4:
            continue
        date, victim, location, headline = cells[:4]
        out.append((date, victim, location, prose(headline),
                    {m.group(2) for m in LINK.finditer(headline)}))
    return out


def similarity(a, b):
    wa = set(re.findall(r"[a-z0-9]+", a.lower()))
    wb = set(re.findall(r"[a-z0-9]+", b.lower()))
    return len(wa & wb) / len(wa | wb) if wa | wb else 0.0


def duplicate_screen(inc, floor=0.5):
    """Pairs sharing a source URL, worded similarly enough to be worth reading."""
    out = []
    for i in range(len(inc)):
        for j in range(i + 1, len(inc)):
            if inc[i][4] and inc[i][4] & inc[j][4]:
                s = similarity(inc[i][3], inc[j][3])
                if s >= floor:
                    out.append((s, inc[i], inc[j]))
    return sorted(out, reverse=True, key=lambda t: t[0])


def load_audit(path):
    """verdict -> {(date, location): reason}, from the hand-audit .tsv."""
    out = {}
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        verdict, date, location, reason = line.split("\t", 3)
        out.setdefault(verdict, {})[(date, location)] = reason
    return out


def main(path, review=False, audit_path=None):
    inc = load(path)
    raw = len(inc)
    audit = load_audit(audit_path) if audit_path else {}

    dropped = audit.get("duplicate", {})
    if dropped:
        inc = [r for r in inc if (r[0], r[2]) not in dropped]
    n = len(inc)
    if audit:
        print(f"TOTAL incidents: {n}  (audited: {raw} rows less "
              f"{raw - n} duplicate(s), per {audit_path})\n")
    else:
        print(f"TOTAL rows: {raw}  (rows, not audited incidents — "
              "see the duplicate screen)\n")

    yr = Counter()
    for d, *_ in inc:
        m = re.search(r"(19|20)\d\d", d)
        yr[m.group(0) if m else "?"] += 1
    print("Per-year:")
    for y in sorted(yr):
        print(f"  {y}: {yr[y]}")

    denom = "incidents" if audit else "rows"
    print(f"\nHeadline keyword coding (prose only; categories overlap; "
          f"share of all {denom}):")
    for label, pat in CATEGORIES.items():
        hits = {(d, loc) for d, _, loc, h, _ in inc if re.search(pat, h, re.I)}
        if audit and label == FATALITY:
            hits -= set(audit.get("not-fatal", {}))
            hits |= {k for k in audit.get("fatal", {})
                     if k in {(d, loc) for d, _, loc, *_ in inc}}
            label = "killed/murdered (AUDITED — a floor; see README)"
        c = len(hits)
        print(f"  {c:4d}  {100*c/n:5.1f}%  {label}")

    if audit:
        print("\nAudit applied:")
        for verdict in ("duplicate", "not-fatal", "fatal"):
            for (d, loc), reason in audit.get(verdict, {}).items():
                print(f"  {verdict:10s} {d} · {loc}\n             {reason}")
        return

    dups = duplicate_screen(inc)
    print(f"\nDuplicate screen: {len(dups)} pair(s) share a source URL and wording."
          "\n  Most shared URLs are one article on a series of attacks, so read before cutting.")
    for s, a, b in dups:
        print(f"  {s:.2f}  {a[0]} · {a[2]}\n        {b[0]} · {b[2]}")

    if review:
        print("\nFatality screen — read every one of these before quoting a count:")
        for date, victim, location, h, _ in inc:
            if re.search(CATEGORIES[FATALITY], h, re.I):
                print(f"\n  {date} · {victim} · {location}\n    {h}")


if __name__ == "__main__":
    argv = sys.argv[1:]
    audit_path = None
    if "--audit" in argv:
        i = argv.index("--audit")
        if i + 1 >= len(argv):
            sys.exit(__doc__)
        audit_path = argv[i + 1]
        del argv[i:i + 2]
    a = [x for x in argv if x != "--review"]
    if len(a) != 1:
        sys.exit(__doc__)
    main(a[0], review="--review" in argv, audit_path=audit_path)
