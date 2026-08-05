"""Parse Wikivoyage articles into prose sections and structured places.

Wikivoyage marks up every attraction, restaurant and hotel with a listing
template that already carries a name, coordinates, an address, opening hours and
a price. A parser that strips templates as "markup" throws that away and leaves
the retriever nothing but prose. We keep both:

  * prose chunks, for questions answered by text ("when should I visit?")
  * place records, for anything that needs geography (every itinerary)

The place records are the reason the assistant can plan a day that makes sense.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Templates that describe a place. Wikivoyage uses {{see}}, {{do}}, {{eat}},
# {{drink}}, {{sleep}}, {{buy}}, {{go}}, and the generic {{listing}}.
PLACE_TEMPLATES = ("see", "do", "eat", "drink", "sleep", "buy", "go", "listing", "marker")

HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
XML_TAG = re.compile(r"<(maplink|mapframe|gallery|ref|nowiki|imagemap)[^>]*?(/>|>.*?</\1>)", re.S | re.I)
SELF_CLOSING = re.compile(r"<[^>]{1,200}?/?>")
WIKILINK = re.compile(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]")
EXTLINK = re.compile(r"\[https?://\S+\s+([^\]]*)\]")
BARE_EXTLINK = re.compile(r"\[?https?://\S+\]?")
HEADING = re.compile(r"^(=+)\s*(.*?)\s*=+\s*$", re.M)
EMPTY_BULLET = re.compile(r"^\s*[*#:;]+\s*$", re.M)
FILE_LINK = re.compile(r"\[\[(?:File|Image):[^\]]*\]\]", re.I)


@dataclass
class Place:
    """One attraction, restaurant or hotel, with coordinates where given."""
    name: str
    kind: str
    city: str
    lat: float | None = None
    lon: float | None = None
    address: str = ""
    hours: str = ""
    price: str = ""
    description: str = ""

    @property
    def has_coords(self) -> bool:
        return self.lat is not None and self.lon is not None

    def as_text(self) -> str:
        """One retrievable line. Carries its own city, so it is self-describing."""
        bits = [f"{self.name} ({self.kind}) in {self.city}."]
        for label, value in (("Address", self.address), ("Hours", self.hours), ("Price", self.price)):
            if value:
                bits.append(f"{label}: {value}.")
        if self.description:
            bits.append(self.description)
        return " ".join(bits)


@dataclass
class Section:
    doc_id: str
    city: str
    path: str          # "Kyoto > See > Temples"
    text: str
    places: list[Place] = field(default_factory=list)


def _split_template(body: str) -> dict[str, str]:
    """Split a template body on top-level pipes, respecting nesting."""
    fields, depth, current = [], 0, []
    for ch in body:
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        if ch == "|" and depth == 0:
            fields.append("".join(current)); current = []
        else:
            current.append(ch)
    fields.append("".join(current))
    out = {"_name": fields[0].strip().lower()}
    for field_text in fields[1:]:
        if "=" in field_text:
            key, value = field_text.split("=", 1)
            out[key.strip().lower()] = value.strip()
    return out


def _iter_templates(text: str):
    """Yield (start, end, body) for every top-level {{...}} in the text."""
    depth, start = 0, None
    i = 0
    while i < len(text) - 1:
        pair = text[i:i + 2]
        if pair == "{{":
            if depth == 0:
                start = i
            depth += 1; i += 2; continue
        if pair == "}}":
            depth -= 1
            if depth == 0 and start is not None:
                yield start, i + 2, text[start + 2:i]
                start = None
            i += 2; continue
        i += 1


def _to_float(value: str) -> float | None:
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return None


def clean_prose(text: str) -> str:
    """Reduce wikitext to readable prose. Templates are removed by the caller."""
    text = HTML_COMMENT.sub(" ", text)
    text = FILE_LINK.sub(" ", text)
    text = XML_TAG.sub(" ", text)
    text = SELF_CLOSING.sub(" ", text)
    text = EXTLINK.sub(r"\1", text)
    text = BARE_EXTLINK.sub(" ", text)
    text = WIKILINK.sub(r"\1", text)
    text = re.sub(r"'''?", "", text)
    text = EMPTY_BULLET.sub("", text)
    text = re.sub(r"^[*#:;]+\s*", "", text, flags=re.M)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_article(wikitext: str, city: str, doc_id: str) -> list[Section]:
    """Split an article into sections, pulling the place listings out of each."""
    # Record where each heading starts, so a template can be attributed to a section.
    headings = [(m.start(), len(m.group(1)), m.group(2).strip()) for m in HEADING.finditer(wikitext)]
    bounds = [h[0] for h in headings] + [len(wikitext)]

    sections: list[Section] = []
    for index, (start, level, title) in enumerate(headings):
        block = wikitext[start:bounds[index + 1]]

        places, spans = [], []
        for t_start, t_end, body in _iter_templates(block):
            fields = _split_template(body)
            if fields["_name"] not in PLACE_TEMPLATES:
                spans.append((t_start, t_end))          # drop non-place templates
                continue
            name = fields.get("name", "").strip()
            if not name:
                spans.append((t_start, t_end)); continue
            places.append(Place(
                name=clean_prose(name), kind=fields["_name"], city=city,
                lat=_to_float(fields.get("lat", "")), lon=_to_float(fields.get("long", fields.get("lon", ""))),
                address=clean_prose(fields.get("address", "")),
                hours=clean_prose(fields.get("hours", "")),
                price=clean_prose(fields.get("price", "")),
                description=clean_prose(fields.get("content", "")),
            ))
            spans.append((t_start, t_end))

        stripped = "".join(
            block[a:b] for a, b in zip(
                [0] + [e for _, e in spans], [s for s, _ in spans] + [len(block)])
        )
        prose = clean_prose(HEADING.sub(lambda m: "", stripped))

        # Build the heading path so every section knows where it sits.
        ancestors = [t for s, lv, t in headings[:index] if lv < level]
        path = " > ".join([city] + ancestors[-1:] + [title]) if title else city
        sections.append(Section(doc_id=doc_id, city=city, path=path, text=prose, places=places))
    return sections
