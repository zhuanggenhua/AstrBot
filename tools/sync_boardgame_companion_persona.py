from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "boardgame_companion_persona.md"
OUTPUT = ROOT / "reports" / "boardgame_companion_persona_sync_result.json"
BASE_URL = os.environ.get("ASTRBOT_BASE_URL", "http://127.0.0.1:6185")
PERSONA_ID = os.environ.get("ASTRBOT_PERSONA_ID", "boardgame_companion")
ASTRBOT_USERNAME = os.environ.get("ASTRBOT_USERNAME")
ASTRBOT_PASSWORD = os.environ.get("ASTRBOT_PASSWORD")


def section(text: str, heading: str) -> str:
    patterns = [
        rf"^##\s+{re.escape(heading)}\s*$",
        rf"^##\s+{re.escape(heading.replace('_suggestion', ' 建议'))}\s*$",
    ]
    starts = []
    for pat in patterns:
        m = re.search(pat, text, re.M)
        if m:
            starts.append(m.end())
    if not starts:
        raise ValueError(f"missing heading: {heading}")
    start = min(starts)
    rest = text[start:]
    next_heading = re.search(r"^##\s+.+$", rest, re.M)
    return rest[:next_heading.start()].strip() if next_heading else rest.strip()


def parse_begin_dialogs(block: str) -> list[str]:
    items: list[str] = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("- "):
            items.append(s[2:].strip())
    if len(items) % 2 != 0:
        raise ValueError(f"begin_dialogs must be even-length, got {len(items)}")
    return items


def api(path: str, payload: dict | None = None, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def login_token() -> str:
    if not ASTRBOT_USERNAME or not ASTRBOT_PASSWORD:
        raise RuntimeError(
            "Missing ASTRBOT_USERNAME / ASTRBOT_PASSWORD environment variables."
        )
    login = api(
        "/api/auth/login",
        {"username": ASTRBOT_USERNAME, "password": ASTRBOT_PASSWORD},
    )
    return login["data"]["token"]


def main() -> None:
    text = DOC.read_text(encoding="utf-8")
    system_prompt = section(text, "system_prompt_suggestion")
    begin_dialogs = parse_begin_dialogs(section(text, "begin_dialogs_suggestion"))
    custom_error_message = section(text, "custom_error_message_suggestion")
    token = login_token()

    update_payload = {
        "persona_id": PERSONA_ID,
        "system_prompt": system_prompt,
        "begin_dialogs": begin_dialogs,
        "custom_error_message": custom_error_message,
    }
    update_res = api("/api/persona/update", update_payload, token)
    detail_res = api("/api/persona/detail", {"persona_id": PERSONA_ID}, token)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(
            {
                "source_doc": str(DOC.relative_to(ROOT)),
                "base_url": BASE_URL,
                "persona_id": PERSONA_ID,
                "update": {k: update_res.get(k) for k in ["status", "message"]},
                "verify": {
                    "persona_id": detail_res["data"]["persona_id"],
                    "system_prompt_prefix": detail_res["data"]["system_prompt"][:400],
                    "begin_dialogs": detail_res["data"]["begin_dialogs"],
                    "custom_error_message": detail_res["data"]["custom_error_message"],
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(str(OUTPUT))


if __name__ == "__main__":
    main()
