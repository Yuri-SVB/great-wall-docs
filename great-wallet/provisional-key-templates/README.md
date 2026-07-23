# Provisional-key QR hand-fill templates

Printable **blank** skeletons for hand-colouring a provisional-key QR onto paper
— the air-gapped carrier described in
[`../../next-steps/provisional-key-bootstrapping.md`](../../next-steps/provisional-key-bootstrapping.md).

| File | Key size | QR | Modules |
|------|----------|----|---------|
| `128-bit-provisional-key-qr-template.png` | 128-bit (16 bytes) | v1 | 21×21 |
| `256-bit-provisional-key-qr-template.png` | 256-bit (32 bytes) | v2 | 25×25 |

Each shows only the **key-independent** structural cells — the three finder
patterns + separators, the two timing lines, the dark module, and (v2) the 5×5
alignment pattern — over a highlighted module grid, inside the spec-mandated
4-module quiet zone. Those cells are fixed by ISO/IEC 18004, so a printed
template matches whatever code the app shows on screen.

## Use
1. Print the template for your chosen key size (the app generates the same files
   beside your vault file via the **T** action in Setup mode).
2. In the app, **write** the setup (**W**) and reveal the QR (**Q**).
3. Colour the empty data cells solid black to match the on-screen code. The
   pre-inked black cells (finders/timing/alignment) are already correct.
4. Error-correction level **L** tolerates ~2 stray mis-coloured cells — work
   carefully, alone, with no cameras present.
5. Scan it back to load (**O** → **Q**). Destroy the paper at graduation
   (shred / burn).

## Provenance
The canonical generator is the app itself (`_QrPainter` blank view in
`app/lib/src/setup/setup_screen.dart`). These committed copies are reference
prints for users without a build; they are byte-for-byte reproducible from the
same structural rules and carry **no secret**.
