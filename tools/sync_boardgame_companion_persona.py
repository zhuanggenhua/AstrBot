from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "boardgame_companion_persona.md"
OUTPUT = ROOT / "reports" / "boardgame_companion_persona_sync_result.json"
BASE_URL = "http://127.0.0.1:6185"
LOGIN_PAYLOAD = {"username": "astrbot", "password": "8b81404f551dd67b3053e92d0d93c765"}
PERSONA_ID = "boardgame_companion"


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
    return rest[: next_heading.start()] .strip() if next_heading else rest.strip()


def parse_begin_dialogs(block: str) -> list[str]:
    items: list[str] = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("- "):
            items.append(s[2:].strip())
    if len(items) % 2 != 0:
        raise ValueError(f"begin_dialogs must be even-length, got {len(items)}")
    return items


def api(path: str, payload: dict, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    text = DOC.read_text(encoding="utf-8")
    system_prompt = section(text, "system_prompt_suggestion")
    begin_dialogs = parse_begin_dialogs(section(text, "begin_dialogs_suggestion"))
    custom_error_message = section(text, "custom_error_message_suggestion")

    login = api("/api/auth/login", LOGIN_PAYLOAD)
    token = login["data"]["token"]

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
