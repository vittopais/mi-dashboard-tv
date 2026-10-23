#!/usr/bin/env python3
"""Fetch current Spanish headlines and write the static file used by the dashboard."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "news.json"
FEEDS = {
    "argentina": "Argentina when:1d",
    "mundo": "site:bbc.com/mundo internacional when:1d",
    "economia": "economía Argentina when:1d",
    "ciencia": "astronomía descubrimiento ciencia when:1d",
    "tecnologia": "tecnología empresas internet when:1d",
    "ia": "inteligencia artificial investigación when:1d",
}


def fetch_feed(query: str) -> list[dict[str, str]]:
    params = urllib.parse.urlencode(
        {"q": query, "hl": "es-419", "gl": "AR", "ceid": "AR:es-419"}
    )
    url = "https://news.google.com/rss/search?" + params
    result = subprocess.run(
        [
            "curl",
            "--fail",
            "--silent",
            "--show-error",
            "--location",
            "--max-time",
            "20",
            "--user-agent",
            "Mozilla/5.0 (compatible; MiCasaDashboard/1.0)",
            url,
        ],
        check=True,
        capture_output=True,
    )
    root = ET.fromstring(result.stdout)

    items: list[dict[str, str]] = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        source = item.findtext("source") or "Google News"
        pub_date = (item.findtext("pubDate") or "").strip()
        if title and link.startswith("https://"):
            items.append(
                {"title": title, "link": link, "author": source.strip(), "pubDate": pub_date}
            )
            if len(items) == 15:
                break
    def published_timestamp(item: dict[str, str]) -> float:
        try:
            published = parsedate_to_datetime(item["pubDate"])
            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)
            return published.timestamp()
        except (KeyError, TypeError, ValueError, OverflowError):
            return 0

    items.sort(key=published_timestamp, reverse=True)
    return items


def main() -> None:
    try:
        existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
        categories = existing.get("categories", {})
    except (OSError, json.JSONDecodeError):
        categories = {}

    used_links: set[str] = set()
    used_titles: set[str] = set()

    def remember(item: dict[str, str]) -> None:
        used_links.add(item.get("link", ""))
        used_titles.add(" ".join(item.get("title", "").lower().split()))

    def remember_previous(category: str) -> None:
        previous = categories.get(category, [])
        if previous:
            remember(previous[0])

    for category, query in FEEDS.items():
        try:
            items = fetch_feed(query)
            selected = next(
                (
                    item
                    for item in items
                    if item["link"] not in used_links
                    and " ".join(item["title"].lower().split()) not in used_titles
                ),
                None,
            )
            if selected:
                categories[category] = [selected]
                remember(selected)
                print(f"{category}: titular más reciente")
            else:
                remember_previous(category)
                print(f"{category}: sin noticia distinta; se conservan los anteriores")
        except Exception as exc:  # Keep the last good snapshot if a feed is temporarily unavailable.
            remember_previous(category)
            print(f"{category}: no se pudo actualizar ({exc}); se conservan los anteriores")

    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "categories": {key: categories.get(key, []) for key in FEEDS},
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, OUTPUT)


if __name__ == "__main__":
    main()
