MAIN = main
SECTIONS = $(wildcard sections/*.tex)

$(MAIN).pdf: $(MAIN).tex $(SECTIONS) references.bib
	pdflatex -interaction=nonstopmode $(MAIN).tex
	bibtex   $(MAIN)
	pdflatex -interaction=nonstopmode $(MAIN).tex
	pdflatex -interaction=nonstopmode $(MAIN).tex

.PHONY: clean
clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out $(MAIN).toc
