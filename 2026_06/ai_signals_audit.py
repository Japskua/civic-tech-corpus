"""Collect evidence for every row of ai_signals.csv as of crawl time.

Usage: python audit_ai_signals.py <ai_signals.csv> <out.jsonl>
Requires an authenticated `gh` CLI. Output is one JSON object per signal with
the raw evidence found on GitHub; true/false-positive judgement is done by a
human reviewing that evidence.
"""

from __future__ import annotations

import base64
import csv
import json
import subprocess
import sys
import time

CRAWL_END = "2026-06-04T16:17:08Z"
CRAWL_DATE = "2026-06-04"

TRAILER_NEEDLE = {
    "claude_code": "claude", "github_copilot": "copilot", "cursor": "cursor",
    "devin": "devin", "openai_codex": "codex", "aider": "aider", "jules": "jules",
}
AGENT_LOGINS = {
    "github_copilot": ["Copilot", "copilot-swe-agent[bot]"],
    "devin": ["devin-ai-integration[bot]"],
    "jules": ["google-labs-jules[bot]"],
    "cursor": ["cursoragent", "cursor[bot]"],
    "claude_code": ["claude[bot]", "noreply@anthropic.com"],
}


def gh(path: str, params: dict | None = None, retries: int = 4):
    cmd = ["gh", "api", "-X", "GET", path]
    for k, v in (params or {}).items():
        cmd += ["-f", f"{k}={v}"]
    for attempt in range(retries):
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0:
            return json.loads(p.stdout) if p.stdout.strip() else None
        err = p.stderr + p.stdout
        if "rate limit" in err.lower() or "secondary" in err.lower():
            time.sleep(20 * (attempt + 1))
            continue
        return {"_error": err.strip()[:300]}
    return {"_error": "rate limited"}


def search(kind: str, q: str):
    time.sleep(2.2)  # search API: 30 requests/minute
    return gh(f"search/{kind}", {"q": q, "per_page": "100"})


_sha: dict[str, str | None] = {}


def crawl_sha(repo: str) -> str | None:
    if repo not in _sha:
        r = gh(f"repos/{repo}/commits", {"until": CRAWL_END, "per_page": "1"})
        _sha[repo] = r[0]["sha"] if isinstance(r, list) and r else None
    return _sha[repo]


def content(repo: str, path: str):
    r = gh(f"repos/{repo}/contents/{path}", {"ref": crawl_sha(repo) or "HEAD"})
    if isinstance(r, dict) and "_error" in r:
        return None
    if isinstance(r, list):
        return {"type": "dir", "entries": [e["name"] for e in r][:15]}
    text = base64.b64decode(r.get("content", "")).decode("utf-8", "replace")
    return {"type": "file", "text": text}


def matching_lines(text: str, needle: str, ctx_filter=None, limit=8):
    out = []
    for ln in text.splitlines():
        low = ln.lower()
        if needle in low and (ctx_filter is None or ctx_filter(low)):
            out.append(ln.strip()[:200])
    return sorted(set(out))[:limit]


def audit(row: dict) -> dict:
    repo, src, tool, ev = row["repo_full_name"], row["source"], row["tool"], row["evidence"]
    res = {**row, "found": False, "evidence_seen": []}
    if src == "file":
        path = ev.split(":", 1)[1]
        c = content(repo, path)
        if c:
            res["found"] = True
            res["evidence_seen"] = (c["entries"] if c["type"] == "dir"
                                    else [c["text"][:600]])
    elif src == "workflow":
        fname = ev.split(":")[1]
        c = content(repo, f".github/workflows/{fname}")
        if c and c["type"] == "file":
            lines = matching_lines(c["text"], "claude") or matching_lines(c["text"], tool.split("_")[0])
            res["found"] = bool(lines)
            res["evidence_seen"] = lines
    elif src == "dependency":
        needle = ev.split(":", 1)[1]
        for mf in ("requirements.txt", "pyproject.toml", "package.json"):
            c = content(repo, mf)
            if c and c["type"] == "file":
                lines = matching_lines(c["text"], needle)
                if lines:
                    res["found"] = True
                    res["evidence_seen"] += [f"{mf}: {x}" for x in lines]
    elif src == "commit_trailer":
        needle = TRAILER_NEEDLE.get(tool, tool)
        r = search("commits", f'repo:{repo} {needle} committer-date:<={CRAWL_DATE}')
        items = r.get("items", []) if isinstance(r, dict) else []
        trailer = lambda low: low.startswith("co-authored-by:") or "generated with" in low or "🤖 generated" in low
        lines = []
        for it in items:
            lines += matching_lines(it["commit"]["message"], needle, trailer)
        res["found"] = bool(lines)
        res["evidence_seen"] = sorted(set(lines))[:10]
        res["search_total"] = r.get("total_count") if isinstance(r, dict) else None
    elif src == "commit_author":
        seen = []
        for who in AGENT_LOGINS.get(tool, []):
            r = gh(f"repos/{repo}/commits", {"author": who, "until": CRAWL_END, "per_page": "5"})
            if isinstance(r, list) and r:
                for c in r[:3]:
                    a = c["commit"]["author"]
                    seen.append(f'{who} | {a["name"]} <{a["email"]}> | {c["commit"]["message"].splitlines()[0][:80]}')
        res["found"] = bool(seen)
        res["evidence_seen"] = seen
    elif src == "pr_author":
        login = ev.split(":", 1)[1]
        q_login = login if not login.endswith("[bot]") else "app/" + login[:-5]
        r = search("issues", f"repo:{repo} is:pr author:{q_login} created:<={CRAWL_DATE}")
        items = r.get("items", []) if isinstance(r, dict) else []
        res["found"] = bool(items)
        res["search_total"] = r.get("total_count") if isinstance(r, dict) else None
        res["evidence_seen"] = [f'#{i["number"]} {i["user"]["login"]}: {i["title"][:80]}' for i in items[:3]]
    elif src == "pr_body":
        needle = TRAILER_NEEDLE.get(tool, tool)
        r = search("issues", f'repo:{repo} is:pr {needle} in:body created:<={CRAWL_DATE}')
        items = r.get("items", []) if isinstance(r, dict) else []
        lines = []
        for it in items:
            body = it.get("body") or ""
            low = body.lower()
            if needle in low and ("generated with" in low or "co-authored-by" in low):
                lines += [f'#{it["number"]}: ' + x for x in matching_lines(body, needle)[:2]]
                lines += [f'#{it["number"]}: ' + x for x in
                          matching_lines(body, "generated with")[:1] + matching_lines(body, "co-authored-by")[:1]]
        res["found"] = bool(lines)
        res["evidence_seen"] = sorted(set(lines))[:10]
    return res


def main() -> None:
    src, out = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(src)))
    with open(out, "w") as fh:
        for i, row in enumerate(rows, 1):
            res = audit(row)
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"[{i}/{len(rows)}] {row['repo_full_name']} {row['evidence']} -> found={res['found']}", flush=True)


if __name__ == "__main__":
    main()
