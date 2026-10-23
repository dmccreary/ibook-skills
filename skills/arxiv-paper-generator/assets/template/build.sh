#!/usr/bin/env bash
# Build script for an arXiv-format paper.
# Uses Tectonic (brew install tectonic); falls back to latexmk + pdfLaTeX if Tectonic is missing.
#
#   ./build.sh            build main.pdf and report pages, warnings and problems
#   ./build.sh clean      remove build artifacts
#   ./build.sh arxiv      build, create arxiv-upload.zip, and test-compile it in a clean folder
#                         (-a is accepted as an alias, matching older build scripts)
#   ./build.sh release    build, then copy main.pdf to <folder-name>-v<version>.pdf

set -euo pipefail

cd "$(dirname "$0")"
SLUG="$(basename "$PWD")"

build_pdf() {
    echo "Building ${SLUG}..."
    if command -v tectonic >/dev/null 2>&1; then
        # Keep main.bbl (needed in the arXiv package) and main.log (for the report below)
        tectonic --keep-intermediates --keep-logs main.tex
    elif command -v latexmk >/dev/null 2>&1; then
        latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    else
        echo "Error: no LaTeX engine found. Install Tectonic with: brew install tectonic" >&2
        exit 1
    fi
    if [ ! -f main.pdf ]; then
        echo "Error: PDF generation failed." >&2
        exit 1
    fi
    report
}

report() {
    # grep exits 1 when nothing matches, so pipefail is relaxed while counting
    set +o pipefail
    local pages undefined overfull missing nonascii
    pages=$(grep -Eo 'Output written on [^ ]+ \([0-9]+ page' main.log | grep -Eo '[0-9]+' | tail -1)
    undefined=$(grep -Ec "(Citation|Reference) .* undefined" main.log || true)
    overfull=$(grep -Eo 'Overfull \\hbox \([0-9.]+pt' main.log | grep -Eo '[0-9.]+' | awk '$1 > 10' | wc -l | tr -d ' ')
    missing=$(grep -c "Missing character" main.log || true)
    nonascii=$(LC_ALL=C grep -n $'[\x80-\xFF]' main.tex sections/*.tex 2>/dev/null | wc -l | tr -d ' ')
    set -o pipefail

    echo ""
    echo "Built main.pdf: ${pages:-?} pages, $(du -h main.pdf | cut -f1)"
    [ "$undefined" -gt 0 ] && echo "  WARNING: ${undefined} undefined citation/reference warnings (see main.log)"
    [ "$overfull" -gt 0 ] && echo "  WARNING: ${overfull} overfull boxes wider than 10pt (search main.log for 'Overfull')"
    [ "$missing" -gt 0 ] && echo "  WARNING: ${missing} 'Missing character' warnings -- Unicode the font can't show"
    [ "$nonascii" -gt 0 ] && echo "  NOTE: ${nonascii} source lines contain non-ASCII characters; arXiv's pdfLaTeX may reject some (run score_paper.py)"
    return 0
}

package_arxiv() {
    echo ""
    echo "Creating arXiv upload package..."
    if [ ! -f main.bbl ]; then
        echo "Error: main.bbl not found -- the build did not run BibTeX." >&2
        exit 1
    fi
    rm -f arxiv-upload.zip

    local files=(main.tex main.bbl sections/*.tex sections/*.bib)
    if [ -d figures ]; then
        while IFS= read -r f; do files+=("$f"); done < <(
            find figures -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
                -o -iname '*.pdf' -o -iname '*.tikz' \) ! -name '.*' | sort)
    fi
    # Code listings pulled in with \lstinputlisting, and arXiv ancillary files (anc/)
    for d in listings anc; do
        if [ -d "$d" ]; then
            while IFS= read -r f; do files+=("$f"); done < <(find "$d" -type f ! -name '.*' | sort)
        fi
    done
    zip -q arxiv-upload.zip "${files[@]}"
    echo "Created arxiv-upload.zip ($(du -h arxiv-upload.zip | cut -f1), ${#files[@]} files)"

    # Prove the package is self-contained: compile it from a clean folder
    local tmp
    tmp="$(mktemp -d)"
    unzip -q arxiv-upload.zip -d "$tmp"
    if command -v tectonic >/dev/null 2>&1; then
        if (cd "$tmp" && tectonic --keep-logs main.tex >/dev/null 2>&1) && [ -f "$tmp/main.pdf" ]; then
            echo "Package test-compile: PASS"
        else
            echo "Package test-compile: FAIL -- see $tmp/main.log" >&2
            exit 1
        fi
    else
        echo "Package test-compile: skipped (Tectonic not installed)"
    fi
    rm -rf "$tmp"
}

release() {
    local version
    version=$(sed -n 's/.*\\newcommand{\\paperversion}{\([^}]*\)}.*/\1/p' main.tex | head -1)
    if [ -z "$version" ]; then
        echo "Error: no \\newcommand{\\paperversion}{...} in main.tex" >&2
        exit 1
    fi
    cp main.pdf "${SLUG}-v${version}.pdf"
    echo "Saved ${SLUG}-v${version}.pdf"
}

case "${1:-}" in
    clean)
        rm -f main.pdf main.aux main.log main.out main.bbl main.blg main.toc \
              main.fls main.fdb_latexmk main.synctex.gz arxiv-upload.zip
        echo "Clean complete."
        ;;
    arxiv|-a)
        build_pdf
        package_arxiv
        ;;
    release)
        build_pdf
        release
        ;;
    "")
        build_pdf
        ;;
    *)
        echo "Usage: ./build.sh [clean|arxiv|release]" >&2
        exit 1
        ;;
esac
