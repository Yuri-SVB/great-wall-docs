# Source of record

## `B-SSL_WP_Oct_11_2025.pdf`

The B-SSL concept whitepaper, as cited by the BitVault treatment in §5. Retrieved
2026-09-01 from

    https://raw.githubusercontent.com/ilghan/bssl-whitepaper/main/B-SSL_WP_Oct_11_2025.pdf

- **Size** 352,036 bytes
- **SHA-256** `64a0c9c4b440ae8ff90a7ba8ecb62bacef3acf153753b9240aee17c8723f5320`
- **Licence** Apache-2.0, per the repository it was published in.

The document is self-attributed to F. Madonna of BitVault SA and is published by a
GitHub account identifying itself with the BitVault organization. It is not linked
from the vendor's own site and the attribution could not be authenticated. It is
kept here as the object the paper analyses, not as an authoritative specification —
which, as §5 records, does not exist publicly.

## `B-SSL_WP_Oct_11_2025.pdf.ots`

An OpenTimestamps attestation over that file, created 2026-09-01.

Snapshot services cannot capture a PDF served through GitHub's blob viewer, so
archive.is preserves the repository page rather than the document. This does what
the snapshot could not: it binds the file's hash into the Bitcoin timechain, so the
claim *this document, in this form, existed on this date* is verifiable by anyone,
independently of GitHub, of archive.is, and of the vendor.

To verify:

    ots verify B-SSL_WP_Oct_11_2025.pdf.ots

Upgraded 2026-09-02 and now anchored in **Bitcoin block 965103** (merkle root
`b3a444da6e952ba00431ad67770ade15b70672c714571d0c35e9b37d4868e7ec`). Verification
requires a Bitcoin node; `ots info` shows the attestation without one.

## `web/` --- vendor and report pages

The classification of §5 and Appendix D rests in several places on what a vendor
*says* about its own product: Blockstream's duress- and wallet-erase-PIN articles,
Coldcard's settings documentation, Trezor's wipe-code guide, the service pages of
Casa, RewindBitcoin, Tus Llaves Tus BTC and the Bitcoin Security Guide, two
CertiK wrench-attack reports, and the vendor and press accounts of the Coldcard
entropy failure. None of those is version-controlled upstream. A page
can be revised, or withdrawn, without notice and without trace, and the citation
then no longer supports the sentence resting on it — the ordinary fate of a claim
about a live web page, and a sharper risk here, since §5 classifies some of these
products in ways their vendors would not choose.

`web/` holds each of the fifteen retrievable pages as fetched on 2026-09-03. `MANIFEST.txt` records, per
source, the bib key, URL, fetch time, HTTP status, byte count and SHA-256;
`MANIFEST.txt.ots` is an OpenTimestamps attestation over the manifest, and so, by
way of the hashes it contains, over the whole set at once; it is anchored in
**Bitcoin block 965345**.

To verify the set:

    cd web
    sha256sum -c <(awk '/^  sha256/{h=$2} /^  file/{print h"  "$2}' MANIFEST.txt)
    ots verify MANIFEST.txt.ots

**What this establishes, and what it does not.** These snapshots were fetched by
us, not by a third party. The timestamp proves that this set of bytes existed in
this form by the date it anchors — enough to detect a later silent revision, and
enough to let a reader see what we read. It does *not* attest that the vendor
served those bytes at that URL: for that, an independent witness is needed. Every
cited page now has one — an archive.today capture, indexed in `ARCHIVE-RECORD.md`
and carried in the bibliography entry itself. The two layers are kept because they
fail differently: an archive service can go dark, while a local snapshot plus a
Bitcoin-anchored hash depends on no service at all, and holds the page body as
text so a later revision can be diffed rather than merely detected.

Two further limits, stated so they are not mistaken for tampering:

- These are live, dynamic pages. Two retrievals minutes apart differ by a few
  dozen bytes in embedded tokens and build identifiers. The hash pins *this
  retrieval*, not a canonical state of the page; a mismatch on refetch is
  expected and is not by itself evidence of revision. Compare the prose.
- Two of the seventeen cited pages are recorded in the manifest as not
  retrieved. `trezor-wipe-deniability`
  (github.com/trezor/trezor-firmware/issues/2055) returned HTTP 403, as GitHub
  blob and issue URLs do from this environment; GitHub retains an edit history
  for issue bodies, which partly covers the gap. `coindesk-coldcard` returned
  HTTP 429 through repeated retries with backoff, the site declining automated
  retrieval. For those two the archive.today capture is the only record.

Sources cited from a git repository are pinned by commit in the bibliography
instead, which is stronger than a snapshot: anyone can verify the pin against
upstream without trusting a copy of ours. That covers `coldcard-pin-entry`
(`7fc656a`) and the attack registry (`9a4a62a`, snapshotted under
`registry-analysis/` because the paper's own figures depend on it).
