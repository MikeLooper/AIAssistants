"""Secret and personal-data pattern pass (standard library only).

Driven by `../references/secret-patterns.json`. Used by:

* `inventory.py` (step 01): `secretCandidates`, `piiCandidates` and `personalDataFound`. Candidates record
  file, line, rule and confidence only; a matched value is never stored or printed.
* `compliance_report.py`: `validate` reports evidence excerpts that contain a secret or personal data
  (`excerpt_hits`), and `aggregate`/`render` mask any that remain (`mask`).

Reads the target's working files only: it never runs Git and never reads `.git/`.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERNS_PATH = os.path.normpath(os.path.join(HERE, "..", "references", "secret-patterns.json"))
CONF_RANK = {"high": 0, "medium": 1, "low": 2}

_RULES = {}


def _glob_regex(pattern):
    from inventory import glob_regex  # noqa: E402  (inventory imports this module lazily: no cycle at import time)
    return glob_regex(pattern)


def _match_any(globs, rel):
    return any(_glob_regex(g).match(rel) for g in globs or [])


class Rules:
    """Compiled rules from secret-patterns.json."""

    def __init__(self, data):
        self.data = data
        sec = data["secrets"]
        self.max_bytes = int(data.get("maxBytesPerFile", 262144))
        self.max_line = int(data.get("maxLineLength", 4000))
        self.max_candidates = int(data.get("maxCandidates", 50))
        self.skip_globs = data.get("skipGlobs", [])
        self.example_globs = data.get("exampleGlobs", [])
        self.secret_rules = [self._compile(r) for r in sec["formats"] + sec["assignments"]]
        ph = sec.get("placeholders", {})
        self.ph_value = re.compile(ph["valueRegex"]) if ph.get("valueRegex") else None
        self.ph_contains = re.compile(ph["containsRegex"]) if ph.get("containsRegex") else None
        self.allow = [a for a in sec.get("allowlist", []) if a]
        self.file_rules = []
        for r in sec.get("files", []):
            r = dict(r)
            r["_line"] = re.compile(r["lineRegex"], re.M) if r.get("lineRegex") else None
            self.file_rules.append(r)
        pii = data.get("pii", {})
        self.pii_scope = pii.get("scopeGlobs", [])
        self.pii_rules = [self._compile(r) for r in pii.get("rules", [])]
        self.pii_allow = {re.sub(r"[\s-]", "", a).upper() for a in pii.get("allowlist", [])}
        self.reserved = re.compile(pii["reservedEmailDomains"]) if pii.get("reservedEmailDomains") else None
        pd = data.get("personalData", {})
        self.pd = dict(pd)
        for k in ("fieldMarkers", "fields", "classification", "tables"):
            if pd.get(k):
                self.pd["_" + k] = re.compile(pd[k], re.M)

    @staticmethod
    def _compile(r):
        r = dict(r)
        r["_rx"] = re.compile(r["regex"])
        return r

    # -- value filters
    def placeholder(self, value):
        v = value.strip().strip("\"'")
        if not v:
            return True
        if self.ph_value and self.ph_value.fullmatch(v):
            return True
        if self.ph_contains and self.ph_contains.search(v):
            return True
        return False

    def allowlisted(self, value):
return any(value == a for a in self.allow)

    def pii_valid(self, rule, value, groups):
        norm = re.sub(r"[\s-]", "", value).upper()
        if norm in self.pii_allow:
            return False
        check = rule.get("check")
        if check == "luhn":
            return 13 <= len(norm) <= 19 and luhn(norm)
        if check == "iban":
            return iban_ok(norm)
        if check == "email":
            domain = groups.get("domain") or value.rsplit("@", 1)[-1]
            return not (self.reserved and self.reserved.search(domain))
        return True


def luhn(digits):
    if not digits.isdigit():
        return False
    total, alt = 0, False
    for ch in reversed(digits):
        d = int(ch)
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


def iban_ok(iban):
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", iban):
        return False
    moved = iban[4:] + iban[:4]
    num = "".join(str(int(c, 36)) for c in moved)
    return int(num) % 97 == 1


def load(path=PATTERNS_PATH):
    if path not in _RULES:
        with open(path, encoding="utf-8-sig") as f:
            _RULES[path] = Rules(json.load(f))
    return _RULES[path]


def _value_span(m):
    if "value" in m.re.groupindex and m.group("value") is not None:
        return m.span("value"), m.group("value")
    return m.span(), m.group(0)


def _line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def _line_text(text, pos):
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    return text[start:end if end != -1 else len(text)]


def _secret_matches(rules, text, rel, excerpt):
    """Yield (rule, match, (start, end)) for secret rules that apply to `rel` (None = any file)."""
    example = rel is not None and _match_any(rules.example_globs, rel)
    for r in rules.secret_rules:
        if excerpt and r.get("excerpt") is False:
            continue
        if example and r["confidence"] != "high":  # templates hold sample values; only unambiguous formats count
            continue
        if r.get("fileGlobs"):
            if rel is None or not _match_any(r["fileGlobs"], rel):
                continue
        for m in r["_rx"].finditer(text):
            span, value = _value_span(m)
            if excerpt and r.get("valueRequiredInExcerpt") and not (m.groupdict().get("value")):
                continue
            if r["confidence"] != "high" and rules.placeholder(value):
                continue
            if rules.allowlisted(value):
                continue
            if r["rule"] == "private-key-block" and m.groupdict().get("value"):
                span = m.span("value")
            elif r["rule"] == "private-key-block":
                span = m.span()
            yield r, m, span


def _pii_matches(rules, text, excerpt):
    for r in rules.pii_rules:
        if excerpt and r.get("excerpt") is False:
            continue
        for m in r["_rx"].finditer(text):
            span, value = _value_span(m)
            if rules.pii_valid(r, value, m.groupdict()):
                yield r, m, span


# ---------------------------------------------------------------- evidence checks (validate / aggregate / render)

def excerpt_hits(text, file=None, rules=None):
    """Rule names whose pattern matches `text` (an evidence excerpt or other report text)."""
    rules = rules or load()
    if not text:
        return []
    hits = [r["rule"] for r, _m, _s in _secret_matches(rules, text, file, True)]
    hits += [r["rule"] for r, _m, _s in _pii_matches(rules, text, True)]
    return sorted(set(hits))


def mask(text, file=None, rules=None):
    """`text` with every secret or personal-data value replaced by `<redacted:kind>`."""
    rules = rules or load()
    if not text:
        return text
    spans = [(s, r["kind"]) for r, _m, s in _secret_matches(rules, text, file, True)]
    spans += [(s, r["kind"]) for r, _m, s in _pii_matches(rules, text, True)]
    if not spans:
        return text
    spans.sort(key=lambda x: (x[0][0], -x[0][1]))
    merged = []
    for (a, b), kind in spans:
        if merged and a < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
            continue
        merged.append([a, b, kind])
    out, pos = [], 0
    for a, b, kind in merged:
        out.append(text[pos:a])
        out.append(f"<redacted:{kind}>")
        pos = b
    out.append(text[pos:])
    return "".join(out)


def mask_obj(obj, file=None, rules=None):
    """Mask every string inside a JSON-like value; evidence `excerpt`s are masked with their own file's rules."""
    rules = rules or load()
    if isinstance(obj, str):
        return mask(obj, file, rules)
    if isinstance(obj, list):
        return [mask_obj(x, file, rules) for x in obj]
    if isinstance(obj, dict):
        f = obj.get("file") if isinstance(obj.get("file"), str) else file
        return {k: (v if k in ("file", "url", "id", "checkId", "element") else mask_obj(v, f, rules))
                for k, v in obj.items()}
    return obj


# ---------------------------------------------------------------- step-01 scan

def _add(found, rel, line, rule, confidence):
    key = (rel, line)
    cur = found.get(key)
    if cur is None or CONF_RANK[confidence] < CONF_RANK[cur["confidence"]]:
        found[key] = {"file": rel, "line": line, "rule": rule, "confidence": confidence}


def _ranked(found, cap):
    items = sorted(found.values(), key=lambda c: (CONF_RANK[c["confidence"]], c["file"], c["line"] or 0))
    return items[:cap], len(items)


def scan_target(target, files, pii_files, rules=None):
    """(secretCandidates, secretTotal, piiCandidates, piiTotal) for a `Target`-like object (with `root`).

    `files` are the target-relative files to scan for secrets; `pii_files` the subset that are test,
    fixture, seed or sample files (scanned for personal data too). Values are never kept.
    """
    rules = rules or load()
    secrets, pii = {}, {}
    pii_set = set(pii_files)
    for rel in files:
        if _match_any(rules.skip_globs, rel):
            continue
        text = None
        for fr in rules.file_rules:
            if not _match_any(fr["globs"], rel) or _match_any(fr.get("exclude"), rel):
                continue
            if fr.get("binaryOk"):
                _add(secrets, rel, None, fr["rule"], fr["confidence"])
                continue
            if text is None:
                text = read_text(target.root, rel, rules.max_bytes)
            if not text or fr["_line"] is None:
                continue
            for m in fr["_line"].finditer(text):
                value = m.groupdict().get("value")
                if value is not None and (rules.placeholder(value) or rules.allowlisted(value)):
                    continue
                _add(secrets, rel, _line_of(text, m.start()), fr["rule"], fr["confidence"])
                break
        if text is None:
            text = read_text(target.root, rel, rules.max_bytes)
        if not text:
            continue
        for r, m, span in _secret_matches(rules, text, rel, False):
            if len(_line_text(text, span[0])) > rules.max_line:
                continue
            _add(secrets, rel, _line_of(text, span[0]), r["rule"], r["confidence"])
        if rel in pii_set:
            for r, m, span in _pii_matches(rules, text, False):
                if len(_line_text(text, span[0])) > rules.max_line:
                    continue
                _add(pii, rel, _line_of(text, span[0]), r["rule"], r["confidence"])
    s, st = _ranked(secrets, rules.max_candidates)
    p, pt = _ranked(pii, rules.max_candidates)
    return s, st, p, pt


def read_text(root, rel, max_bytes):
    """Decoded text of a file, '' for binaries (a NUL byte in the first 4 KiB) or unreadable files."""
    try:
        with open(os.path.join(root, rel), "rb") as f:
            data = f.read(max_bytes)
    except OSError:
        return ""
    if b"\0" in data[:4096]:
        return ""
    return data.decode("utf-8", errors="ignore")


def personal_data_signals(inv, pii_candidates, rules=None):
    """(found, signals) for the step-01 `personalDataFound` rule. `inv` is an inventory.Inventory."""
    rules = rules or load()
    pd = rules.pd
    t = inv.t
    signals, seen = [], set()
    cap = int(pd.get("maxSignals", 10))

    def add(rel, signal):
        if (rel, signal) not in seen and len(signals) < cap:
            seen.add((rel, signal))
            signals.append({"file": rel, "signal": signal})

    by_glob = set(t.match(pd.get("fieldGlobs", []), inv.prod_source))
    marker, fields = pd.get("_fieldMarkers"), pd.get("_fields")
    if fields is not None:
        for rel in inv.prod_source:
            text = t.text(rel)
            if not text:
                continue
            if rel not in by_glob and not (marker and marker.search(text)):
                continue
            if fields.search(text):
                add(rel, "personal-data fields")
                if len(signals) >= 3:
                    break
    cls = pd.get("_classification")
    if cls is not None:
        for rel in t.grep(pd["classification"], inv.prod_source)[:3]:
            add(rel, "data classification")
    tables = pd.get("_tables")
    if tables is not None:
        for rel in t.match(pd.get("tableGlobs", [])):
            if tables.search(t.text(rel)):
                add(rel, "personal-data table")
                if sum(1 for s in signals if s["signal"] == "personal-data table") >= 2:
                    break
    for c in pii_candidates[:2]:
        add(c["file"], f"pii candidate ({c['rule']})")
    return bool(signals), signals
