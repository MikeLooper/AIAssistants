#!/usr/bin/env python3
"""Deterministic run steps for compliance reviews: init (00), inventory (01), N/A subjects, worker dispatch
payloads, state updates, validate, aggregate (90) and render (99), plus maintainer lints and review packs.

Usage:
  compliance_report.py init      <targetPath> [--subjects all|a,b] [--advanced on|off] [--analyzers auto|none|a,b]
                                 [--out-file <path>] [--run-id <id>]
  compliance_report.py inventory <runDir> [--picks <picks.json>]
  compliance_report.py na        <runDir>
  compliance_report.py dispatch  <runDir> [--only <skill>]
  compliance_report.py step      <runDir> <stepId> <status> [--approval a,b]
  compliance_report.py resume    <runDir> [--from <NN>]
  compliance_report.py validate  <runDir> [--mark]
  compliance_report.py aggregate <runDir>
  compliance_report.py render    <runDir> --out docs/reports/<name>.md [--copy-to <path>]
  compliance_report.py labels    [skill ...]
  compliance_report.py packs     build|check [skill ...]

Standard library only. Reads the per-subject transition files in <runDir>
(NN-review-*.json, optionally NN-review-*.part-K.json from older runs). Workers write schemaVersion 2
files (compact `checks`, element-only citations, no labels); schemaVersion 1 files are still read.

Subject and sub-subject labels and each check's default severity are owned by each skill's
references/checklist.md. Citations (`standard`, `url`) are derived from the element ID through the
skill's references/standards/*.md files (see standards.py).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standards  # noqa: E402

SEV_WEIGHT = {"Error": 5, "Warning": 2, "Information": 1}
SEV_RANK = {"Error": 0, "Warning": 1, "Information": 2}
CONF_RANK = {"High": 0, "Medium": 1, "Low": 2}
EFFORT_RANK = {"Small": 0, "Medium": 1, "Large": 2}
RESULTS = {"pass", "fail", "N/A"}
SCHEMA_VERSION = 2                              # transition files written by this script and by workers
FILE_RE = re.compile(r"^(\d\d)-(review-[a-z0-9-]+?)(?:\.part-(\d+))?\.json$")
HEADER_KEYS = ["schemaVersion", "runId", "stepId", "status", "startedAt", "completedAt",
               "targetPath", "targetGitHead", "inputsHash"]
CHECK_BUCKETS = {"pass", "fail", "na"}          # schemaVersion 2 `checks` keys


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


def fmt_score(score):
    """Report/console text for a score: '87.50/100', or 'N/A' when no check applied (all subjects N/A)."""
    return f"{score:.2f}/100" if score is not None else "N/A"


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
    checks, retired, seen, severities = {}, set(), set(), {}
    start = next((i for i, l in enumerate(lines)
                  if l.lstrip().startswith("|") and "id" in [c.lower() for c in split_row(l)]), None)
    if start is None:
        problems.append("no checks table (a Markdown table whose header has an 'id' column)")
    else:
        cols = [c.lower() for c in split_row(lines[start])]
        ci = {name: cols.index(name) if name in cols else None for name in ("id", "sub-subject", "check")}
        sev_col = next((k for k, c in enumerate(cols) if "severity" in c), None)
        for name, idx in ci.items():
            if idx is None:
                problems.append(f"checks table has no '{name}' column")
        if sev_col is None:
            problems.append("checks table has no 'Default severity' column")
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
                        # the first word is the check's default; a parenthetical only qualifies Finding severity
                        sm = re.match(r"\W*(Error|Warning|Information)\b", cells[sev_col]) if sev_col is not None else None
                        if sm:
                            severities[cid] = sm.group(1)
                        else:
                            problems.append(f"line {n}: {cid} default severity {cells[sev_col]!r} doesn't start "
                                            "with Error, Warning or Information")
    subs = []
    for cid, sub in checks.items():
        if sub not in subs:
            subs.append(sub)
    _CHECKLISTS[skill] = {"subject": subject, "checks": checks, "retired": retired, "severities": severities,
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
                if "subject" in e or "subSubject" in e:  # schemaVersion 2 entries carry no labels: not drift
                    changed += 1
                e["subject"], e["subSubject"] = subj, sub
    d["checkResults"] = [c for c in d.get("checkResults", []) if c.get("checkId") not in cl["retired"]]
    return changed


def label(subject, sub):
    """`subject / subSubject`, or the subject alone when the two are equal or there is no sub-subject."""
    return subject if not sub or sub == subject else f"{subject} / {sub}"


def cite(entry, skill, warn=None):
    """Fill `standard`/`url` from `element` when the worker didn't give them (schemaVersion 2 citations)."""
    eid = str(entry.get("element") or "").strip()
    if not eid or str(entry.get("standard") or "").strip():
        return
    resolved = standards.resolve(skill, eid, entry.get("page"))
    if resolved:
        entry["standard"], entry["url"] = resolved
    else:
        entry["standard"], entry["url"] = eid, entry.get("url", "")
        if warn is not None:
            warn.append(f"element {eid!r} of {entry.get('id')} is not in {skill}'s standards (cited as plain text)")


def expand(d, skill):
    """Bring a subject transition file to the internal shape in place: schemaVersion 2 `checks` become
    `checkResults` with labels and severityIfFailed from the checklist; element citations are resolved.

    Returns (problems, warnings) specific to the compact shape. schemaVersion 1 files only get missing
    citations filled in.
    """
    problems, warnings = [], []
    for kind in ("findings", "strengths"):
        for e in d.get(kind, []) or []:
            cite(e, skill, warnings if kind == "findings" else None)
    if "checks" not in d or "checkResults" in d:
        return problems, warnings
    cl = load_checklist(skill)
    checks = d.get("checks")
    if not isinstance(checks, dict):
        return [f"checks must be an object with pass/fail/na, got {type(checks).__name__}"], warnings
    for key in checks:
        if key not in CHECK_BUCKETS:
            problems.append(f"checks has unknown key {key!r} (expected pass, fail, na)")
    results, where = [], {}

    def add(cid, result, reason="", ids=()):
        if cid in where:
            problems.append(f"check {cid} is listed under both {where[cid]} and {result}")
            return
        where[cid] = result
        sev = cl["severities"].get(cid) if usable(cl) else None
        if cid == PLACEHOLDER_CHECK:
            sev = None
        elif sev is None and usable(cl) and cid not in cl["retired"] and cid in cl["checks"]:
            problems.append(f"check {cid} has no default severity in the checklist")
        r = {"checkId": cid, "result": result, "severityIfFailed": sev, "findingIds": list(ids)}
        if reason:
            r["reason"] = reason
        results.append(r)

    passed = checks.get("pass", []) or []
    if not isinstance(passed, list):
        problems.append("checks.pass must be a list of check ids")
        passed = []
    for cid in passed:
        add(str(cid), "pass")
    for cid, v in (checks.get("fail") or {}).items():
        if isinstance(v, dict):
            add(cid, "fail", str(v.get("reason") or ""), v.get("findingIds") or [])
        elif isinstance(v, list):
            add(cid, "fail", "", v)
        else:
            add(cid, "fail", str(v or ""))
    for cid, v in (checks.get("na") or {}).items():
        add(cid, "N/A", str((v.get("reason") if isinstance(v, dict) else v) or ""))
    if not usable(cl) and any(r["result"] != "N/A" for r in results):
        problems.append(f"checklist for {skill} is missing or unreadable: check severities unknown (run `labels`)")
    d["checkResults"] = results
    d.setdefault("subject", cl["subject"] if usable(cl) else skill)
    return problems, warnings


def step_table():
    """{skill: 'NN'} from the step table in transition-schema.md, in step order."""
    if not os.path.exists(TRANSITION_SCHEMA):
        return {}
    with open(TRANSITION_SCHEMA, encoding="utf-8-sig") as f:
        pairs = re.findall(r"\|\s*(\d\d)\s*\|\s*(review-[a-z0-9-]+)\s*(?=\|)", f.read())
    return {skill: nn for nn, skill in sorted(pairs)}


def step_skills():
    """Skill names from the step table in transition-schema.md."""
    return list(step_table())


def labels_lint(skills):
    problems = []
    listed = step_skills()
    if not listed:
        problems.append({"file": os.path.relpath(TRANSITION_SCHEMA, SKILLS_DIR), "problem": "no step table found"})
    problems += standards.citations_lint(skills or None)
    problems += standards.packs_check(skills or None)
    if not skills:
        import_inventory()
        problems += [{"file": "compliance-inventory/references/subject-file-map.json", "problem": p}
                     for p in inventory.lint_map()]
        mapped = set(inventory.load_map()["subjects"])
        problems += [{"file": "compliance-inventory/references/subject-file-map.json",
                      "problem": f"no entry for subject {s}"} for s in listed if s not in mapped]
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


# ---------------------------------------------------------------- redaction (finding-schema.md "Redaction")

_scan = None


def scanner():
    """The shared secret/personal-data pattern module (compliance-inventory/scripts/sensitive_scan.py)."""
    global _scan
    if _scan is None:
        import_inventory()
        import sensitive_scan as mod  # noqa: E402
        _scan = mod
    return _scan


# Free-text fields a worker writes (finding-schema.md "Redaction"); `standard` is free text when `element` is omitted.
REDACT_FIELDS = ("title", "recommendation", "reason", "standard")


def redaction_problems(entry):
    """Evidence excerpts and free-text fields of one finding, strength or check result that contain a secret
    value or personal data. Free-text fields are scanned without file context, as `mask_obj` masks them."""
    out = []
    for i, ev in enumerate(entry.get("evidence") or []):
        if not isinstance(ev, dict):
            continue
        hits = scanner().excerpt_hits(str(ev.get("excerpt") or ""), ev.get("file"))
        if hits:
            out.append(f"evidence[{i}] excerpt contains a secret or personal-data value ({', '.join(hits)}); "
                       "replace the value with <redacted:kind>")
    for k in REDACT_FIELDS:
        hits = scanner().excerpt_hits(str(entry.get(k) or ""))
        if hits:
            out.append(f"{k} contains a secret or personal-data value ({', '.join(hits)}); "
                       "replace the value with <redacted:kind>")
    return out


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


def validate(run_dir, mark=False):
    problems, warnings = [], []
    state_path = os.path.join(run_dir, "state.json")
    state = read_json(state_path) if os.path.exists(state_path) else {}
    if not state:
        problems.append({"file": "state.json", "problem": "missing"})
    found, file_ok = set(), {}
    for _step, skill, _part, name in subject_files(run_dir):
        found.add(skill)
        before = len(problems)
        try:
            d = read_json(os.path.join(run_dir, name))
        except Exception as e:  # noqa: BLE001
            problems.append({"file": name, "problem": f"invalid JSON: {e}"})
            file_ok[name] = False
            continue
        compact = "checks" in d
        p2, w2 = expand(d, skill)
        problems += [{"file": name, "problem": x} for x in p2]
        warnings += [{"file": name, "problem": x} for x in w2]
        for k in HEADER_KEYS:
            if k not in d:
                problems.append({"file": name, "problem": f"missing header field {k}"})
        if d.get("status") != "completed":
            problems.append({"file": name, "problem": f"status is {d.get('status')!r}, expected 'completed'"})
        if d.get("skill") != skill:
            problems.append({"file": name, "problem": f"skill field {d.get('skill')!r} does not match file name"})
        for k in ("findings", "strengths") + (("checks",) if compact else ("subject", "checkResults")):
            if k not in d:
                problems.append({"file": name, "problem": f"missing {k}"})
        ids = set()
        for kind in ("findings", "strengths"):
            for e in d.get(kind, []) or []:
                for p in redaction_problems(e):
                    problems.append({"file": name, "problem": f"{kind[:-1]} {e.get('id')}: {p}"})
        for c in d.get("checkResults", []) or []:
            if isinstance(c, dict):
                for p in redaction_problems(c):
                    problems.append({"file": name, "problem": f"check {c.get('checkId')}: {p}"})
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
            elif c["result"] != "N/A" and not compact and c.get("severityIfFailed") not in SEV_WEIGHT:
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
        if compact:  # schemaVersion 2 files carry no labels, so only the id checks apply
            w = [x for x in w if "normalized by aggregate" not in x]
        problems += [{"file": name, "problem": x} for x in p]
        warnings += [{"file": name, "problem": x} for x in w]
        file_ok[name] = len(problems) == before
    missing_skills = [s for s in state.get("subjects", []) if s not in found]
    ok = not problems and not missing_skills
    if mark and state:
        steps = state.setdefault("steps", {})
        for name, good in file_ok.items():
            m = FILE_RE.match(name)
            sid = f"{m.group(1)}-{m.group(2)}"
            steps[sid] = "completed" if good else "failed"
        for skill in missing_skills:
            sid = f"{step_table().get(skill, '??')}-{skill}"
            if steps.get(sid) in ("started", "completed"):
                steps[sid] = "failed"
        state["updatedAt"] = now_iso()
        write_json(state_path, state)
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
        expand(d, skill)
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
            if c["result"] == "N/A" or c.get("severityIfFailed") not in SEV_WEIGHT:
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
        "schemaVersion": SCHEMA_VERSION, "runId": state["runId"], "stepId": "90-aggregate", "status": "completed",
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
    write_json(os.path.join(run_dir, "90-aggregate.json"), scanner().mask_obj(agg))  # no secret reaches step 90
    state.setdefault("steps", {})["90-aggregate"] = "completed"
    state["updatedAt"] = now_iso()
    write_json(os.path.join(run_dir, "state.json"), state)
    relabeled = sum(r["labelsNormalized"] for r in results)
    print(f"aggregate: overall {fmt_score(overall)} {band(overall)}; Error {counts['Error']}, Warning {counts['Warning']}, "
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
            "overallScore": fmt_score(agg["overallScore"]), "overallBand": agg["overallBand"],
            "subjectScores": [{"subject": s["subject"], "band": s["band"], "score": fmt_score(s["score"])}
                              for s in agg["subjectScores"]],
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
        return scanner().mask(re.sub(r"\n{3,}", "\n\n", render_template(tpl, [ctx])))

    for path in [out_path] + ([copy_to] if copy_to else []):
        report = build_report(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(report)

    write_json(os.path.join(run_dir, "99-report.json"), {
        "schemaVersion": SCHEMA_VERSION, "runId": state["runId"], "stepId": "99-report", "status": "completed",
        "startedAt": now_iso(), "completedAt": now_iso(), "targetPath": state.get("targetPath"),
        "targetGitHead": state.get("targetGitHead"), "inputsHash": state.get("inputsHash"),
        "reportPath": out_path.replace("\\", "/")})
    state.setdefault("steps", {})["99-report"] = "completed"
    state.update({"status": "completed", "reportPath": out_path.replace("\\", "/"), "updatedAt": now_iso()})
    write_json(os.path.join(run_dir, "state.json"), state)
    print(f"report: {out_path}")
    if copy_to:
        print(f"copy: {os.path.abspath(copy_to)}")
    print(f"overall {fmt_score(agg['overallScore'])} {agg['overallBand']}")
    for t in agg["topRisks"]:
        print(f"  {t['rank']}. [{t['severity']}] {t['title']}")
    return 0


# ---------------------------------------------------------------- run management (steps 00, 01, N/A, dispatch)

TRANSITIONS_DIR = os.path.join(REPO_ROOT, "transitions")
INVENTORY_SCRIPTS = os.path.join(SKILLS_DIR, "compliance-inventory", "scripts")
inventory = None


def import_inventory():
    global inventory
    if inventory is None:
        sys.path.insert(0, INVENTORY_SCRIPTS)
        import inventory as inv_module  # noqa: E402
        inventory = inv_module
    return inventory


def emit(obj):
    print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def fail(message, **extra):
    emit({"ok": False, "error": message, **extra})
    return 1


def rel_repo(path):
    try:
        return os.path.relpath(os.path.abspath(path), REPO_ROOT).replace("\\", "/")
    except ValueError:
        return os.path.abspath(path)


def git_head(target):
    """`git -C <target> rev-parse HEAD`, the review's only Git command; None when it isn't a repository."""
    try:
        out = subprocess.run(["git", "-C", target, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    head = out.stdout.strip()
    return head if out.returncode == 0 and re.fullmatch(r"[0-9a-f]{7,64}", head) else None


def inputs_hash(target, head, subjects, flags):
    data = {"targetPath": os.path.normcase(os.path.abspath(target)), "targetGitHead": head,
            "subjects": sorted(subjects), "flags": flags}
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def header(state, step_id, status="completed"):
    t = now_iso()
    return {"schemaVersion": SCHEMA_VERSION, "runId": state["runId"], "stepId": step_id, "status": status,
            "startedAt": t, "completedAt": t if status == "completed" else None,
            "targetPath": state["targetPath"], "targetGitHead": state.get("targetGitHead"),
            "inputsHash": state.get("inputsHash")}


def subject_step(skill):
    return f"{step_table()[skill]}-{skill}"


def parse_bool(value):
    v = str(value).strip().lower()
    if v in ("on", "true", "yes", "1", ""):
        return True
    if v in ("off", "false", "no", "0"):
        return False
    raise ValueError(f"invalid boolean {value!r} (use on|off|true|false)")


def resolve_subjects(value):
    table = step_table()
    if not value or value == "all":
        return list(table)
    chosen = [s.strip() for s in value.split(",") if s.strip()]
    unknown = [s for s in chosen if s not in table]
    if unknown:
        raise ValueError(f"unknown subject(s): {', '.join(unknown)}")
    return [s for s in table if s in chosen]


def save_state(run_dir, state):
    state["updatedAt"] = now_iso()
    write_json(os.path.join(run_dir, "state.json"), state)


def init_run(target, subjects="all", advanced="off", analyzers="auto", out_file=None, run_id=None,
             transitions_dir=None):
    """Step 00: create the run folder, `00-init.json` and `state.json`; print the run's identity as JSON."""
    target_abs = os.path.abspath(target)
    if not os.path.isdir(target_abs):
        return fail(f"target path not found or not a folder: {target}")
    try:
        chosen = resolve_subjects(subjects)
        adv = parse_bool(advanced)
    except ValueError as e:
        return fail(str(e))
    an = analyzers or "auto"
    if an not in ("auto", "none"):
        an = [a.strip() for a in an.split(",") if a.strip()]
    if out_file:
        out_abs = os.path.abspath(out_file if os.path.isabs(out_file) else os.path.join(REPO_ROOT, out_file))
        inside = os.path.normcase(out_abs).startswith(os.path.normcase(target_abs.rstrip("\\/") + os.sep))
        if inside:
            return fail(f"--out-file must not be inside the target: {out_abs}")
    head = git_head(target_abs)
    flags = {"advanced": adv, "analyzers": an}
    short = re.sub(r"[^A-Za-z0-9._-]+", "-", os.path.basename(target_abs.rstrip("\\/"))).strip("-") or "target"
    base_id = run_id or f"{datetime.now():%Y-%m-%d_%H%M}-{short}"
    root = transitions_dir or TRANSITIONS_DIR
    rid, n = base_id, 2
    while os.path.exists(os.path.join(root, rid)):
        if run_id:
            return fail(f"run {run_id} already exists")
        rid, n = f"{base_id}-{n}", n + 1
    run_dir = os.path.join(root, rid)
    os.makedirs(run_dir)
    started = now_iso()
    steps = {"00-init": "completed", "01-inventory": "not-started", "02-analyzers": "not-started"}
    steps.update({subject_step(s): "not-started" for s in chosen})
    steps.update({"90-aggregate": "not-started", "99-report": "not-started"})
    state = {"schemaVersion": SCHEMA_VERSION, "runId": rid, "targetPath": target_abs, "targetGitHead": head,
             "inputsHash": inputs_hash(target_abs, head, chosen, flags), "startedAt": started, "updatedAt": started,
             "status": "in-progress", "subjects": chosen, "flags": flags, "analyzerApproval": "none",
             "linkApprovals": {}, "steps": steps, "reportPath": None}
    write_json(os.path.join(run_dir, "00-init.json"), dict(header(state, "00-init"), subjects=chosen, flags=flags))
    save_state(run_dir, state)
    emit({"ok": True, "runId": rid, "runDir": rel_repo(run_dir), "targetPath": target_abs, "targetGitHead": head,
          "inputsHash": state["inputsHash"], "startedAt": started, "subjects": chosen, "flags": flags})
    return 0


def run_inventory(run_dir, picks_path=None):
    """Step 01: write `01-inventory.json` from the scripted inventory; print a compact summary as JSON."""
    inv_mod = import_inventory()
    state = read_json(os.path.join(run_dir, "state.json"))
    picks = read_json(picks_path) if picks_path else None
    advanced = bool((state.get("flags") or {}).get("advanced", True))
    try:
        content = inv_mod.build_inventory(state["targetPath"], state["subjects"], advanced, picks)
    except (ValueError, KeyError) as e:
        state["steps"]["01-inventory"] = "failed"
        save_state(run_dir, state)
        return fail(str(e))
    write_json(os.path.join(run_dir, "01-inventory.json"), dict(header(state, "01-inventory"), **content))
    state["steps"]["01-inventory"] = "completed"
    if not advanced:
        state["steps"]["02-analyzers"] = "skipped"
    save_state(run_dir, state)
    batches = [{"batchId": b["batchId"], "subjects": {s: len(f) for s, f in b["subjectFiles"].items()}}
               for b in content["fileBatches"]]
    sampled = {s: {"totalMatched": m["totalMatched"],
                   "sample": next(b["subjectFiles"][s] for b in content["fileBatches"] if s in b["subjectFiles"]),
                   "candidates": m["candidates"]} for s, m in content["sampling"].items()}
    emit({"ok": True, "languages": content["languages"], "frameworks": content["frameworks"],
          "apiSpecsFound": content["apiSpecsFound"], "mcpFound": content["mcpFound"],
          "httpSurfaceFound": content["httpSurfaceFound"], "iacFound": content["iacFound"],
          "personalDataFound": content.get("personalDataFound"),
          "secretCandidates": content.get("secretCandidatesTotal", 0), "piiCandidates": content.get("piiCandidatesTotal", 0),
          "targetFiles": content["targetFiles"], "batches": batches, "skippedSubjects": content["skippedSubjects"],
          "sampled": sampled})
    return 0


def write_na(run_dir):
    """Write the minimal N/A transition file for every chosen subject the inventory skipped."""
    state = read_json(os.path.join(run_dir, "state.json"))
    inv = read_json(os.path.join(run_dir, "01-inventory.json"))
    written = []
    for skill, reason in inv.get("skippedSubjects", {}).items():
        if skill not in state.get("subjects", []):
            continue
        sid = subject_step(skill)
        doc = dict(header(state, sid), batchId=None, skill=skill, findings=[], strengths=[],
                   checks={"na": {PLACEHOLDER_CHECK: reason}}, notes=reason)
        write_json(os.path.join(run_dir, f"{sid}.json"), doc)
        state["steps"][sid] = "completed"
        written.append(f"{sid}.json")
    save_state(run_dir, state)
    emit({"ok": True, "written": written})
    return 0


def dispatch(run_dir, only=None):
    """Print one worker payload per `fileBatches` entry (JSON lines). `--only` gives a single-subject retry."""
    state = read_json(os.path.join(run_dir, "state.json"))
    inv = read_json(os.path.join(run_dir, "01-inventory.json"))
    run_abs = os.path.abspath(run_dir)
    batches = inv.get("fileBatches", [])
    if only:
        batches = [dict(b, subjects=[only], subjectFiles={only: b["subjectFiles"][only]})
                   for b in batches if only in b["subjectFiles"]]
        if not batches:
            return fail(f"{only} is not in any batch of this run")
    langs = inv.get("languages", [])
    head = {"schemaVersion": SCHEMA_VERSION, "runId": state["runId"], "startedAt": state.get("startedAt"),
            "targetPath": state["targetPath"], "targetGitHead": state.get("targetGitHead"),
            "inputsHash": state.get("inputsHash")}
    analyzers = os.path.join(run_abs, "02-analyzers.json")
    secrets, secrets_total = merged_secret_candidates(run_dir, inv, state["targetPath"])
    for b in batches:
        subjects = []
        for skill in b["subjects"]:
            sid = subject_step(skill)
            entry = {"skill": skill, "stepId": sid, "out": os.path.join(run_abs, f"{sid}.json").replace("\\", "/"),
                     "files": b["subjectFiles"][skill], "packs": standards.pack_paths(skill, langs)}
            if skill == "review-testing" and inv.get("testInventory"):
                entry["testInventory"] = inv["testInventory"]
            if skill == "review-maintainability" and inv.get("folderListing"):
                entry["folderListing"] = inv["folderListing"]
            if skill == "review-dependency-management" and os.path.exists(analyzers):
                entry["analyzersFile"] = analyzers.replace("\\", "/")
            if skill == "review-security-operational" and secrets:
                entry["secretCandidates"] = secrets
                entry["secretCandidatesTotal"] = secrets_total
            if skill == "review-data-protection":
                if inv.get("piiCandidates"):
                    entry["piiCandidates"] = inv["piiCandidates"]
                    entry["piiCandidatesTotal"] = inv.get("piiCandidatesTotal", len(inv["piiCandidates"]))
                if inv.get("personalDataSignals"):
                    entry["personalDataSignals"] = inv["personalDataSignals"]
            subjects.append(entry)
            state["steps"][sid] = "started"
        payload = {"runId": state["runId"], "batchId": b["batchId"], "targetRoot": state["targetPath"],
                   "advanced": bool(inv.get("advanced", True)), "languages": langs, "header": head,
                   "subjects": subjects}
        if inv.get("mcpFound"):
            payload.update(mcpServers=inv.get("mcpServers", []), httpSurfaceFound=inv.get("httpSurfaceFound"))
        emit(payload)
    save_state(run_dir, state)
    return 0


GITLEAKS_RAW = "02-analyzer-gitleaks.raw.json"
MAX_SECRET_CANDIDATES = 50


def gitleaks_candidates(run_dir, target):
    """Secret candidates from a `gitleaks dir --redact` JSON report in the run folder (file, line and rule only;
    the report's Match/Secret fields are never read)."""
    path = os.path.join(run_dir, GITLEAKS_RAW)
    if not os.path.exists(path):
        return []
    try:
        data = read_json(path)
    except (OSError, ValueError):
        return []
    root = os.path.abspath(target)

    def inside(path):
        return os.path.normcase(path).startswith(os.path.normcase(root) + os.sep)

    out = []
    for item in data if isinstance(data, list) else []:
        f = str(item.get("File") or "").strip() if isinstance(item, dict) else ""
        if not f:
            continue
        full = os.path.abspath(f if os.path.isabs(f) else os.path.join(root, f))
        if not inside(full):
            full = os.path.abspath(f)  # a path relative to the folder gitleaks ran in
        rel = os.path.relpath(full, root) if inside(full) else f
        line = item.get("StartLine")
        out.append({"file": rel.replace("\\", "/"), "line": line if isinstance(line, int) else None,
                    "rule": f"gitleaks:{item.get('RuleID') or 'unknown'}", "confidence": "high"})
    return out


def merged_secret_candidates(run_dir, inv, target):
    """(candidates, total): inventory `secretCandidates` plus gitleaks results, one per file and line, highest
    confidence first, capped at 50. `total` counts every distinct candidate before the cap."""
    rank = {"high": 0, "medium": 1, "low": 2}
    own = list(inv.get("secretCandidates") or [])
    extra = gitleaks_candidates(run_dir, target)
    found = {}
    for c in own + extra:
        key = (c["file"].lower(), c.get("line"))
        cur = found.get(key)
        if cur is None or rank.get(c.get("confidence"), 3) < rank.get(cur.get("confidence"), 3):
            found[key] = c
    items = sorted(found.values(), key=lambda c: (rank.get(c.get("confidence"), 3), c["file"], c.get("line") or 0))
    own_keys = {(c["file"].lower(), c.get("line")) for c in own}
    new_extra = len({(c["file"].lower(), c.get("line")) for c in extra} - own_keys)
    total = max(int(inv.get("secretCandidatesTotal") or 0), len(own)) + new_extra
    return items[:MAX_SECRET_CANDIDATES], max(total, len(items))


def set_step(run_dir, step_id, status, approval=None):
    if status not in ("not-started", "started", "completed", "failed", "skipped"):
        return fail(f"invalid status {status!r}")
    state = read_json(os.path.join(run_dir, "state.json"))
    state.setdefault("steps", {})[step_id] = status
    if approval is not None:
        state["analyzerApproval"] = [a for a in approval.split(",") if a] or "none"
    save_state(run_dir, state)
    emit({"ok": True, "stepId": step_id, "status": status})
    return 0


def step_number(step_id):
    m = re.match(r"^(\d\d)-", step_id)
    return int(m.group(1)) if m else -1


def resume_run(run_dir, from_step=None):
    """Recompute targetGitHead/inputsHash, optionally supersede step NN and later, and name the next step."""
    state_path = os.path.join(run_dir, "state.json")
    if not os.path.exists(state_path):
        return fail(f"no state.json in {run_dir}")
    state = read_json(state_path)
    target = state["targetPath"]
    head = git_head(target) if os.path.isdir(target) else None
    flags = state.get("flags") or {"advanced": True, "analyzers": "auto"}
    new_hash = inputs_hash(target, head, state.get("subjects", []), flags)
    superseded = []
    if from_step is not None:
        nn = int(from_step)
        files = sorted(n for n in os.listdir(run_dir) if re.match(r"^\d\d-.+\.json$", n))
        doomed = {n for n in files if step_number(n) >= nn}
        batches = set()
        for n in doomed:
            if FILE_RE.match(n):
                try:
                    batches.add(read_json(os.path.join(run_dir, n)).get("batchId"))
                except (OSError, ValueError):
                    pass
        batches.discard(None)
        for n in files:  # sibling subjects of a superseded batch call are superseded with it
            if n not in doomed and FILE_RE.match(n):
                try:
                    if read_json(os.path.join(run_dir, n)).get("batchId") in batches:
                        doomed.add(n)
                except (OSError, ValueError):
                    pass
        sup = os.path.join(run_dir, "superseded")
        os.makedirs(sup, exist_ok=True)
        for n in sorted(doomed):
            dest = os.path.join(sup, n)
            k = 2
            while os.path.exists(dest):
                dest = os.path.join(sup, f"{n[:-5]}.{k}.json")
                k += 1
            shutil.move(os.path.join(run_dir, n), dest)
            superseded.append(n)
        steps = state.setdefault("steps", {})
        for sid in list(steps):
            if step_number(sid) >= nn:
                steps[sid] = "not-started"
        for n in superseded:
            m = FILE_RE.match(n)
            if m:
                steps[f"{m.group(1)}-{m.group(2)}"] = "not-started"
        state.update(status="in-progress", reportPath=None)
        save_state(run_dir, state)
    pending = [sid for sid in sorted(state.get("steps", {}), key=step_number)
               if state["steps"][sid] not in ("completed", "skipped")]
    emit({"ok": True, "runId": state["runId"], "status": state.get("status"), "targetGitHead": head,
          "targetGitHeadChanged": head != state.get("targetGitHead"),
          "inputsHashChanged": new_hash != state.get("inputsHash"),
          "nextStep": pending[0] if pending else None, "pending": pending, "superseded": superseded})
    return 0


def packs_command(action, skills):
    if action == "build":
        written = standards.packs_build(skills or None)
        emit({"ok": True, "written": len(written)})
        return 0
    problems = standards.packs_check(skills or None)
    print(json.dumps({"ok": not problems, "problems": problems}, indent=2, ensure_ascii=False))
    return 0 if not problems else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["init", "inventory", "na", "dispatch", "step", "resume", "validate",
                                        "aggregate", "render", "labels", "packs"])
    ap.add_argument("args", nargs="*", help="run directory, target path, step arguments or skills (see usage)")
    ap.add_argument("--out", help="report path (render)")
    ap.add_argument("--copy-to", help="also write the report to this path (render)")
    ap.add_argument("--mark", action="store_true", help="record each subject's validation result in state.json")
    ap.add_argument("--subjects", default="all", help="init: all or comma-separated skill names")
    ap.add_argument("--advanced", default="off", help="init: on|off")
    ap.add_argument("--analyzers", default="auto", help="init: auto|none|comma-separated keys")
    ap.add_argument("--out-file", help="init: the caller's --out-file, checked against the target")
    ap.add_argument("--run-id", help="init: use this run id instead of <YYYY-MM-DD_HHmm>-<target>")
    ap.add_argument("--picks", help="inventory: JSON file {skill: [files]} replacing sampled file lists")
    ap.add_argument("--only", help="dispatch: a single-subject payload for this skill (retry)")
    ap.add_argument("--from", dest="from_step", help="resume: supersede this step number and later")
    ap.add_argument("--approval", help="step: analyzer names that ran (step 02)")
    a = ap.parse_args()
    if a.command == "labels":
        return labels_lint(a.args)
    if a.command == "packs":
        if not a.args or a.args[0] not in ("build", "check"):
            ap.error("packs requires build or check")
        return packs_command(a.args[0], a.args[1:])
    if a.command == "init":
        if len(a.args) != 1:
            ap.error("init requires exactly one target path")
        return init_run(a.args[0], a.subjects, a.advanced, a.analyzers, a.out_file, a.run_id)
    if a.command == "step":
        if len(a.args) != 3:
            ap.error("step requires <runDir> <stepId> <status>")
        return set_step(*a.args, approval=a.approval)
    if len(a.args) != 1:
        ap.error(f"{a.command} requires exactly one run directory")
    run_dir = a.args[0]
    if a.command == "inventory":
        return run_inventory(run_dir, a.picks)
    if a.command == "na":
        return write_na(run_dir)
    if a.command == "dispatch":
        return dispatch(run_dir, a.only)
    if a.command == "resume":
        return resume_run(run_dir, a.from_step)
    if a.command == "validate":
        return validate(run_dir, a.mark)
    if a.command == "aggregate":
        return aggregate(run_dir)
    if not a.out:
        ap.error("render requires --out")
    return render(run_dir, a.out, a.copy_to)


if __name__ == "__main__":
    sys.exit(main())
