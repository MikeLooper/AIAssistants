"""Localized-standards helpers for compliance_report.py (standard library only).

Two jobs, both driven by the skills' own Markdown files so nothing is duplicated:

* **Citations.** Workers cite a standards element by ID only (`Finding.element`, e.g. `AZ-031`). The
  report script resolves `standard` ("<source name> — <element ID>") and `url` from the element's row and
  the citation metadata in its standards file header ("Source name for `Finding.standard`", "Citation base",
  the page-key table and the Anchor(s)/Page/PDF page columns).
* **Review packs.** One generated Markdown file per skill (`compliance-reviewer/packs/<skill>.md`) and per
  skill and language (`<skill>.<lang>.md`), holding what a worker needs: SKILL.md, checklist.md, the
  standards rows without citation columns, and the skill's other reference files. `packs check` flags a pack
  that no longer matches its sources.
"""
import hashlib
import os
import re

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.normpath(os.path.join(SCRIPTS_DIR, "..", ".."))
REVIEWER_DIR = os.path.normpath(os.path.join(SKILLS_DIR, ".."))
REPO_ROOT = os.path.normpath(os.path.join(REVIEWER_DIR, ".."))
PACKS_DIR = os.path.join(REVIEWER_DIR, "packs")
LANGUAGES = ("csharp", "java", "python", "javascript")

ELEMENT_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+$")
ANCHOR_TAG_RE = re.compile(r'<a id="([^"]+)"></a>')
URL_RE = re.compile(r"https?://[^\s`)>]+")


def _read(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def split_row(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def _is_sep(line):
    return bool(re.match(r"^\s*\|[\s:|-]+\|\s*$", line))


def tables(lines):
    """Yield (start, end, header_cells, rows) for every Markdown table; rows are (lineno, cells)."""
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and _is_sep(lines[i + 1]):
            header = split_row(lines[i])
            j, rows = i + 2, []
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append((j, split_row(lines[j])))
                j += 1
            yield i, j, header, rows
            i = j
        else:
            i += 1


def _unquote(text):
    text = text.strip()
    m = re.match(r"^`([^`]+)`", text)
    if m:
        return m.group(1).strip()
    m = re.match(r'^"([^"]+)"', text)
    if m:
        return m.group(1).strip()
    return text.strip("*").strip()


def _bullets(lines):
    """Top-level '- ' bullets of the file header (before the first table), continuation lines joined."""
    out, cur = [], None
    for line in lines:
        if line.lstrip().startswith("|"):
            break
        if line.startswith("- "):
            cur = [line[2:].strip()]
            out.append(cur)
        elif cur is not None and line.startswith("  ") and line.strip():
            cur.append(line.strip())
        elif not line.strip():
            cur = None
    return out


def element_id(cell):
    """(element ID, explicit anchor or None, retired?) from an ID cell, or None when the cell holds no ID."""
    anchor = ANCHOR_TAG_RE.search(cell)
    text = ANCHOR_TAG_RE.sub("", cell).strip()
    retired = "(retired" in text.lower()
    text = re.sub(r"\s*\(retired.*$", "", text, flags=re.I).strip()
    if not ELEMENT_RE.match(text):
        return None
    return text, anchor.group(1) if anchor else None, retired


# ---------------------------------------------------------------- citations

class StandardsFile:
    """Citation metadata and element rows of one `references/standards/<name>.md` file."""

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.lines = _read(path).splitlines()
        self.default_name = None      # header "Source name for `Finding.standard`"
        self.name_ranges = []         # PEP-style: [(name, prefix, first, last)]
        self.src_names = {}           # Src column letter -> source name
        self.base = ""                # header "Citation base"
        self.bases = {}               # sub-bullet "`key` → url" (OAS versions, MCP pages)
        self.template = None          # "Citation: `https://…/<page path>#solution`"
        self.keys = {}                # page-key table: key -> {"url", "path", "name"}
        self.elements = {}            # ID -> {"cells": {col: value}, "anchor": str|None, "retired": bool}
        self._parse()

    def _parse(self):
        for parts in _bullets(self.lines):
            text = " ".join(parts)
            low = text.lower()
            if low.startswith("source name"):
                value = text.split(":", 1)[1].strip() if ":" in text else ""
                ranges = re.findall(r'"([^"]+)"\s*\(([A-Z][A-Z0-9]*)-(\d+)\s*…\s*[A-Z][A-Z0-9]*-(\d+)\)', value)
                if ranges:
                    self.name_ranges = [(n, p, int(a), int(b)) for n, p, a, b in ranges]
                letters = re.findall(r"\*\*([A-Z])\*\*\s*=\s*`([^`]+)`", value)
                if letters:
                    self.src_names = dict(letters)
                elif not ranges and not value.lower().startswith(("the source name", "**per row**", "per row")):
                    self.default_name = _unquote(value) or None
            elif low.startswith("citation base"):
                m = re.search(r"\):\s*(.*)$", text) or re.search(r"^[^:]*:\s*(.*)$", text)
                value = m.group(1) if m else ""
                url = URL_RE.search(value)
                tick = re.search(r"`([^`]+)`", value)
                if url and (not tick or value.find(url.group(0)) < value.find(tick.group(0))):
                    self.base = url.group(0).rstrip(".,;")
                elif tick:
                    self.base = tick.group(1)
                for sub in parts[1:]:
                    m2 = re.match(r"^-\s*`([^`]+)`\s*→\s*(\S+)", sub)
                    if m2:
                        self.bases[m2.group(1)] = m2.group(2)
            elif low.startswith("citation:") and "<page path>" in text:
                m = re.search(r"`([^`]*<page path>[^`]*)`", text)
                if m:
                    self.template = m.group(1)
        for _s, _e, header, rows in tables(self.lines):
            cols = [h.lower() for h in header]
            if cols and cols[0] == "key":
                for _n, cells in rows:
                    rec = dict(zip(cols, cells))
                    key = rec.get("key", "").strip("`")
                    url = next((v for k, v in rec.items() if k in ("citation base", "url")), "")
                    path = rec.get("page path", "")
                    name = next((v for k, v in rec.items() if k.startswith("source name")), "")
                    self.keys[key] = {"url": url.strip("`"), "path": path, "name": name}
            elif cols and cols[0] == "id":
                for _n, cells in rows:
                    parsed = element_id(cells[0]) if cells else None
                    if not parsed:
                        continue
                    eid, anchor, retired = parsed
                    rec = dict(zip(cols, cells))
                    retired = retired or any(str(v).startswith("*(retired") for v in rec.values())
                    self.elements[eid] = {"cells": rec, "anchor": anchor, "retired": retired}

    # -- resolution helpers
    def _source_name(self, eid, rec, key):
        row_name = rec.get("source name", "").strip()
        if row_name:
            return row_name
        src = rec.get("src", "").strip()
        if src and src in self.src_names:
            return self.src_names[src]
        if key and key in self.keys and self.keys[key]["name"]:
            return self.keys[key]["name"]
        m = re.match(r"^([A-Z][A-Z0-9]*)-(\d+)$", eid)
        if m:
            for name, prefix, a, b in self.name_ranges:
                if prefix == m.group(1) and a <= int(m.group(2)) <= b:
                    return name
        return self.default_name or ""

    @staticmethod
    def _join(base, path):
        path = re.sub(r"\s*\(.*$", "", path.strip().strip("`")).strip().strip("`")
        if not path or path == "/":
            return base
        if re.match(r"^https?://", path):
            return path
        if path.startswith(("?", "#")):
            return base + path
        return base.rstrip("/") + "/" + path.lstrip("/") if base else path

    def _key_url(self, key):
        info = self.keys[key]
        if info["url"]:
            return info["url"]
        raw = info["path"]
        if "(citation base)" in raw:
            return self.base
        m = re.search(r"full path from (https?://\S+?)\)?$", raw)
        if m:
            return self._join(m.group(1), raw)
        return self._join(self.base, raw)

    def resolve(self, eid, page=None):
        """(standard, url) for one element, or None when the element isn't in this file."""
        el = self.elements.get(eid)
        if el is None:
            return None
        rec = el["cells"]
        anchor_cell = next((v for k, v in rec.items() if k in ("anchor(s)", "anchor")), "")
        page_cell = next((v for k, v in rec.items() if k in ("page", "page path")), "")
        page_cell = re.split(r",\s*", page_cell.strip())[0].strip().strip("`")
        pdf_cell = rec.get("pdf page", "")
        first = re.split(r",\s*", anchor_cell.strip())[0].strip().strip("`") if anchor_cell.strip() else ""
        key, frag = None, None
        if el["anchor"]:
            frag = el["anchor"]
        elif first and first not in ("—", "-", "(page)") and not first.startswith("§"):
            if "#" in first:
                key, frag = first.split("#", 1)
                key = key or None
            elif first in self.keys or first in self.bases:
                key = first
            else:
                frag = first
        if key is None and page_cell and (page_cell in self.keys or page_cell in self.bases):
            key = page_cell
        name = self._source_name(eid, rec, key)
        # base URL
        if pdf_cell and re.search(r"\d+", pdf_cell):
            url = f"{self.base}#page={re.search(r'\d+', pdf_cell).group(0)}"
            return self._standard(name, eid), url
        if key and key in self.keys:
            base = self._key_url(key)
        elif key and key in self.bases:
            base = self.bases[key]
        elif key:  # an anchor key the file doesn't define: a page under a folder base, else the base page
            base = self._join(self.base, key) + "/" if self.base.endswith("/") else self.base
        elif self.template and page_cell:
            return self._standard(name, eid), self.template.replace("<page path>", page_cell.split(",")[0].strip())
        elif page_cell and not self.bases:
            base = self._join(self.base, page_cell)
        elif self.bases:
            base = self.bases.get(page) or next(iter(self.bases.values()))
        else:
            base = self.base
        if frag:
            frag = re.sub(r"\s*\(.*$", "", frag).strip().strip("`")
            frag = None if re.search(r"\s", frag) else frag  # "item 8", "§3.1": no anchor of its own
        url = base + (f"#{frag}" if frag else "") if base else ""
        standard = self._standard(name, eid)
        if re.match(r"^(?:§\s*\d|item \d)", first):  # pages without anchors: name the section or item instead
            standard += f" ({first})"
        return standard, url

    @staticmethod
    def _standard(name, eid):
        return f"{name} — {eid}" if name else eid


_INDEX = {}


def standards_files(skill):
    folder = os.path.join(SKILLS_DIR, skill, "references", "standards")
    if not os.path.isdir(folder):
        return []
    return [os.path.join(folder, n) for n in sorted(os.listdir(folder))
            if n.endswith(".md") and n != "MAINTENANCE.md"]


def skill_index(skill):
    """{element ID: StandardsFile} for one skill (cached)."""
    if skill not in _INDEX:
        idx = {}
        for path in standards_files(skill):
            sf = StandardsFile(path)
            for eid in sf.elements:
                idx.setdefault(eid, sf)
        _INDEX[skill] = idx
    return _INDEX[skill]


def all_skills():
    return sorted(n for n in os.listdir(SKILLS_DIR) if n.startswith("review-")
                  and os.path.isdir(os.path.join(SKILLS_DIR, n)))


def resolve(skill, eid, page=None):
    """(standard, url) for an element cited by a finding of `skill`; other skills are searched as a fallback."""
    eid = (eid or "").strip()
    if not eid:
        return None
    sf = skill_index(skill).get(eid)
    if sf is None:
        for other in all_skills():
            sf = skill_index(other).get(eid)
            if sf is not None:
                break
    if sf is None:
        return None
    standard, url = sf.resolve(eid, page)
    if url and not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:|^[/#]", url):
        url = url.replace("\\", "/")
    return standard, url


def citations_lint(skills=None):
    """Problems with element citation data: unresolvable elements and duplicate IDs within a skill."""
    problems = []
    for skill in skills or all_skills():
        seen = {}
        for path in standards_files(skill):
            sf = StandardsFile(path)
            rel = os.path.relpath(path, SKILLS_DIR).replace("\\", "/")
            for eid, el in sf.elements.items():
                if eid in seen:
                    problems.append({"file": rel, "problem": f"{eid} also defined in {seen[eid]}"})
                seen[eid] = sf.name
                if el["retired"]:
                    continue
                standard, url = sf.resolve(eid)
                if standard == eid:
                    problems.append({"file": rel, "problem": f"{eid}: no source name"})
                if not url:
                    problems.append({"file": rel, "problem": f"{eid}: no citation URL"})
                elif re.search(r"\s", url):
                    problems.append({"file": rel, "problem": f"{eid}: citation URL contains whitespace: {url}"})
    return problems


# ---------------------------------------------------------------- review packs

DROP_COLUMNS = {"anchor(s)", "anchor", "page", "page path", "src", "source name", "pdf page", "pin"}
DROP_BULLETS = ("source", "sources", "source site", "source name", "source names", "pinned", "citation",
                "localized", "retrieved", "version:", "anchor", "anchors", "page path", "pdf page", "text sha")
GENERATED_MARK = "<!-- GENERATED by compliance_report.py packs build. Do not edit; edit the sources and rebuild. -->"


def _demote(text, levels=1):
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,5} ", line):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out)


def _strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def compact_standards(path):
    """A standards file without citation metadata: header pin/citation bullets, page-key tables, citation
    columns and retired rows are left out. Everything else (legends, rules, element rows) is kept."""
    lines = _read(path).splitlines()
    spans = {s: (e, h, rows) for s, e, h, rows in tables(lines)}
    out, i, skip_bullet = [], 0, False
    first_table = next(iter(sorted(spans)), len(lines))
    while i < len(lines):
        line = lines[i]
        if i in spans:
            end, header, rows = spans[i]
            cols = [h.lower() for h in header]
            if cols and cols[0] == "key":
                i = end
                continue
            keep = [k for k, c in enumerate(cols) if c not in DROP_COLUMNS] if cols and cols[0] == "id" else \
                list(range(len(cols)))
            out.append("| " + " | ".join(header[k] for k in keep) + " |")
            out.append("|" + "|".join("---" for _ in keep) + "|")
            for _n, cells in rows:
                if cols and cols[0] == "id":
                    parsed = element_id(cells[0]) if cells else None
                    if parsed and (parsed[2] or any(c.startswith("*(retired") for c in cells)):
                        continue
                    cells = [ANCHOR_TAG_RE.sub("", c) for c in cells]
                cells = cells + [""] * (len(cols) - len(cells))
                out.append("| " + " | ".join(cells[k] for k in keep) + " |")
            i = end
            continue
        if i < first_table:
            if line.startswith("- "):
                skip_bullet = line[2:].strip().lower().startswith(DROP_BULLETS)
                if skip_bullet:
                    i += 1
                    continue
            elif line.startswith("  ") and line.strip() and skip_bullet:
                i += 1
                continue
            elif not line.strip():
                skip_bullet = False
        out.append(line)
        i += 1
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


LANG_WORDS = {"csharp": ("csharp", "c#"), "java": ("java",), "python": ("python",),
              "javascript": ("javascript", "javascript/typescript", "typescript")}


def standards_plan(skill):
    """[(relative path, load note, language or None)] from the SKILL.md `## Standards` section."""
    text = _read(os.path.join(SKILLS_DIR, skill, "SKILL.md"))
    m = re.search(r"^## Standards[^\n]*\n(.*?)(?=^## )", text, flags=re.M | re.S)
    plan, listed = [], set()
    if m:
        for bullet in re.split(r"\n(?=- )", m.group(1)):
            fm = re.match(r"^- `(references/standards/[^`]+\.md)`[:\s—-]*(.*)", bullet.strip(), flags=re.S)
            if not fm:
                continue
            rel, note = fm.group(1), " ".join(fm.group(2).split())
            lang = None
            lm = re.search(r"language `(\w+)`", note) or re.search(r"only if ([\w#/]+) is detected", note, flags=re.I)
            if lm:
                word = lm.group(1).lower()
                lang = next((k for k, v in LANG_WORDS.items() if word in v), None)
            plan.append((rel, note, lang))
            listed.add(os.path.basename(rel))
    for path in standards_files(skill):  # files on disk the section doesn't name still go in the core pack
        if os.path.basename(path) not in listed:
            plan.append((os.path.relpath(path, os.path.join(SKILLS_DIR, skill)).replace("\\", "/"), "", None))
    return plan


def other_references(skill):
    ref = os.path.join(SKILLS_DIR, skill, "references")
    if not os.path.isdir(ref):
        return []
    return [f"references/{n}" for n in sorted(os.listdir(ref))
            if n.endswith(".md") and n not in ("checklist.md", "sources.md")]


def pack_sources(skill):
    """{pack name: [(relative source path, section heading note)]} for one skill."""
    packs = {skill: [("SKILL.md", ""), ("references/checklist.md", "")]}
    for rel in other_references(skill):
        packs[skill].append((rel, ""))
    plan = standards_plan(skill)
    for rel, note, lang in plan:
        if lang is None:
            packs[skill].append((rel, note))
    for lang in LANGUAGES:
        items = []
        lang_file = f"references/languages/{lang}.md"
        if os.path.exists(os.path.join(SKILLS_DIR, skill, lang_file)):
            items.append((lang_file, ""))
        items += [(rel, note) for rel, note, lg in plan if lg == lang]
        if items:
            packs[f"{skill}.{lang}"] = items
    return packs


def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def build_pack(skill, name, items):
    base = os.path.join(SKILLS_DIR, skill)
    lang = name.split(".", 1)[1] if "." in name else None
    lines = [GENERATED_MARK, "<!-- sources: " + ", ".join(f"{rel}@{_sha(os.path.join(base, rel))}" for rel, _ in items)
             + " -->", ""]
    if lang:
        lines += [f"# Review pack: {skill} ({lang})", "",
                  f"Language-specific part of the `{skill}` pack, for targets where `{lang}` is detected. "
                  f"Read it together with `packs/{skill}.md`.", ""]
    else:
        lines += [f"# Review pack: {skill}", "",
                  "Everything a worker needs for this skill, in one file: `SKILL.md`, `references/checklist.md`, the "
                  "skill's other reference files and its language-neutral standards. Language-specific standards and "
                  f"signals are in `packs/{skill}.<language>.md`. Where the instructions below say to load one of "
                  "these files, use its section here instead; don't open the original. Citation columns (anchors, "
                  "pages, source names) are left out: cite an element by its ID in `Finding.element` and the report "
                  "script fills in `standard` and `url`. `sources.md` is maintainer material and is not included.", ""]
    for rel, note in items:
        path = os.path.join(base, rel)
        text = _read(path)
        if rel == "SKILL.md":
            text = _strip_frontmatter(text)
        elif rel.startswith("references/standards/"):
            text = compact_standards(path)
        lines += ["---", "", f"## File: `{rel}`", ""]
        if note:
            lines += [f"*Load rule: {note}*", ""]
        lines += [_demote(text.strip(), 2), ""]
    return "\n".join(lines).rstrip() + "\n"


def packs_for(skills=None):
    out = {}
    for skill in skills or all_skills():
        for name, items in pack_sources(skill).items():
            out[name] = (skill, items)
    return out


def packs_build(skills=None):
    os.makedirs(PACKS_DIR, exist_ok=True)
    written = []
    wanted = packs_for(skills)
    for name, (skill, items) in wanted.items():
        path = os.path.join(PACKS_DIR, f"{name}.md")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(build_pack(skill, name, items))
        written.append(os.path.relpath(path, REPO_ROOT).replace("\\", "/"))
    if not skills:  # a full build also removes packs whose skill or language file is gone
        for n in os.listdir(PACKS_DIR):
            if n.endswith(".md") and n[:-3] not in wanted and n != "README.md":
                os.remove(os.path.join(PACKS_DIR, n))
    return written


def packs_check(skills=None):
    """Problems: packs that are missing, out of date with their sources, or orphaned."""
    problems = []
    wanted = packs_for(skills)
    for name, (skill, items) in wanted.items():
        path = os.path.join(PACKS_DIR, f"{name}.md")
        rel = os.path.relpath(path, REPO_ROOT).replace("\\", "/")
        if not os.path.exists(path):
            problems.append({"file": rel, "problem": "missing pack (run `packs build`)"})
        elif _read(path) != build_pack(skill, name, items):
            problems.append({"file": rel, "problem": "out of date with its sources (run `packs build`)"})
    if not skills and os.path.isdir(PACKS_DIR):
        for n in sorted(os.listdir(PACKS_DIR)):
            if n.endswith(".md") and n[:-3] not in wanted and n != "README.md":
                problems.append({"file": f"compliance-reviewer/packs/{n}", "problem": "orphaned pack (no source skill/language)"})
    return problems


def pack_paths(skill, languages):
    """Repo-relative pack files a worker reads for `skill` on a target with these languages (existing only)."""
    out = []
    for name in [skill] + [f"{skill}.{lang}" for lang in languages]:
        path = os.path.join(PACKS_DIR, f"{name}.md")
        if os.path.exists(path):
            out.append(os.path.relpath(path, REPO_ROOT).replace("\\", "/"))
    return out
