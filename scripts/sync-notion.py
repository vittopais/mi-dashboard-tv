#!/usr/bin/env python3
"""Publish the selected Notion checklist as a small static JSON snapshot."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notion.json"
API_VERSION = "2026-03-11"


def notion_get(url: str, token: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": API_VERSION,
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Notion respondió HTTP {error.code}.") from None


def block_children(block_id: str, token: str):
    cursor = None
    while True:
        params = {"page_size": "100"}
        if cursor:
            params["start_cursor"] = cursor
        url = f"https://api.notion.com/v1/blocks/{block_id}/children?{urllib.parse.urlencode(params)}"
        page = notion_get(url, token)
        yield from page.get("results", [])
        if not page.get("has_more"):
            break
        cursor = page.get("next_cursor")
        if not cursor:
            break


def block_text(block: dict) -> str:
    kind = block.get("type")
    data = block.get(kind, {})
    rich_text = data.get("rich_text", []) if isinstance(data, dict) else []
    return "".join(part.get("plain_text", "") for part in rich_text).strip()


def collect_tasks(block_id: str, token: str, depth: int = 0) -> list[dict[str, object]]:
    if depth > 8:
        return []
    tasks = []
    for block in block_children(block_id, token):
        kind = block.get("type")
        if kind == "to_do":
            title = block_text(block)
            if title:
                tasks.append(
                    {
                        "id": block.get("id", ""),
                        "text": title,
                        "checked": bool(block.get("to_do", {}).get("checked", False)),
                    }
                )
        if block.get("has_children") and block.get("id"):
            tasks.extend(collect_tasks(block["id"], token, depth + 1))
    return tasks


def main() -> None:
    token = os.environ.get("NOTION_TOKEN", "").strip()
    page_id = os.environ.get("NOTION_PAGE_ID", "").strip()
    if not token:
        print("Notion todavía no está conectado; se conserva el archivo del sitio.")
        return
    if not page_id:
        print("Falta NOTION_PAGE_ID.", file=sys.stderr)
        raise SystemExit(1)

    payload = {
        "title": "Día",
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tasks": collect_tasks(page_id, token),
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Notion: {len(payload['tasks'])} tareas sincronizadas.")


if __name__ == "__main__":
    main()
