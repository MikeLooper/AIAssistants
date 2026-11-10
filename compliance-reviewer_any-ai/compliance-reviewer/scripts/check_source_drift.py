#!/usr/bin/env python3
"""Source-drift checker for the localized standards (maintainers only).

Never run this during a compliance review: reviews never fetch URLs. This script is
for maintenance sessions (see compliance-reviewer/STANDARDS-MAINTENANCE.md and REFRESH.md).

Each localized skill declares its pins in
    compliance-reviewer/skills/<skill>/references/standards/pins.json
and this script compares them with the live sources. It fetches only URLs that are
listed in compliance-review-core/references/approved-sources.md.

Commands
    lint   [skill ...]                      offline: manifests, allowlist, pins vs. headers, element mapping
    check  [skill ...] [--json] [--md FILE]  fetch sources and report drift
           [--method M ...]                  only run checks of these methods
           [--record-baselines]              fill empty baseline pins (writes pins.json)

Exit codes: 0 = no drift / lint clean, 1 = drift found / lint errors, 2 = fetch errors only.
Python 3.8+, standard library only. Set GITHUB_TOKEN to raise the GitHub API rate limit
(60 requests/hour without a token).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import html
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
CR = ROOT / "compliance-reviewer"
SKILLS = CR / "skills"
APPROVED = SKILLS / "compliance-review-core" / "references" / "approved-sources.md"
USER_AGENT = "compliance-reviewer-source-drift-check"
TIMEOUT = 40

METHODS = {
    "github-commit": {"required": ["repo", "pinned"], "pins": ["pinned", "pinnedDate"]},
    "github-release": {"required": ["repo", "pinned"], "pins": ["pinned"]},
    "learn-page": {"required": ["url"], "pins": ["msDate", "gitCommit"]},
    "redirect": {"required": ["url", "expect"], "pins": ["expect"]},
    "regex": {"required": ["url", "pattern", "pinned"], "pins": ["pinned"]},
    "http-status": {"required": ["url", "pinned"], "pins": []},
    "json": {"required": ["url", "select"], "pins": ["pinned"]},
    "text-hash": {"required": ["url"], "pins": ["pinned"]},
    "manual": {"required": ["note"], "pins": []},
}
BASELINE_FIELDS = {"learn-page": ["msDate", "gitCommit"], "json": ["pinned"], "text-hash": ["pinned"]}


# --------------------------------------------------------------------------- manifests

def skill_dirs(names):
    all_dirs = sorted(p for p in SKILLS.glob("review-*") if p.is_dir())
    if not names:
        return all_dirs
    picked = []
    for n in names:
        n = n if n.startswith("review-") else "review-" + n
        d = SKILLS / n
        if not d.is_dir():
            sys.exit(f"unknown skill: {n}")
        picked.append(d)
    return picked


def load_manifest(skill_dir):
    p = skill_dir / "references" / "standards" / "pins.json"
    if not p.exists():
        return None, p
    return json.loads(p.read_text(encoding="utf-8")), p


def save_manifest(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- allowlist

def approved_urls():
    text = APPROVED.read_text(encoding="utf-8")
    urls = set()
    for u in re.findall(r"https?://[^\s)`,>\]]+", text):
        urls.add(_norm(u))
    return urls


def _norm(u):
    u = u.rstrip(".;")
    parts = urllib.parse.urlsplit(u)
    path = parts.path.rstrip("/") or "/"
    return f"{parts.scheme}://{parts.netloc.lower()}{path}"


def fetch_url_of(chk):
    m = chk["method"]
    if m == "github-commit":
        return f"https://api.github.com/repos/{chk['repo']}/commits"
    if m == "github-release":
        return f"https://api.github.com/repos/{chk['repo']}/releases/latest"
    return chk.get("url")


# --------------------------------------------------------------------------- lint

ELEM_ROW = re.compile(r"^\|\s*(?:<a id=\"[^\"]+\"></a>)?([A-Z][A-Z0-9]*-\d+)\s*(\(retired\))?\s*\|")
ELEM_ID = re.compile(r"\b([A-Z][A-Z0-9]*)-(\d+)\b")
RANGE = re.compile(r"\b([A-Z][A-Z0-9]*)-(\d+)\s*(?:…|\.\.\.|–|—|\bto\b)\s*(?:\1-)?(\d+)\b")


def standards_elements(std_dir):
    elems = {}
    for f in sorted(std_dir.glob("*.md")):
        if f.name == "MAINTENANCE.md":
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            m = ELEM_ROW.match(line)
            if m:
                elems[m.group(1)] = (f.name, bool(re.search(r"\(retired\b", line)))
    return elems


def checklist_ids(checklist):
    text = checklist.read_text(encoding="utf-8")
    ids = set()
    for m in RANGE.finditer(text):
        pre, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        width = len(m.group(2))
        for n in range(a, b + 1):
            ids.add(f"{pre}-{n:0{width}d}")
    for m in ELEM_ID.finditer(text):
        ids.add(f"{m.group(1)}-{m.group(2)}")
    return ids


def lint(names):
    allow = approved_urls()
    errors, warnings = [], []
    for d in skill_dirs(names):
        skill = d.name
        std = d / "references" / "standards"
        if not std.is_dir():
            warnings.append(f"{skill}: no references/standards/ folder")
            continue
        data, path = load_manifest(d)
        if data is None:
            errors.append(f"{skill}: missing {path.relative_to(ROOT)}")
            continue
        covered = set()
        seen = set()
        for i, chk in enumerate(data.get("checks", [])):
            where = f"{skill}: check {chk.get('id', i)}"
            cid = chk.get("id")
            if not cid:
                errors.append(f"{where}: missing id")
            elif cid in seen:
                errors.append(f"{where}: duplicate id")
            seen.add(cid)
            m = chk.get("method")
            if m not in METHODS:
                errors.append(f"{where}: unknown method {m!r}")
                continue
            for k in METHODS[m]["required"]:
                if k not in chk:
                    errors.append(f"{where}: missing field {k!r}")
            files = chk.get("file")
            files = [files] if isinstance(files, str) else (files or [])
            for fn in files:
                fp = std / fn
                if not fp.exists():
                    errors.append(f"{where}: file {fn} not found")
                    continue
                covered.add(fn)
                if chk.get("baseline"):
                    continue  # pins recorded by this script, not copied from the header
                text = fp.read_text(encoding="utf-8")
                for k in METHODS[m]["pins"]:
                    v = chk.get(k)
                    if v is None or v == "":
                        continue
                    if str(v) not in text:
                        errors.append(f"{where}: pinned {k}={v!r} not found in {fn} (manifest and header disagree)")
            u = fetch_url_of(chk)
            if m != "manual" and u and _norm(u) not in allow:
                errors.append(f"{where}: URL not in approved-sources.md: {_norm(u)}")
            if m in BASELINE_FIELDS and all(chk.get(k) in (None, "") for k in BASELINE_FIELDS[m]):
                warnings.append(f"{where}: no baseline yet (run `check --record-baselines`)")
        unpinned = data.get("unpinned", {})
        for f in sorted(std.glob("*.md")):
            if f.name == "MAINTENANCE.md" or f.name in covered or f.name in unpinned:
                continue
            errors.append(f"{skill}: {f.name} has no pins.json check and isn't listed under 'unpinned'")
        # element-to-checklist mapping
        checklist = d / "references" / "checklist.md"
        if checklist.exists():
            ignore = tuple(data.get("lint", {}).get("elementsNotInChecklist", []))
            listed = checklist_ids(checklist)
            for eid, (fn, retired) in standards_elements(std).items():
                if retired or (ignore and eid.startswith(ignore)):
                    continue
                if eid not in listed:
                    warnings.append(f"{skill}: element {eid} ({fn}) isn't listed in checklist.md")
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    print(json.dumps({"ok": not errors, "errors": len(errors), "warnings": len(warnings)}))
    return 1 if errors else 0


# --------------------------------------------------------------------------- fetching

class Fetcher:
    def __init__(self, allow):
        self.allow = allow
        self.cache = {}
        self.gh_blocked = None
        self.token = os.environ.get("GITHUB_TOKEN")

    def get(self, url, accept=None):
        if _norm(url) not in self.allow:
            raise PermissionError(f"not in approved-sources.md: {_norm(url)}")
        if url in self.cache:
            return self.cache[url]
        headers = {"User-Agent": USER_AGENT}
        if accept:
            headers["Accept"] = accept
        is_gh = url.startswith("https://api.github.com/")
        if is_gh:
            if self.gh_blocked:
                raise RuntimeError(self.gh_blocked)
            if self.token:
                headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                body = r.read().decode("utf-8", "replace")
                res = (r.status, r.geturl(), body)
        except urllib.error.HTTPError as e:
            if is_gh and e.code in (403, 429) and e.headers.get("X-RateLimit-Remaining") == "0":
                self.gh_blocked = "GitHub API rate limit reached; set GITHUB_TOKEN and re-run"
                raise RuntimeError(self.gh_blocked)
            res = (e.code, url, "")
        self.cache[url] = res
        return res


def _meta(body, name):
    m = re.search(r'<meta[^>]+name="' + re.escape(name) + r'"[^>]*content="([^"]*)"', body)
    if not m:
        m = re.search(r'<meta[^>]+content="([^"]*)"[^>]*name="' + re.escape(name) + r'"', body)
    return m.group(1) if m else None


def _strip(fragment):
    fragment = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", fragment)
    text = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.sub(r"\s+", " ", text).strip()


def _sha16(text, n=16):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def text_hash(body, chk):
    if chk.get("extract") == "ids":
        ids = sorted(set(re.findall(r'\bid\s*=\s*"([^"]+)"', body)))
        return _sha16("\n".join(ids), chk.get("hashLength", 16))
    s_marker, e_marker = chk.get("startMarker"), chk.get("endMarker")
    if s_marker:
        s = body.find(s_marker)
        e = body.find(e_marker, s) if e_marker else -1
        if s < 0 or (e_marker and e < 0):
            raise ValueError("hash markers not found on the page")
        frag = body[body.rfind("<", 0, s): body.rfind("<", 0, e) if e_marker else len(body)]
    else:
        frag = body
    return _sha16(_strip(frag), chk.get("hashLength", 16))


def json_select(obj, path):
    """Tiny path language: a.b[*].c, a[k=v].c, a[0], trailing {x,y} projection."""
    proj = None
    m = re.search(r"\{([^}]*)\}$", path)
    if m:
        proj = [p.strip() for p in m.group(1).split(",")]
        path = path[: m.start()].rstrip(".")
    cur, many = obj, False
    for tok in [t for t in path.split(".") if t]:
        tm = re.fullmatch(r"([^\[\]]+)?(?:\[([^\]]+)\])?", tok)
        key, filt = tm.group(1), tm.group(2)

        def step(o):
            v = o.get(key) if key and isinstance(o, dict) else o
            if filt is None:
                return v, False
            if filt == "*":
                return v, True
            if filt.isdigit():
                return v[int(filt)], False
            fk, fv = filt.split("=", 1)
            return [x for x in v if str(x.get(fk)).lower() == fv.lower()], True

        if many:
            nxt = []
            for o in cur:
                v, is_list = step(o)
                nxt.extend(v if is_list else [v])
            cur = nxt
        else:
            cur, many = step(cur)
    if proj is not None:
        cur = [{k: o.get(k) for k in proj} for o in cur] if many else {k: cur.get(k) for k in proj}
    if many and isinstance(cur, list) and len(cur) == 1 and proj is None:
        cur = cur[0]
    return cur


def _same_sha(a, b):
    a, b = (a or "").lower(), (b or "").lower()
    return bool(a and b) and (a.startswith(b) or b.startswith(a))


def run_check(chk, f):
    m = chk["method"]
    res = {"status": "unchanged", "current": None, "detail": ""}
    if m == "manual":
        res.update(status="manual", detail=chk["note"])
        return res
    if m == "github-commit":
        q = {"per_page": "1"}
        if chk.get("path"):
            q["path"] = chk["path"]
        if chk.get("ref"):
            q["sha"] = chk["ref"]
        url = f"https://api.github.com/repos/{chk['repo']}/commits?" + urllib.parse.urlencode(q)
        status, _, body = f.get(url, "application/vnd.github+json")
        if status != 200:
            raise RuntimeError(f"HTTP {status}")
        data = json.loads(body)
        if not data:
            raise RuntimeError("no commits returned (path moved or deleted?)")
        sha = data[0]["sha"]
        date = data[0]["commit"]["committer"]["date"][:10]
        res["current"] = f"{sha[:12]} ({date})"
        if _same_sha(sha, chk["pinned"]):
            return res
        pdate = chk.get("pinnedDate")
        if pdate and date <= pdate:
            res["detail"] = "latest change to this path is not after the pin date"
            return res
        res.update(status="changed", detail=f"pinned {chk['pinned'][:12]} ({pdate or '?'})")
        return res
    if m == "github-release":
        status, _, body = f.get(f"https://api.github.com/repos/{chk['repo']}/releases/latest", "application/vnd.github+json")
        if status != 200:
            raise RuntimeError(f"HTTP {status}")
        tag = json.loads(body)["tag_name"]
        res["current"] = tag
        if tag != chk["pinned"]:
            res.update(status="changed", detail=f"pinned {chk['pinned']}")
        return res

    status, final, body = f.get(chk["url"])
    if m == "http-status":
        res["current"] = status
        if status != int(chk["pinned"]):
            res.update(status="changed", detail=f"expected HTTP {chk['pinned']}")
        return res
    if status != 200:
        raise RuntimeError(f"HTTP {status}")
    if m == "redirect":
        res["current"] = final
        if chk["expect"] not in final:
            res.update(status="changed", detail=f"expected the final URL to contain {chk['expect']!r}")
        return res
    if m == "learn-page":
        cur_date = (_meta(body, "ms.date") or "")[:10]
        cur_commit = _meta(body, "git_commit_id") or ""
        res["current"] = {"msDate": cur_date, "gitCommit": cur_commit[:12]}
        diffs = []
        if chk.get("msDate") and cur_date != chk["msDate"]:
            diffs.append(f"ms.date {chk['msDate']} -> {cur_date}")
        if chk.get("gitCommit") and not _same_sha(cur_commit, chk["gitCommit"]):
            diffs.append(f"git_commit_id {chk['gitCommit'][:12]} -> {cur_commit[:12]}")
        req_path = urllib.parse.urlsplit(chk["url"]).path.rstrip("/")
        fin_path = re.sub(r"^/[a-z]{2}-[a-z]{2}(?=/)", "", urllib.parse.urlsplit(final).path).rstrip("/")
        if fin_path.lower() != req_path.lower():
            diffs.append(f"moved to {final}")
        if not chk.get("msDate") and not chk.get("gitCommit"):
            res.update(status="no-baseline")
        if diffs:
            res.update(status="changed", detail="; ".join(diffs))
        return res
    if m == "regex":
        mm = re.search(chk["pattern"], body, re.S)
        if not mm:
            raise RuntimeError("pattern not found on the page")
        cur = mm.group(1)
        res["current"] = cur
        if cur != str(chk["pinned"]):
            res.update(status="changed", detail=f"pinned {chk['pinned']}")
        return res
    if m == "json":
        val = json_select(json.loads(body), chk["select"])
        if chk.get("first") and isinstance(val, list):
            val = val[0] if val else None
        cur = _sha16(json.dumps(val, sort_keys=True, separators=(",", ":"))) if chk.get("hash") else val
        res["current"] = cur
        if chk.get("pinned") in (None, ""):
            res.update(status="no-baseline")
        elif str(cur) != str(chk["pinned"]):
            res.update(status="changed", detail=f"pinned {chk['pinned']}")
        return res
    if m == "text-hash":
        cur = text_hash(body, chk)
        res["current"] = cur
        if chk.get("pinned") in (None, ""):
            res.update(status="no-baseline")
        elif cur != chk["pinned"]:
            res.update(status="changed", detail=f"pinned {chk['pinned']}")
        return res
    raise RuntimeError(f"unsupported method {m}")


def check(names, as_json, md_out, record, methods=None):
    f = Fetcher(approved_urls())
    results = []
    today = _dt.date.today().isoformat()
    for d in skill_dirs(names):
        data, path = load_manifest(d)
        if data is None:
            results.append({"skill": d.name, "id": "-", "status": "error", "detail": "no pins.json"})
            continue
        dirty = False
        for chk in data.get("checks", []):
            if methods and chk["method"] not in methods:
                continue
            row = {"skill": d.name, "id": chk["id"], "method": chk["method"], "file": chk.get("file"),
                   "watch": bool(chk.get("watch"))}
            try:
                row.update(run_check(chk, f))
            except Exception as e:  # noqa: BLE001 - report every failure, keep going
                row.update(status="error", detail=f"{type(e).__name__}: {e}")
            if record and row["status"] == "no-baseline":
                cur = row["current"]
                if chk["method"] == "learn-page":
                    chk["msDate"], chk["gitCommit"] = cur["msDate"], cur["gitCommit"]
                else:
                    chk["pinned"] = cur
                chk["baseline"] = today
                row.update(status="recorded", detail=f"baseline recorded {today}")
                dirty = True
            if chk.get("note") and chk["method"] != "manual":
                row["note"] = chk["note"]
            results.append(row)
            if not as_json:
                print(f"{row['status']:<11} {d.name:<34} {chk['id']:<28} {row.get('detail') or row.get('current') or ''}",
                      flush=True)
        if dirty:
            save_manifest(path, data)
    summary = {}
    for r in results:
        summary[r["status"]] = summary.get(r["status"], 0) + 1
    out = {"date": today, "summary": summary, "results": results}
    if as_json:
        print(json.dumps(out, indent=2, default=str))
    else:
        print(json.dumps({"summary": summary}))
    if md_out:
        write_md(out, pathlib.Path(md_out))
    if summary.get("changed"):
        return 1
    return 2 if summary.get("error") else 0


def write_md(out, path):
    lines = [f"# Source drift report — {out['date']}", "",
             "Generated by `compliance-reviewer/scripts/check_source_drift.py check`. Maintainers only.", "",
             "Summary: " + ", ".join(f"{k} {v}" for k, v in sorted(out["summary"].items())), ""]
    for status in ("changed", "error", "no-baseline", "recorded", "manual"):
        rows = [r for r in out["results"] if r["status"] == status]
        if not rows:
            continue
        lines += [f"## {status} ({len(rows)})", "", "| Skill | Check | File | Detail | Current |", "|---|---|---|---|---|"]
        for r in rows:
            cur = r.get("current")
            cur = json.dumps(cur) if isinstance(cur, (dict, list)) else (cur or "")
            fl = r.get("file")
            fl = ", ".join(fl) if isinstance(fl, list) else (fl or "")
            det = (r.get("detail") or "") + (" (watch item)" if r.get("watch") else "")
            lines.append(f"| {r['skill']} | {r['id']} | {fl} | {det.replace('|', '/')} | {str(cur).replace('|', '/')} |")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {path}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_l = sub.add_parser("lint", help="offline consistency checks")
    p_l.add_argument("skills", nargs="*")
    p_c = sub.add_parser("check", help="fetch sources and report drift")
    p_c.add_argument("skills", nargs="*")
    p_c.add_argument("--json", action="store_true", help="print the full result as JSON")
    p_c.add_argument("--md", metavar="FILE", help="also write a Markdown report (keep it outside the repo or in a scratch folder)")
    p_c.add_argument("--record-baselines", action="store_true", help="store current values for checks without a baseline")
    p_c.add_argument("--method", action="append", choices=sorted(METHODS), help="only run checks of this method (repeatable)")
    a = ap.parse_args(argv)
    if a.cmd == "lint":
        return lint(a.skills)
    return check(a.skills, a.json, a.md, a.record_baselines, a.method)


if __name__ == "__main__":
    sys.exit(main())
