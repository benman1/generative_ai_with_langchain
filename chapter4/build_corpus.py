"""Build the Japan travel corpus the chapter's assistant retrieves from.

Reads the raw Wikivoyage articles vendored under data/wikivoyage_raw/ and writes
data/japan_corpus.json with two collections:

  sections  prose, one entry per heading, carrying its own heading path
  places    attractions, restaurants and hotels, most with coordinates

The split matters. A parser that strips Wikivoyage's {{see}} / {{do}} / {{sleep}}
templates as markup deletes every place name and coordinate in the corpus and
keeps the debris around them. Chapter 4 measures what that costs.

Run:  python build_corpus.py
"""

from __future__ import annotations

import glob
import json
import os

from wikivoyage import parse_article

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "wikivoyage_raw")
OUT = os.path.join(HERE, "data", "japan_corpus.json")

MIN_ARTICLE_CHARS = 200      # below this the page is a redirect stub
MIN_SECTION_CHARS = 120      # below this a section is a heading and a bullet


def city_of(filename: str) -> str:
    """Kyoto_Higashiyama.wiki -> Kyoto. District pages belong to their parent."""
    return os.path.basename(filename)[:-5].split("_")[0]


def build() -> dict:
    sections, places, skipped = [], [], 0

    for path in sorted(glob.glob(os.path.join(RAW, "*.wiki"))):
        with open(path, encoding="utf-8") as handle:
            wikitext = handle.read()
        if len(wikitext) < MIN_ARTICLE_CHARS:
            skipped += 1
            continue

        name = os.path.basename(path)[:-5]
        parsed = parse_article(wikitext, city=city_of(path), doc_id=f"jp_{name.lower()}")

        for section in parsed:
            if len(section.text) >= MIN_SECTION_CHARS:
                sections.append({
                    "doc_id": section.doc_id,
                    "city": section.city,
                    "path": section.path,
                    "text": section.text,
                })
            for place in section.places:
                if not place.name:
                    continue
                places.append({
                    "doc_id": section.doc_id,
                    "city": place.city,
                    "name": place.name,
                    "kind": place.kind,
                    "lat": place.lat,
                    "lon": place.lon,
                    "text": place.as_text(),
                })

    return {"sections": sections, "places": places, "skipped_stubs": skipped}


def main() -> None:
    corpus = build()
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(corpus, handle, ensure_ascii=False, indent=1)

    with_coords = sum(1 for p in corpus["places"] if p["lat"] is not None)
    cities = sorted({s["city"] for s in corpus["sections"]})
    print(f"wrote {OUT}")
    print(f"  {len(corpus['sections'])} prose sections")
    print(f"  {len(corpus['places'])} places, {with_coords} with coordinates")
    print(f"  {len(cities)} cities: {', '.join(cities)}")
    print(f"  skipped {corpus['skipped_stubs']} redirect stubs")


if __name__ == "__main__":
    main()
