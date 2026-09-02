# Build the Deadly Race manuscript.
#   make            -> main.pdf (full run with bibliography)
#   make pages      -> report the body page count against the FC'27 limit
#   make anon-check -> fail if the blind build leaks identifying strings
#   make submission -> build, then run both checks (do this before uploading)
#   make clean      -> remove build artifacts
#
# Target venue: Financial Cryptography and Data Security (FC) 2027, SoK track:
# 20 pages in standard LNCS format, EXCLUDING references and appendices.
# `make pages` reports the count that the limit applies to.

MAIN = main
SECTIONS = $(wildcard sections/*.tex)
LIMIT = 20

$(MAIN).pdf: $(MAIN).tex $(SECTIONS) references.bib references-anon.bib splncs04-unsrt.bst
	pdflatex -interaction=nonstopmode $(MAIN).tex
	bibtex   $(MAIN)
	pdflatex -interaction=nonstopmode $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex

# Anonymized bibliography for the blind-review build, generated from the single
# source so the two cannot drift. Three kinds of de-anonymizing content: the
# author's name, his GitHub URLs, and the project's coined code names. The
# names matter as much as the URLs -- "Flying Turtle" and "Namtso" are unique
# search strings, so withholding the URL while keeping the name still hands a
# curious reviewer the author in one query. Each is replaced by the plain
# description it was a label for, which is all the citation needs to be useful.
references-anon.bib: references.bib
	sed -e 's/{da Silva Villas Boas, Yuri}/{Anonymous author}/g' \
	    -e 's#\\url{https://github\.com/Yuri-SVB/[^}]*}#[URL withheld for review]#g' \
	    -e 's/Burning Ship Encoder --- Design Document/Fractal Encoder --- Design Document/' \
	    -e 's/Flying Turtle --- Outsourced Anonymous Timelock/An Outsourced Anonymous Timelock/' \
	    -e 's/(Flying Turtle module)/(outsourced-timelock module)/' \
	    -e 's/Companion paper (Namtso),/Companion paper,/' \
	    references.bib > $@

.PHONY: anon-bib
anon-bib: references-anon.bib

# splncs04 numbers references alphabetically by author. Springer's LNCS
# instructions allow either that or numbering in order of citation; we take the
# latter, so a reader meets [1] first. The only change is deleting the two lines
# that sort the entry list before they are numbered -- entry formatting is
# untouched, so the bibliography still looks exactly like LNCS. Derived rather
# than hand-copied so it cannot drift from the installed splncs04.
splncs04-unsrt.bst:
	sed -e '/^ITERATE {presort}$$/d' -e '/^SORT$$/d' \
	    "$$(kpsewhich splncs04.bst)" > $@

.PHONY: unsrt-bst
unsrt-bst: splncs04-unsrt.bst

.PHONY: pages
pages: $(MAIN).pdf
	@body=$$(sed -n 's/.*newlabel{page:lastbody}{{[^}]*}{\([0-9]*\)}.*/\1/p' $(MAIN).aux); \
	total=$$(sed -n 's/.*Output written on .*(\([0-9]*\) pages.*/\1/p' $(MAIN).log | tail -1); \
	over=$$((body - $(LIMIT))); \
	echo "--------------------------------------------------"; \
	echo " body (counts against the limit) : $$body pp"; \
	echo " FC'27 SoK-track limit           : $(LIMIT) pp"; \
	if [ $$over -gt 0 ]; then echo " OVER BY                         : $$over pp"; \
	else echo " under by                        : $$((-over)) pp"; fi; \
	echo " references + appendices (free)  : $$((total - body)) pp"; \
	echo " total PDF                       : $$total pp"; \
	echo "--------------------------------------------------"

# Deny-list check on the built PDF. FC'27 desk-rejects a submission that is not
# properly anonymized, and the failure mode is silent -- nothing in a LaTeX run
# complains about a leaked name. This turns that into a build error.
#
# The text is stripped of whitespace and hyphens before matching, because
# pdftotext breaks words at arbitrary points ("physi\ncal", "Burning-Ship") and
# a deny-list matched against the raw layout misses exactly the leaks that
# happen to land at a line end. Patterns are therefore written closed-up.
#
# Two entries are deliberately narrow. `burningshipencoder' rather than
# `burningship': the Burning Ship fractal is public mathematics and the paper
# names it legitimately; only the coined *product* title identifies the author.
# `jadeclock' rather than `jade': Blockstream Jade is a third-party wallet the
# paper cites a dozen times.
#
# One trap when extending this list: pdftotext silently drops fi/ff/fl
# ligatures ("firmware" extracts as "rmware"), so a pattern spanning one can
# never match. No entry below contains one -- note that the turtle is matched
# by `turtle', not `flyingturtle', for exactly this reason -- and any pattern
# added later must be checked against the same hazard.
#
# The check also sweeps every *other* PDF in this directory. A superseded
# non-anonymous build sitting beside main.pdf, under a similar name, is one
# misclick away from being the file that gets uploaded -- which is why the v1
# manuscript now lives in papers/archive/ instead of here.
DENY_RE = yuri|villasboas|pm\.me|namtso|turtle|jadeclock|phoenixscroll|mountaindynasty|greatwall|burningshipencoder|celestialpeace

.PHONY: anon-check
anon-check: $(MAIN).pdf
	@grep -qxF '\anontrue' $(MAIN).tex || { \
	    echo "anon-check: main.tex is in non-blind mode -- skipped."; exit 0; }; \
	command -v pdftotext >/dev/null 2>&1 || { \
	    echo "anon-check: pdftotext not installed -- cannot verify"; exit 1; }; \
	fail=0; \
	hits=$$(pdftotext $(MAIN).pdf - | tr -d '[:space:]-' \
	        | grep -o -i -E '$(DENY_RE)' | sort | uniq -c); \
	if [ -n "$$hits" ]; then \
	    echo "anon-check: FAIL -- de-anonymizing strings in the text of $(MAIN).pdf:"; \
	    echo "$$hits"; fail=1; \
	fi; \
	meta=$$(pdfinfo $(MAIN).pdf 2>/dev/null \
	        | grep -i -E '^(Title|Subject|Keywords|Author|Creator):' \
	        | tr -d '[:space:]-' | grep -i -E '$(DENY_RE)'); \
	if [ -n "$$meta" ]; then \
	    echo "anon-check: FAIL -- de-anonymizing document metadata:"; \
	    echo "$$meta"; fail=1; \
	fi; \
	stray=$$(for f in *.pdf; do \
	    [ "$$f" = "$(MAIN).pdf" ] && continue; \
	    [ -e "$$f" ] || continue; \
	    pdftotext "$$f" - 2>/dev/null | tr -d '[:space:]-' \
	      | grep -q -i -E '$(DENY_RE)' && echo "  $$f"; \
	  done); \
	if [ -n "$$stray" ]; then \
	    echo "anon-check: FAIL -- non-anonymous PDF(s) in the submission directory:"; \
	    echo "$$stray"; \
	    echo "  Move them out of this directory (see papers/archive/)."; fail=1; \
	fi; \
	[ $$fail -eq 0 ] || exit 1; \
	echo "anon-check: OK -- $(MAIN).pdf is clean and no stray PDF sits beside it."

# One command to run before uploading: build, verify anonymity, report pages.
.PHONY: submission
submission: anon-check pages

.PHONY: clean
clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log \
	      $(MAIN).out $(MAIN).toc
