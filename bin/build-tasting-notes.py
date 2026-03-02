#!/usr/bin/env python3
"""Generate tasting-notes.html from template + lineup.md + tasting-notes-content.md."""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINEUP_DATA = ROOT / "src" / "data" / "lineup.md"
NOTES_DATA = ROOT / "src" / "data" / "tasting-notes-content.md"
TEMPLATE = ROOT / "src" / "templates" / "tasting-notes.template.html"
OUTPUT = ROOT / "site" / "tasting-notes.html"


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


def parse_notes(text):
    """Parse tasting-notes-content.md into a dict keyed by beer number."""
    notes = {}
    beer_sections = re.split(r"^## \d+\. ", text, flags=re.MULTILINE)[1:]
    for i, section in enumerate(beer_sections, 1):
        lines = section.strip().splitlines()
        # Skip the beer name line (first line)
        content_lines = lines[1:]
        notes[i] = parse_beer_notes(content_lines)
    return notes


def parse_beer_notes(lines):
    """Parse a single beer's notes into a list of (type, content) tuples.

    Types: 'h3', 'p', 'kicker'
    """
    elements = []
    current_para = []

    def flush_para():
        if current_para:
            text = " ".join(current_para)
            elements.append(("p", text))
            current_para.clear()

    for line in lines:
        line = line.strip()
        if not line:
            flush_para()
            continue
        if line.startswith("### "):
            flush_para()
            elements.append(("h3", line[4:]))
        elif line.startswith("> "):
            flush_para()
            # Strip > and surrounding *italic* markers
            kicker = line[2:].strip()
            if kicker.startswith("*") and kicker.endswith("*"):
                kicker = kicker[1:-1]
            elements.append(("kicker", kicker))
        else:
            current_para.append(line)

    flush_para()
    return elements


def md_to_html(text):
    """Convert markdown inline formatting to HTML.

    Handles **bold** → <strong> and escapes & for HTML.
    """
    # Escape & but not if already part of an entity-like pattern
    # We need to be careful: escape & first, then handle bold
    text = text.replace("&", "&amp;")
    # Convert **bold** to <strong>
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def build_paired_songs(beer):
    """Build the paired-songs div, or empty string if no songs."""
    song1 = beer.get("Song 1", "")
    song2 = beer.get("Song 2", "")
    if not song1:
        return ""
    # Split "Title — Artist" and escape &
    def format_song(s):
        return html.escape(s).replace(" — ", " &mdash; ").replace(" — ", " &mdash; ")
    parts = []
    if song1:
        parts.append(f"<div>{format_song(song1)}</div>")
    if song2:
        parts.append(f"<div>{format_song(song2)}</div>")
    return f'    <div class="paired-songs">{"".join(parts)}</div>\n'


def build_slide_nav(current, total):
    """Build the slide-nav div."""
    links = []
    for i in range(1, total + 1):
        cls = ' class="current"' if i == current else ""
        links.append(f'    <a href="#beer{i}"{cls}>{i}</a>')
    return "  <div class=\"slide-nav\">\n" + "\n".join(links) + "\n  </div>"


def build_notes_html(elements):
    """Convert parsed note elements to HTML."""
    parts = []
    for typ, content in elements:
        text = md_to_html(content)
        if typ == "h3":
            parts.append(f"    <h3>{text}</h3>")
        elif typ == "p":
            parts.append(f"    <p>{text}</p>")
        elif typ == "kicker":
            parts.append(f'    <p class="kicker">{text}</p>')
    return "\n".join(parts)


def build_slide(num, beer, notes_elements, total):
    """Build a complete slide div."""
    paired = build_paired_songs(beer)
    image = beer["Image"]
    name = beer["name"]
    brewery = beer["Brewery"]
    style = beer["Style"]
    abv = beer["ABV"]
    nav = build_slide_nav(num, total)
    notes_html = build_notes_html(notes_elements)

    # Build the notes section with blank lines between elements
    # to match the original formatting (blank line before each h3 except first)
    formatted_notes = []
    for i, (typ, content) in enumerate(notes_elements):
        text = md_to_html(content)
        if typ == "h3":
            if i > 0:
                formatted_notes.append("")
            formatted_notes.append(f"    <h3>{text}</h3>")
        elif typ == "p":
            formatted_notes.append(f"    <p>{text}</p>")
        elif typ == "kicker":
            formatted_notes.append("")
            formatted_notes.append(f'    <p class="kicker">{text}</p>')
    notes_block = "\n".join(formatted_notes)

    return (
        f"<!-- BEER {num} -->\n"
        f'<div class="slide" id="beer{num}">\n'
        f"  <div class=\"slide-header\">\n"
        f"{paired}"
        f"    <img src=\"{image}\" alt=\"\">\n"
        f"    <div class=\"title-block\">\n"
        f"      <h2>{name}</h2>\n"
        f"      <div class=\"meta\">{html.escape(brewery)} &middot; {html.escape(style)} &middot; {abv}</div>\n"
        f"    </div>\n"
        f"  </div>\n"
        f"  <div class=\"notes\">\n"
        f"{notes_block}\n"
        f"  </div>\n"
        f"{nav}\n"
        f"</div>"
    )


if __name__ == "__main__":
    beers = parse_lineup(LINEUP_DATA.read_text())
    notes = parse_notes(NOTES_DATA.read_text())
    total = len(beers)

    slides = []
    for i, beer in enumerate(beers, 1):
        beer_notes = notes.get(i, [])
        slides.append(build_slide(i, beer, beer_notes, total))

    slides_html = "\n\n".join(slides)
    template = TEMPLATE.read_text()
    output = template.replace("<!-- {{SLIDES}} -->", slides_html)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output)
    print(f"Generated {OUTPUT.name} with {total} slides")
