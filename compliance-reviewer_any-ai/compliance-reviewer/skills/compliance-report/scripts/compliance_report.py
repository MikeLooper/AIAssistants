#!/usr/bin/env python3
"""Deterministic validate, aggregate (step 90) and render (step 99) for compliance review runs.

Usage:
  compliance_report.py validate  <runDir>
  compliance_report.py aggregate <runDir>
  compliance_report.py render    <runDir> --out docs/reports/<name>.md
  compliance_report.py labels    [skill ...]

Standard library only. Reads the per-subject transition files in <runDir>
(NN-review-*.json, optionally NN-review-*.part-K.json from older runs).

Subject and sub-subject labels are owned by each skill's references/checklist.md
(`Subject:` line and `Sub-subject` column). validate warns on drift, aggregate and
render rewrite every label from the checklist, and `labels` lints the checklists.
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


# ---------------------------------------------------------------- checklist labels

SKILLS_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TRANSITION_SCHEMA = os.path.join(SKILLS_DIR, "compliance-review-core", "references", "transition-schema.md")
PLACEHOLDER_CHECK = "N/A"                       # checkId of an orchestrator-written N/A subject file
NO_LABEL = {"", "—", "-", "–"}
LABEL_MAX = 36                                  # D-2: "at most about 32 characters"
SMALL_WORDS = {"a", "an", "the", "of", "for", "in", "on", "to", "or", "by", "with", "vs"}
TITLE_CASE_EXEMPT = {"review-twelve-factor"}    # keeps the source's own factor titles (D-2)
RANGE_RE = re.compile(r"^(.*?)(\d+)\s*…\s*(\d+)$")  # e.g. CS-CS-01…05
_CHECKLISTS = {}


def split_row(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def expand_ids(cell):
    """`CS-CS-01…05` -> CS-CS-01 … CS-CS-05; anything else is a single id."""
    m = RANGE_RE.match(cell)
    if not m:
        return [cell]
    prefix, a, b = m.group(1), m.group(2), m.group(3)
    return [f"{prefix}{i:0{len(a)}d}" for i in range(int(a), int(b) + 1)]


def label_style(label, skill):
    """D-2 problems with one label (empty list when fine)."""
    out = []
    if label in NO_LABEL:
        return ["empty label"]
    if " / " in label or label.startswith("/") or label.endswith("/"):
        out.append("contains the ' / ' separator")
    if len(label) > LABEL_MAX:
        out.append(f"longer than {LABEL_MAX} characters")
    if skill not in TITLE_CASE_EXEMPT:
        if re.search(r"\band\b", label):
            out.append("uses 'and' instead of '&'")
        words = label.split()
        bad = [w for i, w in enumerate(words)
               if w[:1].isalpha() and w[:1].islower() and (i == 0 or w.lower() not in SMALL_WORDS)]
        if bad:
            out.append(f"not Title Case ({', '.join(bad)})")
    return out


def load_checklist(skill):
    """{subject, checks: {checkId: subSubject}, retired: set, subSubjects: [...], problems: [...]} or None."""
    if skill in _CHECKLISTS:
        return _CHECKLISTS[skill]
    path = os.path.join(SKILLS_DIR, skill, "references", "checklist.md")
    if not os.path.exists(path):
        _CHECKLISTS[skill] = None
        return None
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().splitlines()
    problems = []
    subjects = [l[len("Subject:"):].strip() for l in lines if l.startswith("Subject:")]
    if len(subjects) != 1:
        problems.append(f"expected exactly one 'Subject:' line, found {len(subjects)}")
    subject = subjects[0] if subjects else ""
    checks, retired, seen = {}, set(), set()
    start = next((i for i, l in enumerate(lines)
                  if l.lstrip().startswith("|") and "id" in [c.lower() for c in split_row(l)]), None)
    if start is None:
        problems.append("no checks table (a Markdown table whose header has an 'id' column)")
    else:
        cols = [c.lower() for c in split_row(lines[start])]
        ci = {name: cols.index(name) if name in cols else None for name in ("id", "sub-subject", "check")}
        for name, idx in ci.items():
            if idx is None:
                problems.append(f"checks table has no '{name}' column")
        if None not in ci.values():
            for n, line in enumerate(lines[start + 2:], start + 3):
                if not line.lstrip().startswith("|"):
                    stray = [m for m, l in enumerate(lines[n:], n + 1) if re.match(r"^\|\s*[A-Z][A-Z0-9-]*-\d+", l)]
                    if stray:
                        problems.append(f"line(s) {', '.join(map(str, stray))}: check row outside the checks table "
                                        "(a blank line or text breaks the table)")
                    break
                cells = split_row(line)
                if len(cells) < len(cols):
                    problems.append(f"line {n}: {len(cells)} cells, header has {len(cols)}")
                    continue
                is_retired = cells[ci["check"]].startswith("*(retired")
                for cid in expand_ids(cells[ci["id"]]):
                    if cid in seen:
                        problems.append(f"line {n}: duplicate id {cid}")
                    seen.add(cid)
                    if is_retired:
                        retired.add(cid)
                    else:
                        checks[cid] = cells[ci["sub-subject"]]
    subs = []
    for cid, sub in checks.items():
        if sub not in subs:
            subs.append(sub)
    _CHECKLISTS[skill] = {"subject": subject, "checks": checks, "retired": retired,
                          "subSubjects": subs, "problems": problems, "path": path}
    return _CHECKLISTS[skill]


def usable(cl):
    return cl is not None and not cl["problems"] and cl["subject"] and cl["checks"]


def canonical(cl, check_id, given_sub):
    """Canonical (subject, subSubject) for an entry of this skill; given_sub is kept when nothing better is known."""
    sub = cl["checks"].get(check_id)
    if sub is None:
        if len(cl["subSubjects"]) == 1:
            sub = cl["subSubjects"][0]
        elif check_id == PLACEHOLDER_CHECK:
            sub = cl["subject"]
        else:
            sub = given_sub or cl["subject"]
    return cl["subject"], sub


def normalize(d, skill):
    """Rewrite subject/subSubject from the checklist in place; drop retired check results. Returns #entries changed."""
    cl = load_checklist(skill)
    if not usable(cl):
        return 0
    changed = 0
    d["subject"] = cl["subject"]
    for kind in ("findings", "strengths", "checkResults"):
        for e in d.get(kind, []):
            subj, sub = canonical(cl, e.get("checkId"), e.get("subSubject"))
            if (e.get("subject"), e.get("subSubject")) != (subj, sub):
                changed += 1
                e["subject"], e["subSubject"] = subj, sub
    d["checkResults"] = [c for c in d.get("checkResults", []) if c.get("checkId") not in cl["retired"]]
    return changed


def label(subject, sub):
    """`subject / subSubject`, or the subject alone when the two are equal or there is no sub-subject."""
    return subject if not sub or sub == subject else f"{subject} / {sub}"


def step_skills():
    """Skill names from the step table in transition-schema.md."""
    if not os.path.exists(TRANSITION_SCHEMA):
        return []
    with open(TRANSITION_SCHEMA, encoding="utf-8-sig") as f:
        return re.findall(r"\|\s*\d\d\s*\|\s*(review-[a-z0-9-]+)\s*(?=\|)", f.read())


def labels_lint(skills):
    problems = []
    listed = step_skills()
    if not listed:
        problems.append({"file": os.path.relpath(TRANSITION_SCHEMA, SKILLS_DIR), "problem": "no step table found"})
    for skill in skills or listed:
        cl = load_checklist(skill)
        rel = f"{skill}/references/checklist.md"
        if cl is None:
            problems.append({"file": rel, "problem": "missing checklist"})
            continue
        problems += [{"file": rel, "problem": p} for p in cl["problems"]]
        if cl["subject"]:
            problems += [{"file": rel, "problem": f"Subject {cl['subject']!r}: {p}"}
                         for p in label_style(cl["subject"], skill)]
        if not cl["checks"]:
            problems.append({"file": rel, "problem": "no active checks"})
        for cid, sub in cl["checks"].items():
            problems += [{"file": rel, "problem": f"{cid} sub-subject {sub!r}: {p}"} for p in label_style(sub, skill)]
    ok = not problems
    print(json.dumps({"ok": ok, "problems": problems}, indent=2, ensure_ascii=False))
    return 0 if ok else 1


# ---------------------------------------------------------------- validate

def check_labels(d, skill):
    """D-4 checks of one subject file against its checklist: (problems, warnings)."""
    problems, warnings = [], []
    cl = load_checklist(skill)
    if not usable(cl):
        warnings.append(f"checklist for {skill} is missing or unreadable (run `labels`); labels not checked")
        return problems, warnings
    if d.get("subject") != cl["subject"]:
        warnings.append(f"subject {d.get('subject')!r} differs from checklist {cl['subject']!r} (normalized by aggregate)")
    drift = {}
    for kind in ("findings", "strengths", "checkResults"):
        for e in d.get(kind, []):
            cid = e.get("checkId")
            if kind == "strengths" and not cid:
                continue
            if cid in cl["retired"]:
                warnings.append(f"{kind} entry uses retired check {cid} (dropped from scoring)")
                continue
            if cid not in cl["checks"] and cid != PLACEHOLDER_CHECK:
                (warnings if kind == "strengths" else problems).append(f"{kind} entry has unknown checkId {cid!r}")
                continue
            want = canonical(cl, cid, e.get("subSubject"))
            have = (e.get("subject"), e.get("subSubject"))
            if have != want:
                drift.setdefault((have, want), []).append(cid)
    for (have, want), ids in drift.items():
        warnings.append(f"label {label(*have)!r} should be {label(*want)!r} for {', '.join(sorted(set(ids)))} "
                        "(normalized by aggregate)")
    results = d.get("checkResults", [])
    placeholder = any(c.get("checkId") == PLACEHOLDER_CHECK for c in results)
    if not placeholder:
        present = {c.get("checkId") for c in results}
        absent = [cid for cid in cl["checks"] if cid not in present]
        if absent:
            problems.append(f"no checkResults entry for active check(s) {', '.join(absent)}")
    return problems, warnings


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
        p, w = check_labels(d, skill)
        problems += [{"file": name, "problem": x} for x in p]
        warnings += [{"file": name, "problem": x} for x in w]
    missing_skills = [s for s in state.get("subjects", []) if s not in found]
    ok = not problems and not missing_skills
    print(json.dumps({"ok": ok, "missing": missing_skills, "problems": problems, "warnings": warnings}, indent=2))
    return 0 if ok else 1


# ---------------------------------------------------------------- loading

def load_results(run_dir):
    """Per-skill merged results, in pipeline order, with labels normalized from the checklists.

    Merges .part-K files of older runs. Retired check results are dropped.
    """
    by_skill = {}
    for step, skill, part, name in subject_files(run_dir):
        d = read_json(os.path.join(run_dir, name))
        changed = normalize(d, skill)
        cur = by_skill.get(skill)
        if cur is None:
            cur = by_skill[skill] = {"skill": skill, "step": step, "subject": d.get("subject", skill),
                                     "findings": [], "strengths": [], "checkResults": {}, "urlsFetched": [],
                                     "labelsNormalized": 0}
        cur["labelsNormalized"] += changed
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

    # 1. exact duplicates: same checkId + subject + subSubject + standard citation with overlapping evidence.
    #    Findings of one check that cite different standard elements are distinct violations and stay separate.
    order = 0
    findings = []
    for r in results:
        for f in r["findings"]:
            f = dict(f, _skill=r["skill"], _step=r["step"], _ord=order)
            order += 1
            for g in findings:
                key = lambda x: (x["checkId"], x["subject"], x.get("subSubject"), (x.get("standard") or "").strip())
                if key(g) == key(f) and any_overlap(f, g):
                    g["evidence"] += [e for e in f["evidence"] if not any(overlaps(e, x) for x in g["evidence"])]
                    if SEV_RANK[f["severity"]] < SEV_RANK[g["severity"]]:
                        g["severity"] = f["severity"]
                    f = None
                    break
            if f is not None:
                findings.append(f)

    # 2. cross-subject semantic duplicates: the strongest finding is the primary.
    #    Only findings from different subject skills (transition files) can suppress each other; different
    #    checks inside one skill are distinct violations even when they cite the same lines.
    findings.sort(key=lambda f: (SEV_RANK[f["severity"]], f["_step"], f["_ord"]))
    primaries, suppressed, suppressed_checks = [], [], []
    for f in findings:
        primary = next((p for p in primaries if p["_skill"] != f["_skill"] and any_overlap(f, p)), None)
        if primary is None:
            primaries.append(f)
            continue
        where = label(primary["subject"], primary.get("subSubject"))
        suppressed.append({"suppressedId": f["id"], "primaryId": primary["id"],
                           "reason": f"overlapping evidence; {primary['severity']} finding in {where} outranks or precedes {f['severity']} in {label(f['subject'], f.get('subSubject'))}"})
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
        "labelsNormalized": {r["skill"]: r["labelsNormalized"] for r in results},
        "notes": "checkResults are not embedded; render reads them from the per-subject transition files and applies suppressedChecks.",
    }
    write_json(os.path.join(run_dir, "90-aggregate.json"), agg)
    state.setdefault("steps", {})["90-aggregate"] = "completed"
    state["updatedAt"] = now_iso()
    write_json(os.path.join(run_dir, "state.json"), state)
    relabeled = sum(r["labelsNormalized"] for r in results)
    print(f"aggregate: overall {overall}/100 {band(overall)}; Error {counts['Error']}, Warning {counts['Warning']}, "
          f"Information {counts['Information']}; {len(suppressed)} duplicate(s) suppressed; "
          f"{relabeled} label(s) normalized")
    return 0


# ---------------------------------------------------------------- render

def cell(text):
    return re.sub(r"\s+", " ", str(text or "")).replace("|", "\\|").strip()


REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
REPORTS_DIR = os.path.join(REPO_ROOT, "docs", "reports")


def citation(standard, url, out_dir):
    """Markdown citation: plain text without a URL; repo-relative URLs rebased onto the report's folder.

    A URL with no scheme (and not starting with '/' or '#') is relative to docs/reports/ (finding-schema.md).
    """
    standard, url = str(standard or "").strip(), str(url or "").strip()
    if not url:
        return standard
    if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:|^[/#]", url):
        path, sep, frag = url.partition("#")
        try:
            rel = os.path.relpath(os.path.normpath(os.path.join(REPORTS_DIR, path)), out_dir)
            url = rel.replace("\\", "/") + sep + frag
        except ValueError:  # different drive on Windows: keep the original link
            pass
    return f"[{standard or url}]({url})"


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


def run_flags(state):
    """Appendix text for the run flags in state.json (absent on runs that predate operational flags)."""
    flags = state.get("flags")
    if not isinstance(flags, dict):
        return "not recorded"
    adv = "on" if flags.get("advanced") else "off"
    an = flags.get("analyzers", "auto")
    an = ",".join(an) if isinstance(an, list) else str(an)
    return f"advanced {adv}" + (f" · analyzers {an}" if flags.get("advanced") else " (IaC and CLI analyzers not run)")


def render(run_dir, out_path, copy_to=None):
    state = read_json(os.path.join(run_dir, "state.json"))
    agg = read_json(os.path.join(run_dir, "90-aggregate.json"))
    inv_path = os.path.join(run_dir, "01-inventory.json")
    inv = read_json(inv_path) if os.path.exists(inv_path) else {}
    results = load_results(run_dir)
    cur = {"dir": os.path.dirname(os.path.abspath(out_path))}  # citation links are rebased onto this folder
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
                "subSubject": f.get("subSubject", ""), "where": label(f["subject"], f.get("subSubject")),
                "file": f"{ev.get('file', '')}{extra}",
                "lineStart": ev.get("lineStart", ""), "lineEnd": ev.get("lineEnd", ""),
                "recommendation": f.get("recommendation", ""),
                "cite": citation(f.get("standard"), f.get("url"), cur["dir"])}

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
            sub = sub or r["subject"]
            group = subs["subSubjects"].setdefault(sub, {"subSubject": sub, "checks": [],
                                                         "heading": sub if sub != r["subject"] else ""})
            group["checks"].append({"checkId": cid, "result": result,
                                    "evidenceOrReason": cell(reason) if result != "pass" else ""})
    subjects_ctx = [{"name": s["name"], "subSubjects": list(s["subSubjects"].values())} for s in subjects.values()]

    strengths = {}
    for s in agg["strengths"]:
        ev = (s.get("evidence") or [{}])[0]
        strengths.setdefault(s["subject"], {"subject": s["subject"], "strengths": []})["strengths"].append(
            {"subSubject": s.get("subSubject", ""), "title": s["title"], "file": ev.get("file", ""),
             "tag": s.get("subSubject", "") if s.get("subSubject") != s["subject"] else ""})

    def by_sev(k):
        return [finding_row(f) for f in agg["findings"] if f["severity"] == k]

    urls = sorted({u for r in results for u in r["urlsFetched"]})
    skipped = inv.get("skippedSubjects", {})
    init_path = os.path.join(run_dir, "00-init.json")
    started = state.get("startedAt") or (read_json(init_path).get("startedAt") if os.path.exists(init_path) else "")
    generated = now_iso()

    def build_report(path):
        cur["dir"] = os.path.dirname(os.path.abspath(path))
        ctx = {
            "targetName": os.path.basename(str(state.get("targetPath", "")).rstrip("\\/")) or "target",
            "generatedAt": generated, "runId": state["runId"],
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
            "runFlags": run_flags(state),
        }
        return re.sub(r"\n{3,}", "\n\n", render_template(tpl, [ctx]))

    for path in [out_path] + ([copy_to] if copy_to else []):
        report = build_report(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
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
    if copy_to:
        print(f"copy: {os.path.abspath(copy_to)}")
    print(f"overall {agg['overallScore']}/100 {agg['overallBand']}")
    for t in agg["topRisks"]:
        print(f"  {t['rank']}. [{t['severity']}] {t['title']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["validate", "aggregate", "render", "labels"])
    ap.add_argument("run_dir", nargs="*", help="run directory (validate/aggregate/render), or skills to lint (labels)")
    ap.add_argument("--out", help="report path (render only)")
    ap.add_argument("--copy-to", help="also write the report to this path (render only)")
    a = ap.parse_args()
    if a.command == "labels":
        return labels_lint(a.run_dir)
    if len(a.run_dir) != 1:
        ap.error(f"{a.command} requires exactly one run directory")
    a.run_dir = a.run_dir[0]
    if a.command == "validate":
        return validate(a.run_dir)
    if a.command == "aggregate":
        return aggregate(a.run_dir)
    if not a.out:
        ap.error("render requires --out")
    return render(a.run_dir, a.out, a.copy_to)


if __name__ == "__main__":
    sys.exit(main())
