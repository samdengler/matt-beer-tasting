# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Project Overview

Beer tasting event for Matt's 50th birthday (Feb 28, 2026). This repo contains:
- `rating-sheet.html` - printable 4.25" x 11" rating card for card stock
- `shopping-list.md` - shopping route, quantities, budget
- `images/` - beer label logos, QR code, Sergio illustration
- `_external/manifest.md` - brewery research manifest (other research files gitignored)
- `bin/` - build scripts

## Build: Rating Card PDF

### Prerequisites

System libraries (macOS):
```bash
brew install pango
```

Python dependencies (install once):
```bash
uv sync
```

Or install as global CLI tools:
```bash
uv tool install weasyprint
uv tool install qrcode[pil]
```

### Generate QR Code

```bash
uv run qr "https://untappd.com/user/samdengler/lists/13782328" > images/untappd-qr.png
```

### Generate PDF

```bash
bin/to-pdf.sh rating-sheet.html
```

This calls `.venv/bin/python` directly with `DYLD_FALLBACK_LIBRARY_PATH` to work around
macOS SIP stripping DYLD_* env vars from `uv run`.

The PDF is a generated artifact (.gitignored). Regenerate it from the HTML source.

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
