#!/usr/bin/env python3
"""Fetch current Spanish headlines and write the static file used by the dashboard."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "news.json"
FEEDS = {
    "argentina": "Argentina when:1d",
    "mundo": "mundo OR internacional when:1d",
    "economia": "economía Argentina when:1d",
    "politica": "política Argentina when:1d",
    "ciencia": "ciencia tecnología when:1d",
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
        if len(items) == 3:
            break
    return items


def main() -> None:
    try:
        existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
        categories = existing.get("categories", {})
    except (OSError, json.JSONDecodeError):
        categories = {}

    for category, query in FEEDS.items():
        try:
            items = fetch_feed(query)
            if items:
                categories[category] = items
                print(f"{category}: {len(items)} titulares")
            else:
                print(f"{category}: sin resultados nuevos; se conservan los anteriores")
        except Exception as exc:  # Keep the last good snapshot if a feed is temporarily unavailable.
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
