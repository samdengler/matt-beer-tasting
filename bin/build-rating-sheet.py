#!/usr/bin/env python3
"""Generate rating-sheet.html from template + lineup.md data."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINEUP_DATA = ROOT / "src" / "data" / "lineup.md"
TEMPLATE = ROOT / "src" / "templates" / "rating-sheet.template.html"
OUTPUT = ROOT / "site" / "rating-sheet.html"

BEER_ICON_SVG = (
    '<svg viewBox="0 0 26 32" fill="none" stroke="#1a1a1a" stroke-width="1.5">'
    '<path d="M5 8 L4 26 Q4 29 6 29 L18 29 Q20 29 20 26 L19 8 Z"/>'
    '<line x1="5" y1="8" x2="19" y2="8" stroke-width="2"/>'
    '<path d="M19 13 L22 13 Q23.5 13 23.5 15 L23.5 20 Q23.5 22 22 22 L20 22" stroke-width="1.5"/>'
    '<path d="M4 8 Q4 5 7 4 Q10 2.5 12 4 Q14 2 17 3.5 Q20 5 20 8" fill="#1a1a1a" stroke="none" opacity="0.12"/>'
    '<path d="M4 8 Q4 5 7 4 Q10 2.5 12 4 Q14 2 17 3.5 Q20 5 20 8" fill="none" stroke="#1a1a1a" stroke-width="1.5"/>'
    '</svg>'
)


def parse_lineup(text):
    """Parse lineup.md into a list of beer dicts."""
    beers = []
    sections = re.split(r"^## \d+\. ", text, flags=re.MULTILINE)[1:]
    for section in sections:
        lines = section.strip().splitlines()
        name = lines[0].strip()
        fields = {}
        for line in lines[1:]:
            m = re.match(r"^- \*\*(.+?)\*\*:\s*(.+)$", line)
            if m:
                fields[m.group(1)] = m.group(2)
        beers.append({"name": name, **fields})
    return beers


def build_beer_card(num, beer):
    """Build a single beer card div."""
    image = beer["Image"]
    name = html.escape(beer["name"])
    brewery = html.escape(beer["Brewery"])
    style = html.escape(beer["Style"])
    abv = beer["ABV"]
    untappd = beer.get("Untappd", "")
    desc = html.escape(beer["Description"])

    # Build 5 beer icons for rating
    icons = "\n".join(
        f'        <div class="beer-icon">{BEER_ICON_SVG}</div>'
        for _ in range(5)
    )

    # Build paired-with line (commented out, matching original)
    song1 = beer.get("Song 1", "")
    song2 = beer.get("Song 2", "")
    paired = ""
    if song1:
        songs = html.escape(song1)
        if song2:
            songs += " &middot; " + html.escape(song2)
        paired = f'    <!-- <div class="paired-with"><span class="label">Paired with </span>{songs}</div> -->\n'

    return (
        f'<!-- Beer {num} -->\n'
        f'<div class="beer-card">\n'
        f'  <div class="beer-num"><img src="{image}" alt="">{num}</div>\n'
        f'  <div class="beer-info">\n'
        f'    <div class="beer-name">{name}</div>\n'
        f'    <div class="beer-meta">{brewery} &middot; {style} &middot; {abv} <span class="untappd">Untappd {untappd}</span></div>\n'
        f'    <div class="beer-desc">{desc}</div>\n'
        f'{paired}'
        f'    <div class="rating-row">\n'
        f'      <span class="rating-label">Rating</span>\n'
        f'      <div class="beer-circles">\n'
        f'{icons}\n'
        f'      </div>\n'
        f'    </div>\n'
        f'    <div class="notes-line">\n'
        f'      <span class="notes-label">Notes</span>\n'
        f'      <span class="notes-blank"></span>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</div>'
    )


if __name__ == "__main__":
    beers = parse_lineup(LINEUP_DATA.read_text())
    cards = "\n\n".join(build_beer_card(i, b) for i, b in enumerate(beers, 1))
    template = TEMPLATE.read_text()
    output = template.replace("<!-- {{BEER_CARDS}} -->", cards)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output)
    print(f"Generated {OUTPUT.name} with {len(beers)} beer cards")
