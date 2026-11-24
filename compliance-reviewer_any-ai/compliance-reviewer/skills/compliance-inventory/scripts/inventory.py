"""Deterministic compliance inventory (step 01), standard library only.

Driven by `../references/subject-file-map.json`; `compliance_report.py inventory` calls `build_inventory`.
Reads the target's working files only: it never runs Git and never reads `.git/`.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
MAP_PATH = os.path.normpath(os.path.join(HERE, "..", "references", "subject-file-map.json"))
PROJECT_FILES = re.compile(r"(?:^|/)(?:[^/]+\.(?:cs|fs|vb)proj|pom\.xml|build\.gradle(?:\.kts)?|package\.json|pyproject\.toml|setup\.py|requirements\.txt)$")
TEST_NAME_RE = re.compile(r"(?i)(?:^test_.+|.+_test|.+tests?|.+\.(?:test|spec)|.+IT)\.\w+$")
LOW_VALUE = {"__init__.py", "conftest.py", "index.ts", "index.js", "AssemblyInfo.cs", "GlobalUsings.cs", "package-info.java"}
TEST_DIR_RE = re.compile(r"(?i)^(?:tests?|__tests__|e2e|spec|specs|.+[._-]?tests?|.+\.tests?\..+)$")
MAX_CANDIDATES = 60
MAX_FOLDER_LISTING = 80

_GLOB_CACHE = {}
_RE_CACHE = {}


def load_map(path=MAP_PATH):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def glob_regex(pattern):
    """Compile a map glob (see the map's $comment) to a regex matched against the whole relative path."""
    if pattern in _GLOB_CACHE:
        return _GLOB_CACHE[pattern]
    anchored = pattern.startswith("/")
    pat = pattern.lstrip("/")
    out, i = [], 0
    if not anchored and "/" not in pat:
        out.append("(?:.*/)?")
    while i < len(pat):
        c = pat[i]
        if pat.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pat.startswith("/**", i) and i + 3 == len(pat):
            out.append("(?:/.*)?")
            i += 3
        elif pat.startswith("**", i):
            out.append(".*")
            i += 2
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        elif c == "{":
            j = pat.index("}", i)
            out.append("(?:" + "|".join(re.escape(a) for a in pat[i + 1:j].split(",")) + ")")
            i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    rx = re.compile("".join(out) + r"\Z")
    _GLOB_CACHE[pattern] = rx
    return rx


def rx(pattern):
    if pattern not in _RE_CACHE:
        _RE_CACHE[pattern] = re.compile(pattern)
    return _RE_CACHE[pattern]


class Target:
    """The target's file list and lazily read file text."""

    def __init__(self, root, cfg):
        self.root = os.path.abspath(root)
        self.cfg = cfg
        self.files, self.truncated = [], False
        self._text = {}
        excluded = set(cfg["excludeDirs"])
        limit = cfg.get("maxTargetFiles", 50000)
        for dirpath, dirnames, filenames in os.walk(self.root):
            if "pyvenv.cfg" in filenames and os.path.abspath(dirpath) != self.root:  # a Python virtual environment
                dirnames[:] = []
                continue
            dirnames[:] = sorted(d for d in dirnames if d not in excluded)
            rel_dir = os.path.relpath(dirpath, self.root).replace("\\", "/")
            for name in sorted(filenames):
                rel = name if rel_dir == "." else f"{rel_dir}/{name}"
                if any(glob_regex(g).match(rel) for g in cfg.get("excludeGlobs", [])):
                    continue
                self.files.append(rel)
                if len(self.files) >= limit:
                    self.truncated = True
                    break
            if self.truncated:
                break
        self.files.sort()

    def text(self, rel):
        if rel not in self._text:
            try:
                with open(os.path.join(self.root, rel), "rb") as f:
                    data = f.read(self.cfg.get("maxReadBytes", 524288))
                self._text[rel] = "" if b"\0" in data[:4096] else data.decode("utf-8", errors="ignore")
            except OSError:
                self._text[rel] = ""
        return self._text[rel]

    def match(self, globs, pool=None):
        regs = [glob_regex(g) for g in globs]
        return [f for f in (self.files if pool is None else pool) if any(r.match(f) for r in regs)]

    def grep(self, pattern, pool):
        r = rx(pattern)
        return [f for f in pool if r.search(self.text(f))]


class Inventory:
    def __init__(self, root, advanced, cfg=None):
        self.cfg = cfg or load_map()
        self.t = Target(root, self.cfg)
        self.advanced = bool(advanced)
        self.patterns = self.cfg["patterns"]
        c, t = self.cfg, self.t
        exts = tuple(c["sourceExtensions"])
        test_excl = set(t.match(c["testExcludeGlobs"]))
        self.tests = set(t.match(c["testGlobs"])) - test_excl
        self.dropped = test_excl
        gen = set(t.match(c["generatedGlobs"]))
        marker = rx(c["generatedMarker"])
        for f in t.files:
            if f.endswith(exts) and f not in gen and marker.search(t.text(f)[:600]):
                gen.add(f)
        self.generated = gen
        iac = set(t.match(c["iacGlobs"]))
        ic = c["iacContains"]
        iac |= set(t.grep(ic["contains"], [f for f in t.match(ic["globs"]) if f not in iac]))
        iac |= set(t.grep(c["iacSourceContains"], [f for f in t.files if f.endswith(exts)]))
        self.iac = iac
        self.source = [f for f in t.files if f.endswith(exts) and f not in gen and f not in iac and f not in test_excl]
        self.prod_source = [f for f in self.source if f not in self.tests]
        self.test_source = [f for f in self.source if f in self.tests]

    # -- helpers
    def pat(self, value):
        """Replace '@name' references to the map's `patterns` with the (non-capturing) pattern itself."""
        return re.sub(r"@(\w+)", lambda m: f"(?:{self.patterns[m.group(1)]})" if m.group(1) in self.patterns
                      else m.group(0), value or "")

    def expand_globs(self, globs):
        special = {"@entryPoints": "entryPointGlobs", "@apiSpecs": "apiSpecGlobs", "@webServers": "webServerGlobs",
                   "@iac": "iacGlobs"}
        out = []
        for g in globs:
            out += self.cfg[special[g]] if g in special else [g]
        return out

    def usable(self, files, tests="exclude", subject_iac_only=False, include_excluded=False):
        out = []
        for f in files:
            if (f in self.dropped or f in self.generated) and not include_excluded:
                continue
            if not self.advanced and f in self.iac:
                continue
            is_test = f in self.tests
            if (tests == "exclude" and is_test) or (tests == "only" and not is_test):
                continue
            out.append(f)
        return out

    def tier_files(self, tier, iac_only=False):
        t = self.t
        if tier.get("testFiles"):
            pool = list(self.test_source)
        elif tier.get("globs"):
            globs = self.expand_globs(tier["globs"])
            pool = t.match(globs)
            if "@iac" in tier["globs"]:
                pool = sorted(set(pool) | (self.iac if self.advanced else set()))
            if tier.get("source"):
                src = set(self.source)
                pool = [f for f in pool if f in src]
        elif tier.get("source"):
            pool = list(self.source)
        else:
            pool = []
        pool = self.usable(pool, tier.get("tests", "exclude"), iac_only, bool(tier.get("includeExcluded")))
        if tier.get("exclude"):
            ex = set(t.match(tier["exclude"], pool))
            pool = [f for f in pool if f not in ex]
        if tier.get("contains"):
            pool = t.grep(self.pat(tier["contains"]), pool)
        name = lambda f: f.rsplit("/", 1)[-1]
        pool.sort(key=lambda f: (name(f) in LOW_VALUE, bool(tier.get("testFiles")) and not TEST_NAME_RE.match(name(f)),
                                 f.count("/"), f))
        if tier.get("perProject"):
            pool = spread(pool, key=self.test_group)
        elif tier.get("perDir"):
            pool = spread(pool, key=lambda f: f.rsplit("/", 1)[0] if "/" in f else ".")
        return pool

    def test_group(self, rel):
        parts = rel.split("/")
        proj_dirs = self.project_dirs()
        for i in range(len(parts) - 1, 0, -1):
            d = "/".join(parts[:i])
            if d in proj_dirs and TEST_DIR_RE.match(parts[i - 1]):
                return d
        for i, seg in enumerate(parts[:-1]):
            if TEST_DIR_RE.match(seg):
                return "/".join(parts[:i + 1])
        return "/".join(parts[:-1]) or "."

    def project_dirs(self):
        if not hasattr(self, "_proj"):
            self._proj = {f.rsplit("/", 1)[0] if "/" in f else "." for f in self.t.files if PROJECT_FILES.search(f)}
        return self._proj

    # -- detection
    def languages(self):
        return [lang for lang, globs in self.cfg["languages"].items() if self.t.match(globs)]

    def frameworks(self):
        found, web = [], False
        for fw in self.cfg["frameworks"]:
            if self.t.grep(fw["contains"], self.t.match(fw["globs"])):
                found.append(fw["name"])
                web = web or fw.get("web", False)
        return found, web

    def entry_points(self):
        return self.usable([f for f in self.t.match(self.cfg["entryPointGlobs"]) if f in set(self.source)])

    def api_specs(self):
        files = self.usable(self.t.match(self.cfg["apiSpecGlobs"]), tests="include")
        return self.t.grep(r"[\"']?(?:openapi|swagger)[\"']?\s*:", files)

    def routes(self):
        return self.t.grep(self.patterns["route"], self.prod_source)

    def mcp_servers(self):
        m = self.cfg["mcp"]
        servers = {}
        for rule in m["manifests"]:
            for man in self.t.match(rule["globs"]):
                if man in self.tests:
                    continue
                hit = rx(rule["contains"]).search(self.t.text(man))
                if not hit:
                    continue
                root = man.rsplit("/", 1)[0] if "/" in man else "."
                under = [f for f in self.prod_source if root == "." or f.startswith(root + "/")]
                code = self.t.grep(m["server"], under)
                if not code:
                    continue
                sdk = hit.group(1) + (f" {hit.group(2)}" if hit.lastindex and hit.lastindex >= 2 and hit.group(2) else "")
                cfg_files = [f for f in self.t.files if (root == "." or f.startswith(root + "/"))
                             and re.search(r"application[^/]*\.(?:properties|ya?ml)$", f)]
                transports = []
                if self.t.grep(m["stdio"], code + cfg_files):
                    transports.append("stdio")
                if self.t.grep(m["http"], code + cfg_files):
                    transports.append("http")
                servers.setdefault(root, {"path": root, "language": rule["language"], "sdk": sdk,
                                          "transports": transports or ["stdio"]})
        return sorted(servers.values(), key=lambda s: s["path"])

    def folder_listing(self):
        top, second = set(), set()
        for f in self.t.files:
            parts = f.split("/")
            top.add(parts[0] + ("/" if len(parts) > 1 else ""))
            if len(parts) > 2:
                second.add(f"{parts[0]}/{parts[1]}/")
        listing = sorted(top) + sorted(second)
        return listing[:MAX_FOLDER_LISTING]

    def production_roots(self):
        roots = set()
        for f in self.t.files:
            if not PROJECT_FILES.search(f) or f in self.tests or f in self.iac:
                continue
            d = f.rsplit("/", 1)[0] if "/" in f else "."
            if any(TEST_DIR_RE.match(seg) for seg in d.split("/") if seg != "."):
                continue
            roots.add(d)
        if not roots and self.prod_source:
            roots.add(".")
        return sorted(roots)

    def test_inventory(self, subject_cfg):
        groups = {}
        for f in self.test_source:
            groups.setdefault(self.test_group(f), []).append(f)
        cats, names = self.cfg["testCategories"], self.cfg["testNames"]
        projects, totals = [], {"unit": 0, "integration": 0, "e2e": 0, "unclassified": 0}
        for path in sorted(groups):
            files = groups[path]
            extra = [g for g in self.t.files if PROJECT_FILES.search(g) and (g.rsplit("/", 1)[0] if "/" in g else ".") == path]
            text = "\n".join(self.t.text(f) for f in files + extra)
            present = [c for c in ("e2e", "integration", "unit") if rx(cats[c]).search(text)]
            named = [c for c in present if rx(names[c]).search(path)]
            cat = named[0] if named else (present[0] if present else "unclassified")
            projects.append({"path": path, "category": cat, "files": len(files)})
            totals[cat] += len(files)
        tiers = {t["name"]: t for t in subject_cfg["tiers"]}
        sig = self.cfg["signals"]
        prod_cfg = self.usable(self.t.match(["appsettings*.json", "application*.{yml,yaml,properties}", "settings*.py"]))
        signals = {
            "accessControl": bool(self.t.grep(self.pat(sig["accessControl"]), self.prod_source + prod_cfg)),
            "integrationPoints": bool(self.t.grep(self.pat(sig["integrationPoints"]), self.prod_source)),
            "untrustedInput": bool(self.t.grep(self.pat(sig["untrustedInput"]), self.prod_source)),
            "loadTests": bool(self.tier_files(tiers["load tests"])) if "load tests" in tiers else False,
            "faultInjection": bool(self.tier_files(tiers["resilience and fault-injection tests"]))
            if "resilience and fault-injection tests" in tiers else False,
        }
        return {"testProjects": projects, "totals": totals, "productionRoots": self.production_roots(),
                "signals": signals}

    def subject_files(self, skill, cap):
        scfg = self.cfg["subjects"][skill]
        tiers = [self.tier_files(t, scfg.get("iacOnly", False)) for t in scfg["tiers"]]
        matched, seen = [], set()
        for files in tiers:
            for f in files:
                if f not in seen:
                    seen.add(f)
                    matched.append(f)
        if len(matched) <= cap:
            return matched, None
        picked, seen = [], set()
        for tier, files in zip(scfg["tiers"], tiers):
            take = [f for f in files if f not in seen][:tier.get("max", cap)]
            for f in take:
                if len(picked) >= cap:
                    break
                picked.append(f)
                seen.add(f)
        for f in matched:
            if len(picked) >= cap:
                break
            if f not in seen:
                picked.append(f)
                seen.add(f)
        return picked, {"totalMatched": len(matched), "candidates": matched[:MAX_CANDIDATES]}


def spread(files, key):
    """Round-robin over groups (in first-seen order) so the first files cover as many groups as possible."""
    groups, order = {}, []
    for f in files:
        k = key(f)
        if k not in groups:
            groups[k] = []
            order.append(k)
        groups[k].append(f)
    out, i = [], 0
    while len(out) < len(files):
        for k in order:
            if i < len(groups[k]):
                out.append(groups[k][i])
        i += 1
    return out


def make_batches(subject_lists, max_files=20, max_subjects=5, overlap=0.7):
    """Group applicable subjects per compliance-inventory SKILL.md step 7 (each subject in exactly one batch)."""
    order = sorted(subject_lists, key=lambda s: (-len(subject_lists[s]), s))
    batches = []
    for skill in order:
        files = subject_lists[skill]
        placed = False
        for b in batches:
            union = b["files"] | set(files)
            shared = sum(1 for f in files if f in b["files"])
            ratio = shared / len(files) if files else 1.0  # a subject with no files adds nothing to read
            if ratio >= overlap and len(union) <= max_files and len(b["subjects"]) < max_subjects:
                b["subjects"].append(skill)
                b["files"] = union
                placed = True
                break
        if not placed:
            batches.append({"subjects": [skill], "files": set(files)})
    out = []
    for i, b in enumerate(batches, 1):
        out.append({"batchId": f"batch-{i}", "subjects": b["subjects"],
                    "subjectFiles": {s: subject_lists[s] for s in b["subjects"]}})
    return out


def build_inventory(root, subjects, advanced, picks=None, cfg=None):
    """The step-01 content (without the transition header) for the chosen subjects."""
    inv = Inventory(root, advanced, cfg)
    cfg = inv.cfg
    cap = cfg["maxFilesPerSubject"]
    languages = inv.languages()
    frameworks, web_fw = inv.frameworks()
    specs, routes = inv.api_specs(), inv.routes()
    api_found = bool(specs or routes)
    servers = inv.mcp_servers()
    mcp_found = bool(servers)
    web_servers = inv.usable(inv.t.match(cfg["webServerGlobs"]))
    http_surface = api_found or web_fw or bool(web_servers) or any("http" in s["transports"] for s in servers)
    iac_found = bool(advanced) and bool(inv.usable(sorted(inv.iac), tests="include"))
    scan = sensitive_candidates(inv)
    skipped = {}
    for skill in subjects:
        scfg = cfg["subjects"].get(skill)
        if scfg is None:
            raise ValueError(f"unknown subject {skill}")
        if scfg.get("iacOnly"):
            if not advanced:
                skipped[skill] = "advanced usage off (IaC not reviewed)"
            elif not iac_found:
                skipped[skill] = "no infrastructure-as-code found"
        if skill == "review-mcp-server" and not mcp_found:
            skipped[skill] = "no MCP server found"
        if skill in ("review-api-design", "review-security-web-api") and mcp_found and not http_surface:
            skipped[skill] = "no HTTP surface (stdio-only MCP server)"
        elif skill == "review-api-design" and not api_found:
            skipped[skill] = "no API found"
        if skill == "review-data-protection" and not scan["personalDataFound"]:
            skipped[skill] = "no personal data found"
    lists, meta = {}, {}
    picks = picks or {}
    for skill in subjects:
        if skill in skipped:
            continue
        files, sample = inv.subject_files(skill, cap)
        if skill in picks:
            chosen = [p.replace("\\", "/").lstrip("./") if p.startswith("./") else p.replace("\\", "/") for p in picks[skill]]
            known = set(inv.t.files)
            bad = [p for p in chosen if p not in known]
            if bad:
                raise ValueError(f"picks for {skill}: not in the target's file list: {', '.join(bad)}")
            if len(chosen) > cap:
                raise ValueError(f"picks for {skill}: {len(chosen)} files, cap is {cap}")
            files = chosen
            sample = dict(sample or {"totalMatched": len(chosen), "candidates": chosen}, picked=True)
        lists[skill] = files
        meta[skill] = sample
    batches = make_batches(lists)
    batch_of = {s: b["batchId"] for b in batches for s in b["subjects"]}
    subj = {}
    for skill in subjects:
        if skill in skipped:
            subj[skill] = {"batch": None, "applicable": False}
            continue
        entry = {"batch": batch_of[skill], "applicable": True, "fileCount": len(lists[skill])}
        if meta[skill]:
            entry.update(sampled=True, totalMatched=meta[skill]["totalMatched"])
            if meta[skill].get("picked"):
                entry["picked"] = True
        subj[skill] = entry
    out = {
        "generator": "compliance_report.py inventory",
        "languages": languages,
        "frameworks": frameworks,
        "entryPoints": inv.entry_points()[:20],
        "apiSpecsFound": api_found,
        "apiSpecs": specs[:10],
        "mcpFound": mcp_found,
        "mcpServers": servers,
        "httpSurfaceFound": http_surface,
        "advanced": bool(advanced),
        "iacFound": iac_found,
        "maxFilesPerSubject": cap,
        "fileBatches": batches,
        "subjects": subj,
        "skippedSubjects": skipped,
        "folderListing": inv.folder_listing(),
        "sampling": {s: {"totalMatched": m["totalMatched"], "candidates": m["candidates"]}
                     for s, m in meta.items() if m and not m.get("picked")},
        "targetFiles": len(inv.t.files),
        "targetTruncated": inv.t.truncated,
        **scan,
    }
    if "review-testing" in subjects:
        out["testInventory"] = inv.test_inventory(cfg["subjects"]["review-testing"])
    return out


def sensitive_candidates(inv):
    """Secret and personal-data candidates (file, line, rule, confidence; never the value) and `personalDataFound`.

    Every walked text file is scanned for secrets, except IaC files when advanced usage is off. Test, fixture,
    seed and sample files are also scanned for personal data.
    """
    import sensitive_scan  # noqa: E402
    rules = sensitive_scan.load()
    t = inv.t
    files = [f for f in t.files if inv.advanced or f not in inv.iac]
    scope = inv.tests | inv.dropped | set(t.match(rules.pii_scope))
    pii_files = [f for f in files if f in scope]
    secrets, s_total, pii, p_total = sensitive_scan.scan_target(t, files, pii_files, rules)
    found, signals = sensitive_scan.personal_data_signals(inv, pii, rules)
    return {"secretCandidates": secrets, "secretCandidatesTotal": s_total,
            "piiCandidates": pii, "piiCandidatesTotal": p_total,
            "personalDataFound": found, "personalDataSignals": signals}


def lint_map(cfg=None):
    """Problems in subject-file-map.json: bad regexes, unknown pattern references, unknown subjects."""
    cfg = cfg or load_map()
    problems = []
    names = set(cfg["patterns"])

    def check_regex(where, value, refs=True):
        for ref in re.findall(r"@(\w+)", value or "") if refs else []:
            if ref not in names:
                problems.append(f"{where}: unknown pattern @{ref}")
        try:
            re.compile(re.sub(r"@(\w+)", lambda m: f"(?:{cfg['patterns'][m.group(1)]})" if m.group(1) in names
                              else m.group(0), value or ""))
        except re.error as e:
            problems.append(f"{where}: bad regex: {e}")

    for name, value in cfg["patterns"].items():
        check_regex(f"patterns.{name}", value, refs=False)
    for skill, scfg in cfg["subjects"].items():
        for t in scfg["tiers"]:
            where = f"subjects.{skill}.{t.get('name')}"
            if not (t.get("globs") or t.get("source") or t.get("testFiles")):
                problems.append(f"{where}: no globs, source or testFiles")
            if t.get("contains"):
                check_regex(where, t["contains"])
            for g in t.get("globs", []):
                if g.startswith("@") and g not in ("@entryPoints", "@apiSpecs", "@webServers", "@iac"):
                    problems.append(f"{where}: unknown glob list {g}")
                else:
                    try:
                        glob_regex(g)
                    except (ValueError, re.error) as e:
                        problems.append(f"{where}: bad glob {g}: {e}")
    return problems
