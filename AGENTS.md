# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Project Overview

Beer tasting event for Matt's 50th birthday (Feb 28, 2026). This repo contains:

### Source files (`src/`)
- `src/data/lineup.md` - beer lineup data (brewery, style, ABV, images, songs)
- `src/data/tasting-notes-content.md` - presenter notes and tasting descriptions
- `src/templates/lineup.template.html` - landing page template
- `src/templates/tasting-notes.template.html` - tasting notes template
- `src/templates/rating-sheet.template.html` - rating card template
- `src/images/` - beer label images, QR codes, Sergio illustration

### Build scripts (`bin/`)
- `bin/build-index.py` - generates `site/index.html` from lineup template + data
- `bin/build-tasting-notes.py` - generates `site/tasting-notes.html` from tasting notes template + data
- `bin/build-rating-sheet.py` - generates `site/rating-sheet.html` from rating sheet template + data
- `bin/to-pdf.sh` - weasyprint wrapper for PDF generation

### Other files
- `shopping-list.md` - shopping route, quantities, budget
- `playlist-pairings.md` - Spotify playlist pairings
- `_external/manifest.md` - brewery research manifest (other research files gitignored)

### Generated directories (gitignored)
- `site/` - intermediate HTML output from build scripts
- `dist/` - final Vite build output, deployed to GitHub Pages

## Build Pipeline

```
src/data/ + src/templates/ → bin/build-*.py → site/*.html → vite build → dist/
```

### Prerequisites

System libraries (macOS):
```bash
brew install pango
```

Python dependencies (install once):
```bash
uv sync
```

### Build Commands

```bash
npm run generate          # Generate all HTML into site/
npm run generate:index    # Generate just index.html
npm run generate:notes    # Generate just tasting-notes.html
npm run generate:rating   # Generate just rating-sheet.html
npm run build             # Generate + Vite build to dist/
npm run dev               # Generate + Vite dev server
npm run pdf               # Generate PDFs (notes + rating)
npm run pdf:notes         # PDF of tasting notes
npm run pdf:rating        # PDF of rating sheet + copy to site/public/
npm run all               # generate + pdf + build
```

### Generate PDF

```bash
bin/to-pdf.sh site/rating-sheet.html
```

This calls `.venv/bin/python` directly with `DYLD_FALLBACK_LIBRARY_PATH` to work around
macOS SIP stripping DYLD_* env vars from `uv run`.

PDFs are generated artifacts (.gitignored). Regenerate from HTML source.

### Untappd List

Public list: https://untappd.com/user/samdengler/lists/13782328

## Beads Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
