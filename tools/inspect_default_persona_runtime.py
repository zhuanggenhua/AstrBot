import json
import urllib.request
from pathlib import Path

login_payload = {"username": "astrbot", "password": "8b81404f551dd67b3053e92d0d93c765"}
req = urllib.request.Request(
    "http://127.0.0.1:6185/api/auth/login",
    data=json.dumps(login_payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
login = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
token = login["data"]["token"]

req2 = urllib.request.Request(
    "http://127.0.0.1:6185/api/config/get",
    headers={"Authorization": "Bearer " + token},
)
res = json.loads(urllib.request.urlopen(req2).read().decode("utf-8"))
Path("reports").mkdir(exist_ok=True)
Path("reports/runtime_config_snapshot.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"top_keys": list(res.keys()), "data_keys": list(res.get("data", {}).keys()) if isinstance(res.get("data"), dict) else type(res.get("data")).__name__}, ensure_ascii=False, indent=2))
