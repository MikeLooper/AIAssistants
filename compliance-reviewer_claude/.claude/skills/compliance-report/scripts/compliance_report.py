#!/usr/bin/env python3
"""Deterministic validate, aggregate (step 90) and render (step 99) for compliance review runs.

Usage:
  compliance_report.py validate  <runDir>
  compliance_report.py aggregate <runDir>
  compliance_report.py render    <runDir> --out docs/reports/<name>.md

Standard library only. Reads the per-subject transition files in <runDir>
(NN-review-*.json, optionally NN-review-*.part-K.json from older runs).
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

SEV_WEIGHT = {"Error": 5, "Warning": 2, "Information": 1}
SEV_RANK = {"Error": 0, "Warning": 1, "Information": 2}
CONF_RANK = {"High": 0, "Medium": 1, "Low": 2}
EFFORT_RANK = {"Small": 0, "Medium": 1, "Large": 2}
RESULTS = {"pass", "fail", "N/A"}
FILE_RE = re.compile(r"^(\d\d)-(review-[a-z0-9-]+?)(?:\.part-(\d+))?\.json$")
HEADER_KEYS = ["schemaVersion", "runId", "stepId", "status", "startedAt", "completedAt",
               "targetPath", "targetGitHead", "inputsHash"]


def read_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def subject_files(run_dir):
    out = []
    for name in sorted(os.listdir(run_dir)):
        m = FILE_RE.match(name)
        if m:
            out.append((int(m.group(1)), m.group(2), int(m.group(3) or 0), name))
    return out


def band(score):
    if score is None:
        return "N/A"
    return "Excellent" if score >= 90 else "Good" if score >= 75 else "Fair" if score >= 60 else "Poor"


# ---------------------------------------------------------------- validate

def validate(run_dir):
    problems, warnings = [], []
    state_path = os.path.join(run_dir, "state.json")
    state = read_json(state_path) if os.path.exists(state_path) else {}
    if not state:
        problems.append({"file": "state.json", "problem": "missing"})
    found = set()
    for _step, skill, _part, name in subject_files(run_dir):
        found.add(skill)
        try:
            d = read_json(os.path.join(run_dir, name))
        except Exception as e:  # noqa: BLE001
            problems.append({"file": name, "problem": f"invalid JSON: {e}"})
            continue
        for k in HEADER_KEYS:
            if k not in d:
                problems.append({"file": name, "problem": f"missing header field {k}"})
        if d.get("status") != "completed":
            problems.append({"file": name, "problem": f"status is {d.get('status')!r}, expected 'completed'"})
        if d.get("skill") != skill:
            problems.append({"file": name, "problem": f"skill field {d.get('skill')!r} does not match file name"})
        for k in ("subject", "findings", "strengths", "checkResults"):
            if k not in d:
                problems.append({"file": name, "problem": f"missing {k}"})
        ids = set()
        for f in d.get("findings", []):
            if f.get("severity") not in SEV_WEIGHT:
                problems.append({"file": name, "problem": f"finding {f.get('id')} has invalid severity"})
            if not f.get("evidence"):
                problems.append({"file": name, "problem": f"finding {f.get('id')} has no evidence"})
            if f.get("id") in ids:
                problems.append({"file": name, "problem": f"duplicate finding id {f.get('id')}"})
            ids.add(f.get("id"))
        for c in d.get("checkResults", []):
            if c.get("result") not in RESULTS:
                problems.append({"file": name, "problem": f"check {c.get('checkId')} has invalid result"})
            elif c["result"] != "N/A" and c.get("severityIfFailed") not in SEV_WEIGHT:
                problems.append({"file": name, "problem": f"check {c.get('checkId')} has invalid severityIfFailed"})
            if c.get("result") == "fail":
                missing = [i for i in c.get("findingIds", []) if i not in ids]
                if not c.get("findingIds"):
                    warnings.append({"file": name, "problem": f"failed check {c.get('checkId')} has no findingIds"})
                elif missing:
                    problems.append({"file": name, "problem": f"check {c.get('checkId')} references unknown finding {missing}"})
        if len(d.get("strengths", [])) > 3:
            warnings.append({"file": name, "problem": f"{len(d['strengths'])} strengths (cap is 3)"})
    missing_skills = [s for s in state.get("subjects", []) if s not in found]
    ok = not problems and not missing_skills
    print(json.dumps({"ok": ok, "missing": missing_skills, "problems": problems, "warnings": warnings}, indent=2))
    return 0 if ok else 1


# ---------------------------------------------------------------- loading

def load_results(run_dir):
    """Per-skill merged results, in pipeline order. Merges .part-K files of older runs."""
    by_skill = {}
    for step, skill, part, name in subject_files(run_dir):
        d = read_json(os.path.join(run_dir, name))
        cur = by_skill.get(skill)
        if cur is None:
            cur = by_skill[skill] = {"skill": skill, "step": step, "subject": d.get("subject", skill),
                                     "findings": [], "strengths": [], "checkResults": {}, "urlsFetched": []}
        remap = {}
        existing = {f["id"] for f in cur["findings"]}
        for f in d.get("findings", []):
            if f["id"] in existing:
                new_id = f"{f['id']}~{part or len(existing)}"
                remap[f["id"]] = new_id
                f = dict(f, id=new_id)
            existing.add(f["id"])
            cur["findings"].append(f)
        cur["strengths"] += d.get("strengths", [])
        cur["urlsFetched"] += d.get("urlsFetched", [])
        for c in d.get("checkResults", []):
            c = dict(c, findingIds=[remap.get(i, i) for i in c.get("findingIds", [])])
            key = (c.get("subSubject", ""), c["checkId"])
            old = cur["checkResults"].get(key)
            if old is None:
                cur["checkResults"][key] = c
            else:  # a check seen in several parts: fail beats pass beats N/A
                rank = {"fail": 0, "pass": 1, "N/A": 2}
                keep = c if rank[c["result"]] < rank[old["result"]] else old
                keep["findingIds"] = sorted(set(old.get("findingIds", [])) | set(c.get("findingIds", [])))
                cur["checkResults"][key] = keep
    return sorted(by_skill.values(), key=lambda r: r["step"])


# ---------------------------------------------------------------- aggregate

def norm_file(p):
    return (p or "").replace("\\", "/").lower()


def overlaps(a, b):
    """Same real file and near-identical location (line ranges with IoU >= 0.5, or both whole-file)."""
    fa, fb = norm_file(a.get("file")), norm_file(b.get("file"))
    if not fa or fa != fb:
        return False
    a1, b1 = a.get("lineStart") or None, b.get("lineStart") or None
    if a1 is None or b1 is None:
        return a1 is None and b1 is None
    a2, b2 = a.get("lineEnd") or a1, b.get("lineEnd") or b1
    inter = min(a2, b2) - max(a1, b1) + 1
    return inter > 0 and inter / (max(a2, b2) - min(a1, b1) + 1) >= 0.5

def any_overlap(f, g):
    return any(overlaps(x, y) for x in f["evidence"] for y in g["evidence"])


def aggregate(run_dir):
    state = read_json(os.path.join(run_dir, "state.json"))
    results = load_results(run_dir)
    if not results:
        print("no subject transition files found", file=sys.stderr)
        return 1

    # 1. exact duplicates: same checkId + subject + subSubject with overlapping evidence
    order = 0
    findings = []
    for r in results:
        for f in r["findings"]:
            f = dict(f, _skill=r["skill"], _step=r["step"], _ord=order)
            order += 1
            for g in findings:
                same = (g["checkId"], g["subject"], g.get("subSubject")) == (f["checkId"], f["subject"], f.get("subSubject"))
                if same and any_overlap(f, g):
                    g["evidence"] += [e for e in f["evidence"] if not any(overlaps(e, x) for x in g["evidence"])]
                    if SEV_RANK[f["severity"]] < SEV_RANK[g["severity"]]:
                        g["severity"] = f["severity"]
                    f = None
                    break
            if f is not None:
                findings.append(f)

    # 2. cross-subject semantic duplicates: the strongest finding is the primary
    findings.sort(key=lambda f: (SEV_RANK[f["severity"]], f["_step"], f["_ord"]))
    primaries, suppressed, suppressed_checks = [], [], []
    for f in findings:
        primary = next((p for p in primaries
                        if (p["checkId"], p["subject"]) != (f["checkId"], f["subject"]) and any_overlap(f, p)), None)
        if primary is None:
            primaries.append(f)
            continue
        where = f"{primary['subject']}/{primary.get('subSubject', '')}"
        suppressed.append({"suppressedId": f["id"], "primaryId": primary["id"],
                           "reason": f"overlapping evidence; {primary['severity']} finding in {where} outranks or precedes {f['severity']} in {f['subject']}/{f.get('subSubject', '')}"})
        suppressed_checks.append({"skill": f["_skill"], "checkId": f["checkId"], "subSubject": f.get("subSubject", ""),
                                  "findingId": f["id"], "primaryId": primary["id"], "primarySubject": where})
    primaries.sort(key=lambda f: f["_ord"])

    # 3. scoring from checkResults (suppressed duplicates still count as fail)
    subj = {}
    for r in results:
        s = subj.setdefault(r["subject"], {"subject": r["subject"], "step": r["step"], "pass": 0, "total": 0})
        for c in r["checkResults"].values():
            if c["result"] == "N/A":
                continue
            w = SEV_WEIGHT[c["severityIfFailed"]]
            s["total"] += w
            if c["result"] == "pass":
                s["pass"] += w
    counts = {"Error": 0, "Warning": 0, "Information": 0}
    for f in primaries:
        counts[f["severity"]] += 1
    scores = []
    for s in sorted(subj.values(), key=lambda s: s["step"]):
        score = round(s["pass"] / s["total"] * 100, 2) if s["total"] else None
        per = {k: sum(1 for f in primaries if f["subject"] == s["subject"] and f["severity"] == k) for k in counts}
        scores.append({"subject": s["subject"], "score": score, "band": band(score),
                       "passWeight": s["pass"], "totalWeight": s["total"], "findings": per})
    tot_pass = sum(s["passWeight"] for s in scores)
    tot = sum(s["totalWeight"] for s in scores)
    overall = round(tot_pass / tot * 100, 2) if tot else None

    top = sorted(primaries, key=lambda f: (SEV_RANK[f["severity"]], CONF_RANK.get(f.get("confidence"), 3),
                                           EFFORT_RANK.get(f.get("effort"), 3), f["_step"], f["_ord"]))[:5]
    clean = [{k: v for k, v in f.items() if not k.startswith("_")} for f in primaries]
    agg = {
        "schemaVersion": 1, "runId": state["runId"], "stepId": "90-aggregate", "status": "completed",
        "startedAt": now_iso(), "completedAt": now_iso(), "targetPath": state.get("targetPath"),
        "targetGitHead": state.get("targetGitHead"), "inputsHash": state.get("inputsHash"),
        "overallScore": overall, "overallBand": band(overall), "subjectScores": scores,
        "severityCounts": counts,
        "topRisks": [{"rank": i + 1, "findingId": f["id"], "severity": f["severity"], "title": f["title"]}
                     for i, f in enumerate(top)],
        "findings": clean, "strengths": [s for r in results for s in r["strengths"]],
        "duplicatesSuppressed": suppressed, "suppressedChecks": suppressed_checks,
        "notes": "checkResults are not embedded; render reads them from the per-subject transition files and applies suppressedChecks.",
    }
    write_json(os.path.join(run_dir, "90-aggregate.json"), agg)
    state.setdefault("steps", {})["90-aggregate"] = "completed"
    state["updatedAt"] = now_iso()
    write_json(os.path.join(run_dir, "state.json"), state)
    print(f"aggregate: overall {overall}/100 {band(overall)}; Error {counts['Error']}, Warning {counts['Warning']}, "
          f"Information {counts['Information']}; {len(suppressed)} duplicate(s) suppressed")
    return 0


# ---------------------------------------------------------------- render

def cell(text):
    return re.sub(r"\s+", " ", str(text or "")).replace("|", "\\|").strip()


def lookup(stack, name):
    for ctx in reversed(stack):
        if isinstance(ctx, dict) and name in ctx:
            return ctx[name]
    return ""


def render_template(tpl, stack):
    def section(m):
        val = lookup(stack, m.group(1))
        if isinstance(val, list):
            return "".join(render_template(m.group(2), stack + [item]) for item in val)
        return render_template(m.group(2), stack + [val]) if val else ""
    tpl = re.sub(r"\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}", section, tpl, flags=re.S)
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(lookup(stack, m.group(1))), tpl)


def render(run_dir, out_path):
    state = read_json(os.path.join(run_dir, "state.json"))
    agg = read_json(os.path.join(run_dir, "90-aggregate.json"))
    inv_path = os.path.join(run_dir, "01-inventory.json")
    inv = read_json(inv_path) if os.path.exists(inv_path) else {}
    results = load_results(run_dir)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "assets", "report-template.md"), encoding="utf-8") as f:
        tpl = f.read()
    # section tags alone on a line must not leave blank lines behind
    tpl = re.sub(r"^[ \t]*(\{\{[#/]\w+\}\})[ \t]*\r?\n", r"\1", tpl, flags=re.M)

    by_id = {f["id"]: f for f in agg["findings"]}
    titles = {(r["skill"], f["id"]): f["title"] for r in results for f in r["findings"]}
    sup = {(s["skill"], s["checkId"], s["subSubject"]): s for s in agg["suppressedChecks"]}

    def finding_row(f):
        ev = f["evidence"][0] if f.get("evidence") else {}
        extra = f" (+{len(f['evidence']) - 1} more)" if len(f.get("evidence", [])) > 1 else ""
        return {"severity": f["severity"], "title": f["title"], "subject": f["subject"],
                "subSubject": f.get("subSubject", ""), "file": f"{ev.get('file', '')}{extra}",
                "lineStart": ev.get("lineStart", ""), "lineEnd": ev.get("lineEnd", ""),
                "recommendation": f.get("recommendation", ""), "standard": f.get("standard", ""), "url": f.get("url", "")}

    subjects = {}
    for r in results:
        subs = subjects.setdefault(r["subject"], {"name": r["subject"], "subSubjects": {}})
        for (sub, cid), c in r["checkResults"].items():
            s = sup.get((r["skill"], cid, sub))
            result, reason, ids = c["result"], c.get("reason", ""), c.get("findingIds", [])
            if s:
                reason = f"duplicate evidence of {s['primaryId']}, see {s['primarySubject']}"
            elif result == "fail" and not reason and ids:
                reason = titles.get((r["skill"], ids[0]), ids[0])
            group = subs["subSubjects"].setdefault(sub or r["subject"], {"subSubject": sub or r["subject"], "checks": []})
            group["checks"].append({"checkId": cid, "result": result,
                                    "evidenceOrReason": cell(reason) if result != "pass" else ""})
    subjects_ctx = [{"name": s["name"], "subSubjects": list(s["subSubjects"].values())} for s in subjects.values()]

    strengths = {}
    for s in agg["strengths"]:
        ev = (s.get("evidence") or [{}])[0]
        strengths.setdefault(s["subject"], {"subject": s["subject"], "strengths": []})["strengths"].append(
            {"subSubject": s.get("subSubject", ""), "title": s["title"], "file": ev.get("file", "")})

    def by_sev(k):
        return [finding_row(f) for f in agg["findings"] if f["severity"] == k]

    urls = sorted({u for r in results for u in r["urlsFetched"]})
    skipped = inv.get("skippedSubjects", {})
    init_path = os.path.join(run_dir, "00-init.json")
    started = state.get("startedAt") or (read_json(init_path).get("startedAt") if os.path.exists(init_path) else "")
    ctx = {
        "targetName": os.path.basename(str(state.get("targetPath", "")).rstrip("\\/")) or "target",
        "generatedAt": now_iso(), "runId": state["runId"],
        "overallScore": f"{agg['overallScore']:.2f}", "overallBand": agg["overallBand"],
        "subjectScores": [{"subject": s["subject"], "score": f"{s['score']:.2f}", "band": s["band"]}
                          for s in agg["subjectScores"] if s["score"] is not None],
        "errorCount": agg["severityCounts"]["Error"], "warningCount": agg["severityCounts"]["Warning"],
        "infoCount": agg["severityCounts"]["Information"],
        "topRisks": [finding_row(by_id[t["findingId"]]) for t in agg["topRisks"]],
        "strengthsBySubject": list(strengths.values()),
        "errorFindings": by_sev("Error"), "warningFindings": by_sev("Warning"), "infoFindings": by_sev("Information"),
        "subjects": subjects_ctx,
        "targetPath": state.get("targetPath", ""), "targetGitHead": state.get("targetGitHead") or "n/a",
        "startedAt": started, "completedAt": now_iso(),
        "skippedSubjects": "; ".join(f"{k} ({v})" for k, v in skipped.items()) or "none",
        "urlsFetched": ", ".join(urls) or "none",
        "linkApprovals": json.dumps(state["linkApprovals"]) if state.get("linkApprovals") else "none",
    }
    report = re.sub(r"\n{3,}", "\n\n", render_template(tpl, [ctx]))
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(report)

    write_json(os.path.join(run_dir, "99-report.json"), {
        "schemaVersion": 1, "runId": state["runId"], "stepId": "99-report", "status": "completed",
        "startedAt": now_iso(), "completedAt": now_iso(), "targetPath": state.get("targetPath"),
        "targetGitHead": state.get("targetGitHead"), "inputsHash": state.get("inputsHash"),
        "reportPath": out_path.replace("\\", "/")})
    state.setdefault("steps", {})["99-report"] = "completed"
    state.update({"status": "completed", "reportPath": out_path.replace("\\", "/"), "updatedAt": now_iso()})
    write_json(os.path.join(run_dir, "state.json"), state)
    print(f"report: {out_path}")
    print(f"overall {agg['overallScore']}/100 {agg['overallBand']}")
    for t in agg["topRisks"]:
        print(f"  {t['rank']}. [{t['severity']}] {t['title']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["validate", "aggregate", "render"])
    ap.add_argument("run_dir")
    ap.add_argument("--out", help="report path (render only)")
    a = ap.parse_args()
    if a.command == "validate":
        return validate(a.run_dir)
    if a.command == "aggregate":
        return aggregate(a.run_dir)
    if not a.out:
        ap.error("render requires --out")
    return render(a.run_dir, a.out)


if __name__ == "__main__":
    sys.exit(main())
