#!/usr/bin/env python3
"""Generate index.html from lineup.html template + lineup.md data."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINEUP_DATA = ROOT / "src" / "data" / "lineup.md"
TEMPLATE = ROOT / "src" / "templates" / "lineup.template.html"
OUTPUT = ROOT / "site" / "index.html"


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


def build_beer_item(beer):
    """Build a single <li> beer item."""
    return (
        f'    <li class="beer-item">\n'
        f'      <img src="{beer["Image"]}" alt="{beer["name"]}">\n'
        f'      <div class="info">\n'
        f'        <div class="name">{beer["name"]}</div>\n'
        f'        <div class="meta">{beer["Brewery"]} &middot; {beer["Style"]} &middot; {beer["ABV"]}</div>\n'
        f'        <div class="desc">{beer["Description"]}</div>\n'
        f'      </div>\n'
        f'    </li>'
    )


if __name__ == "__main__":
    beers = parse_lineup(LINEUP_DATA.read_text())
    items = "\n".join(build_beer_item(b) for b in beers)
    html = TEMPLATE.read_text().replace("    <!-- {{BEER_LIST}} -->", items)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html)
    print(f"Generated {OUTPUT.name} with {len(beers)} beers")
