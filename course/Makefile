# Makefile — build the Great Wall pilot-course PDFs.
#
# Targets:
#   make            build the textbook and every slide deck
#   make textbook   build textbook/textbook.pdf
#   make slides     build every slides/*.pdf
#   make clean      remove LaTeX aux files (keep PDFs)
#   make distclean  remove aux files AND built PDFs
#
# Requirements: a TeX Live / MacTeX install with latexmk, pdflatex, tikz,
# pgfplots, tcolorbox, and beamer (all in texlive-full). The shared style
# lives in style/greatwall.sty and is found via the relative \usepackage path
# from each document; we also add style/ to TEXINPUTS as a belt-and-suspenders.

LATEXMK ?= latexmk
LATEXMKFLAGS = -pdf -interaction=nonstopmode -halt-on-error -file-line-error
export TEXINPUTS := .:$(CURDIR)/style:$(TEXINPUTS)

TEXTBOOK_SRC := textbook/textbook.tex
TEXTBOOK_PDF := $(TEXTBOOK_SRC:.tex=.pdf)

# gwtheme.tex is an \input-ed theme fragment, not a standalone document.
SLIDE_SRCS := $(filter-out slides/gwtheme.tex,$(wildcard slides/*.tex))
SLIDE_PDFS := $(SLIDE_SRCS:.tex=.pdf)

.PHONY: all textbook slides clean distclean

all: textbook slides

textbook: $(TEXTBOOK_PDF)

slides: $(SLIDE_PDFS)

# Build each PDF in its own directory so the relative ../style path resolves.
%.pdf: %.tex style/greatwall.sty
	$(LATEXMK) $(LATEXMKFLAGS) -cd $<

clean:
	-$(LATEXMK) -C -cd $(TEXTBOOK_SRC) $(SLIDE_SRCS) 2>/dev/null || true
	@rm -f textbook/*.aux textbook/*.log textbook/*.out textbook/*.toc \
	       textbook/*.fls textbook/*.fdb_latexmk textbook/*.nav \
	       textbook/*.snm textbook/*.vrb \
	       slides/*.aux slides/*.log slides/*.out slides/*.toc \
	       slides/*.fls slides/*.fdb_latexmk slides/*.nav \
	       slides/*.snm slides/*.vrb
	@echo "Cleaned LaTeX aux files."

distclean: clean
	@rm -f $(TEXTBOOK_PDF) $(SLIDE_PDFS)
	@echo "Removed built PDFs."
