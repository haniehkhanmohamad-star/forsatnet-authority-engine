import json
import os
import pathlib
import sys
import urllib.error
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
    if job.get("status") != "ready":
        fail(f"Job status is {job.get('status')!r}; expected 'ready'.")
    if job.get("published"):
        print("Job is already marked published. Nothing to do.")
        return

    article_path = ROOT / job["article_path"]
    body_markdown = article_path.read_text(encoding="utf-8")

    # DEV renders the API title separately, so avoid a duplicated H1 when the file starts with one.
    first_line, sep, rest = body_markdown.partition("\n")
    if first_line.startswith("# "):
        body_markdown = rest.lstrip("\n") if sep else ""

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
            "User-Agent": "forsatnet-authority-engine/1.1",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        fail(f"DEV publication failed with HTTP {exc.code}: {detail}")
    except Exception as exc:
        fail(f"DEV publication failed: {exc}")

    article_url = result.get("url")
    if not article_url:
        fail(f"DEV returned no article URL: {json.dumps(result, ensure_ascii=False)}")

    job["published"] = True
    job["status"] = "published"
    job["dev_article_id"] = result.get("id")
    job["published_url"] = article_url
    job["published_slug"] = result.get("slug")
    QUEUE.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    output = {
        "id": result.get("id"),
        "url": article_url,
        "slug": result.get("slug"),
        "title": result.get("title"),
        "target_url": job.get("target_url"),
        "anchor_text": job.get("anchor_text"),
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
