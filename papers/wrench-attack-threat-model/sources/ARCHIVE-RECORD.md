# Third-party captures of the cited web pages

Every web page cited by the manuscript has an independent archive.today capture,
made 2026-09-03 except where noted --- with two outstanding exceptions,
the Sparrow pages, recorded below. Each permalink is recorded in the `note` field
of its bibliography entry, so a reader of the paper reaches it without consulting
this file; the list is kept here as an index and to record what the captures do
and do not cover.

This is the layer the snapshots in `web/` could not supply. Those were fetched by
us, and so attest integrity only — that a byte string existed by a date. An
archive.today capture is an independent witness that the page served this content
at this URL, which is the claim a citation to a live vendor page actually needs.

| bib key | captured |
|---|---|
| `coindesk-coldcard` | `http://archive.today/2026.08.01-211808/` (pre-existing, 2026-08-01) |
| `trezor-wipe-deniability` | `http://archive.today/2026.09.03-164059/` |
| `jade-duress-pin` | `http://archive.today/2026.09.03-164731/` |
| `jade-erase-pin` | `http://archive.today/2026.09.03-164738/` |
| `coldcard-trick-pins` | `http://archive.today/2026.09.03-164807/` |
| `trezor-wipe-code` | `http://archive.today/2026.09.03-164822/` |
| `jade-passphrase` | `http://archive.today/2026.09.03-164822/` |
| `casa` | `http://archive.today/2026.09.03-165338/` |
| `rewind-bitcoin` | `http://archive.today/2026.09.03-170016/` |
| `tlt-servicios` | `http://archive.today/2026.09.03-170027/` |
| `bsg-passphrase` | `http://archive.today/2026.09.03-170047/` |
| `certik-intel3d-h1-2026` | `http://archive.today/2026.09.03-170208/` |
| `certik-skynet-2026` | `http://archive.today/2026.09.03-171000/` |
| `coinkite-entropy` | `http://archive.today/2026.09.03-171027/` |
| `block-coldcard-postmortem` | `http://archive.today/2026.08.06-112407/` (pre-existing, 2026-08-06) |
| `balland` | `http://archive.today/2026.09.03-171044/` |
| `fisc-leak-2026` | `http://archive.today/2026.01.09-094000/` (pre-existing, 2026-01-09) |
| `ong-autocustodia` | `http://archive.today/2026.09.03-171910/` |
| `sparrow-faq` | **not yet captured** --- see below |
| `sparrow-best-practices` | **not yet captured** --- see below |

Each permalink continues with the captured URL, which is the cited URL except in
the three cases below. The full strings are in `references.bib`.

## The outstanding capture

`sparrow-faq` and `sparrow-best-practices` were added on 2026-09-06, when
archive.today was unreachable from the environment the fetches were made in (the connection was reset before any request
completed). The local snapshot, its SHA-256 and the manifest attestation are in
place; the independent-witness layer is not. Until a capture is made, each citation
rests on our own snapshot alone --- which attests that these bytes existed by this
date, but not that Sparrow served them at that URL. Each carries a single documented sentence, quoted in full in the bibliography entry
and in S5, so a reader can check it against the live page for as long as it stands
unrevised; that is weaker than the other rows here and is flagged rather than
smoothed over.

## Where the captured URL is not the cited URL

- `jade-duress-pin` and `jade-erase-pin` were cited by Blockstream's retired
  Zendesk-style paths (`/hc/en-us/articles/<id>-<slug>`), which HTTP 301 to
  `/blockstream-jade/<category>/<slug>`. The captures are of the redirect targets.
  The bibliography now cites the canonical paths, which is what `jade-passphrase`
  already did, and which survives the eventual removal of the redirect.
- `coinkite-entropy` redirects to a trailing slash; the citation now carries it.

Confirmed by following each cited URL and reading the effective URL back, not by
assuming the archives matched.

## What the earlier snapshots still add

`web/` is not superseded. It holds the page bodies as text, so a later revision
can be *diffed* rather than merely detected, and `MANIFEST.txt.ots` binds the whole
set into the Bitcoin timechain, which depends on no service's continued existence.
archive.today is a single point of failure; the pairing is deliberate.

Two pages have a capture but no local snapshot, both because the site refused
automated retrieval from the build environment: `coindesk-coldcard` (HTTP 429) and
`trezor-wipe-deniability` (HTTP 403). For those the archive is the only record.

## The cited video

`ong-autocustodia` is a livestream, and a capture of the page is not a capture of
the video. The recording is ~94 MB even at 144p, too large to belong in a
repository whose value is that it is cheap to clone, so it is held offline
instead. `video-X_cCwJubekQ.sha256` records the digests of two downloads and
`video-X_cCwJubekQ.sha256.ots` timestamps that record, which puts the digests in
the Bitcoin timechain without putting the file in git. That attestation is
anchored in **Bitcoin block 965356**. As with the other stamps here, `ots verify`
needs a Bitcoin node; `ots info` shows the attestation without one.

Read what this proves narrowly. The downloads were made through a third-party
service, so each is a re-encode rather than the bytes YouTube serves; a digest
identifies *that* download and has no canonical relation to the original. The
digests were supplied by the author who performed the download — the files were
never in the build environment. Provenance for the cited page rests on the
archive.today capture above, not on these hashes; what they add is that a copy
produced later can be matched against a record fixed at a known date.

## Not covered here, and why

- `lopp-attacks` / `ratirl` — pinned at commit `9a4a62a`, with the snapshot the
  paper's figures depend on under `registry-analysis/`, hashed and timestamped.
- `coldcard-pin-entry` — pinned at commit `7fc656a`.
- `bitvault`, `bssl` — captured earlier; `bssl` also carries a Bitcoin-anchored
  OpenTimestamps attestation over the PDF itself.
- `gw-*` — our own repository; pin by commit rather than archive.

A commit pin beats a capture wherever a source lives in git: anyone can verify it
against upstream without trusting either a copy of ours or an archive service.

Note that the registry snapshot under `registry-analysis/` contains several
hundred archive.is links of its own. Those are Lopp's citations, not ours, and
must not be rewritten: the file's SHA-256 and its timestamp commit to those exact
bytes.
