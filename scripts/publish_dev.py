import json
import os
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUEUE = ROOT / "queue" / "001-ai-delegation-matrix.json"


def fail(message: str, code: int = 1):
    print(message, file=sys.stderr)
    raise SystemExit(code)


def main():
    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        fail("DEVTO_API_KEY is not configured. Refusing to publish.")

    job = json.loads(QUEUE.read_text(encoding="utf-8"))
    if job.get("platform") != "devto":
        fail("Job platform is not devto.")
    if job.get("published"):
        fail("Job is already marked published; refusing duplicate publication.")

    article_path = ROOT / job["article_path"]
    body_markdown = article_path.read_text(encoding="utf-8")

    payload = {
        "article": {
            "title": job["title"],
            "published": True,
            "body_markdown": body_markdown,
            "description": job["description"],
            "tags": job["tags"],
        }
    }

    req = urllib.request.Request(
        "https://dev.to/api/articles",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/vnd.forem.api-v1+json",
            "User-Agent": "forsatnet-authority-engine/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        fail(f"DEV publication failed: {exc}")

    output = {
        "id": result.get("id"),
        "url": result.get("url"),
        "slug": result.get("slug"),
        "title": result.get("title"),
        "target_url": job.get("target_url"),
        "anchor_text": job.get("anchor_text"),
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
