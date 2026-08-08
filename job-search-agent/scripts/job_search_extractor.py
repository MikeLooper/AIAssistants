from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover
    sync_playwright = None
    PlaywrightTimeoutError = Exception


@dataclass
class AliasTerm:
    discover: str
    report: str


@dataclass
class ExtractedJob:
    source_url: str
    source_site: str
    job_url: str
    attributes: dict[str, str]


def read_non_comment_lines(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def read_alias_terms(path: Path) -> list[AliasTerm]:
    out: list[AliasTerm] = []
    for line in read_non_comment_lines(path):
        if ":" in line:
            left, right = line.split(":", 1)
            out.append(AliasTerm(discover=left.strip(), report=right.strip()))
        else:
            out.append(AliasTerm(discover=line.strip(), report=line.strip()))
    return out


def detect_site(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    for prefix in ("www.", "m.", "jobs.", "careers."):
        if host.startswith(prefix):
            host = host[len(prefix) :]
    if host.endswith("dice.com"):
        return "Dice"
    if host.endswith("linkedin.com"):
        return "LinkedIn"
    if host.endswith("glassdoor.com"):
        return "Glassdoor"
    if host.endswith("greenhouse.io"):
        return "Greenhouse"
    if host.endswith("remotive.com"):
        return "Remotive"
    return "Generic"


def text_or_empty(value: str | None) -> str:
    return value.strip() if isinstance(value, str) else ""


def extract_terms(text: str, aliases: list[AliasTerm], is_language: bool = False) -> str:
    found: list[str] = []
    hay = text.lower()
    for alias in aliases:
        discover = alias.discover.strip()
        if not discover:
            continue
        if is_language and discover.lower() == "go":
            pattern = r"\bgolang\b"
        else:
            pattern = r"(?<!\w)" + re.escape(discover.lower()) + r"(?!\w)"
        if re.search(pattern, hay, flags=re.IGNORECASE) and alias.report not in found:
            found.append(alias.report)
    return ", ".join(found)


def extract_salary(text: str) -> str:
    patterns = [
        r"\$[\d,]+(?:\.\d+)?[kK]?\s*(?:to|-|–|—)\s*\$[\d,]+(?:\.\d+)?[kK]?",
        r"\b\d{2,3}[kK]\s*(?:to|-|–|—)\s*\d{2,3}[kK]\b",
        r"\$[\d,]{6,}\s*(?:to|-|–|—)\s*\$[\d,]{6,}",
        r"[Uu]p\s+to\s+\$[\d,]+(?:\.\d+)?[kK]?",
        r"\$[\d,]+(?:\.\d+)?[kK]?\+",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return ""


def ordered_attributes(requested: list[str], values: dict[str, str]) -> dict[str, str]:
    canonical = ["Job Title", "Programming Language", "Tools", "Salary Range"]
    ordered_keys: list[str] = []
    for key in canonical:
        if key in values:
            ordered_keys.append(key)
    for key in requested:
        if key in values and key not in ordered_keys:
            ordered_keys.append(key)
    for key in values:
        if key not in ordered_keys:
            ordered_keys.append(key)
    return {key: values.get(key, "") for key in ordered_keys}


def gather_text_for_selector_list(page, selectors: Iterable[str]) -> str:
    for selector in selectors:
        locator = page.locator(selector).first
        if locator.count() > 0:
            text = text_or_empty(locator.inner_text(timeout=3000))
            if text:
                return text
    return ""


def gather_href_for_selector_list(page, selectors: Iterable[str], base_url: str) -> str:
    for selector in selectors:
        locator = page.locator(selector).first
        if locator.count() > 0:
            href = text_or_empty(locator.get_attribute("href", timeout=3000))
            if href:
                if href.startswith("http"):
                    return href
                return base_url.rstrip("/") + "/" + href.lstrip("/")
    return ""


def collect_unique_hrefs(page, selector: str, base_url: str, limit: int) -> list[str]:
    hrefs: list[str] = []
    seen: set[str] = set()
    count = page.locator(selector).count()
    for idx in range(count):
        href = text_or_empty(page.locator(selector).nth(idx).get_attribute("href"))
        if not href:
            continue
        if not href.startswith("http"):
            href = base_url.rstrip("/") + "/" + href.lstrip("/")
        if href in seen:
            continue
        seen.add(href)
        hrefs.append(href)
        if len(hrefs) >= limit:
            break
    return hrefs


def wait_for_detail_refresh(page, detail_root_selectors: list[str], previous_snapshot: str) -> str:
    for _ in range(6):
        detail_text = gather_text_for_selector_list(page, detail_root_selectors)
        if detail_text and detail_text != previous_snapshot:
            return detail_text
        page.wait_for_timeout(400)
    return gather_text_for_selector_list(page, detail_root_selectors)


def extract_job_from_current_selection(
    page,
    source_url: str,
    source_site: str,
    requested_attributes: list[str],
    language_aliases: list[AliasTerm],
    tool_aliases: list[AliasTerm],
    title_selectors: list[str],
    detail_root_selectors: list[str],
    job_url_selectors: list[str],
    url_fallback: str,
) -> ExtractedJob | None:
    title = gather_text_for_selector_list(page, title_selectors)
    detail_text = gather_text_for_selector_list(page, detail_root_selectors)
    combined_text = "\n".join([title, detail_text]).strip()
    if not combined_text:
        return None

    job_url = gather_href_for_selector_list(page, job_url_selectors, url_fallback)
    if not job_url:
        job_url = page.url or source_url

    values: dict[str, str] = {}
    values["Job Title"] = title
    values["Programming Language"] = extract_terms(combined_text, language_aliases, is_language=True)
    values["Tools"] = extract_terms(combined_text, tool_aliases, is_language=False)
    values["Salary Range"] = extract_salary(combined_text)

    filtered = {attr: values.get(attr, "") for attr in requested_attributes}
    attributes = ordered_attributes(requested_attributes, filtered)

    return ExtractedJob(
        source_url=source_url,
        source_site=source_site,
        job_url=job_url,
        attributes=attributes,
    )


def click_each_card_and_extract(
    page,
    source_url: str,
    source_site: str,
    requested_attributes: list[str],
    language_aliases: list[AliasTerm],
    tool_aliases: list[AliasTerm],
    card_selector: str,
    card_click_selector: str,
    detail_root_selectors: list[str],
    title_selectors: list[str],
    job_url_selectors: list[str],
    url_fallback: str,
    max_cards: int,
) -> list[ExtractedJob]:
    jobs: list[ExtractedJob] = []
    seen: set[tuple[str, str]] = set()

    card_count = page.locator(card_selector).count()
    if card_count == 0:
        return jobs

    previous_detail = ""
    for idx in range(min(card_count, max_cards)):
        card = page.locator(card_selector).nth(idx)
        try:
            card.scroll_into_view_if_needed(timeout=3000)
            if card.locator(card_click_selector).count() > 0:
                card.locator(card_click_selector).first.click(timeout=5000)
            else:
                card.click(timeout=5000)
        except PlaywrightTimeoutError:
            continue

        detail_text = wait_for_detail_refresh(page, detail_root_selectors, previous_detail)
        previous_detail = detail_text

        job = extract_job_from_current_selection(
            page=page,
            source_url=source_url,
            source_site=source_site,
            requested_attributes=requested_attributes,
            language_aliases=language_aliases,
            tool_aliases=tool_aliases,
            title_selectors=title_selectors,
            detail_root_selectors=detail_root_selectors,
            job_url_selectors=job_url_selectors,
            url_fallback=url_fallback,
        )
        if not job:
            continue
        dedupe_key = (job.job_url, job.attributes.get("Job Title", ""))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        jobs.append(job)

    return jobs


def extract_dice(
    page,
    url: str,
    requested_attributes: list[str],
    language_aliases: list[AliasTerm],
    tool_aliases: list[AliasTerm],
    max_cards: int,
) -> list[ExtractedJob]:
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)
    jobs = click_each_card_and_extract(
        page=page,
        source_url=url,
        source_site="Dice",
        requested_attributes=requested_attributes,
        language_aliases=language_aliases,
        tool_aliases=tool_aliases,
        card_selector="dhi-search-card",
        card_click_selector="a[data-cy='card-title-link'], a[href*='/job-detail/']",
        detail_root_selectors=["[data-cy='jobDetails']", ".job-details", "#detail-panel", "div[class*='description']", "main", "body"],
        title_selectors=["h1", "[data-cy='jobTitle']", "[data-testid='job-title']", "title"],
        job_url_selectors=["a[data-cy='card-title-link'][href*='/job-detail/']", "a[href*='/job-detail/']"],
        url_fallback="https://www.dice.com",
        max_cards=max_cards,
    )
    if jobs:
        return jobs

    # Fallback for layouts where list cards render as anchor links without the card component.
    detail_links = collect_unique_hrefs(page, "a[href*='/job-detail/']", "https://www.dice.com", max_cards)
    extracted: list[ExtractedJob] = []
    seen: set[tuple[str, str]] = set()
    for href in detail_links:
        try:
            page.goto(href, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(1200)
        except PlaywrightTimeoutError:
            continue
        job = extract_job_from_current_selection(
            page=page,
            source_url=url,
            source_site="Dice",
            requested_attributes=requested_attributes,
            language_aliases=language_aliases,
            tool_aliases=tool_aliases,
            title_selectors=["h1", "[data-cy='jobTitle']", "[data-testid='job-title']", "title"],
            detail_root_selectors=["[data-cy='jobDetails']", ".job-details", "#detail-panel", "div[class*='description']", "main", "body"],
            job_url_selectors=["link[rel='canonical']", "a[href*='/job-detail/']"],
            url_fallback="https://www.dice.com",
        )
        if not job:
            continue
        dedupe_key = (job.job_url, job.attributes.get("Job Title", ""))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        extracted.append(job)
    return extracted


def extract_linkedin(
    page,
    url: str,
    requested_attributes: list[str],
    language_aliases: list[AliasTerm],
    tool_aliases: list[AliasTerm],
    max_cards: int,
) -> list[ExtractedJob]:
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)
    return click_each_card_and_extract(
        page=page,
        source_url=url,
        source_site="LinkedIn",
        requested_attributes=requested_attributes,
        language_aliases=language_aliases,
        tool_aliases=tool_aliases,
        card_selector="li[data-occludable-job-id]",
        card_click_selector="a[href*='/jobs/view/']",
        detail_root_selectors=["div.jobs-description__content", "div[class*='job-view-layout']", "article", "div.description__text"],
        title_selectors=["h1.jobs-unified-top-card__job-title", "h1.top-card-layout__title", "h1"],
        job_url_selectors=["li[data-occludable-job-id] a[href*='/jobs/view/']", "a[href*='/jobs/view/']"],
        url_fallback="https://www.linkedin.com",
        max_cards=max_cards,
    )


def dismiss_glassdoor_modals(page) -> None:
    selectors = [
        "button[data-test='job-alert-modal-close']",
        "span.SVGInline.modal_closeIcon",
        "button.modal_closeBtn",
        "[aria-label='Close']",
    ]
    for selector in selectors:
        locator = page.locator(selector).first
        if locator.count() > 0:
            try:
                locator.click(timeout=1500)
                page.wait_for_timeout(300)
            except PlaywrightTimeoutError:
                pass


def extract_glassdoor(
    page,
    url: str,
    requested_attributes: list[str],
    language_aliases: list[AliasTerm],
    tool_aliases: list[AliasTerm],
    max_cards: int,
) -> list[ExtractedJob]:
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)
    dismiss_glassdoor_modals(page)
    return click_each_card_and_extract(
        page=page,
        source_url=url,
        source_site="Glassdoor",
        requested_attributes=requested_attributes,
        language_aliases=language_aliases,
        tool_aliases=tool_aliases,
        card_selector="li[data-test='jobListing'], li.react-job-listing",
        card_click_selector="[data-test='job-link'], a[class*='jobLink'], a[href*='/job-listing/']",
        detail_root_selectors=["[data-test='jobDescriptionContent']", "div.jobDescriptionContent", "div[class*='desc']", "div.desc"],
        title_selectors=["[data-test='job-title']", "h1", "[data-test='job-link']"],
        job_url_selectors=["[data-test='job-link'][href]", "a[class*='jobLink'][href]", "a[href*='/job-listing/']"],
        url_fallback="https://www.glassdoor.com",
        max_cards=max_cards,
    )


def extract_generic(
    page,
    url: str,
    requested_attributes: list[str],
    language_aliases: list[AliasTerm],
    tool_aliases: list[AliasTerm],
    max_cards: int,
) -> list[ExtractedJob]:
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)
    return click_each_card_and_extract(
        page=page,
        source_url=url,
        source_site="Generic",
        requested_attributes=requested_attributes,
        language_aliases=language_aliases,
        tool_aliases=tool_aliases,
        card_selector="li[class*='job'], div[class*='job-card'], article[class*='job'], div[class*='posting']",
        card_click_selector="a[href]",
        detail_root_selectors=["div[class*='description']", "div[class*='details']", "article", "main", "body"],
        title_selectors=["h1", "h2", "title"],
        job_url_selectors=["a[href]"],
        url_fallback=url,
        max_cards=max_cards,
    )


def run_extraction(
    urls: list[str],
    requested_attributes: list[str],
    language_aliases: list[AliasTerm],
    tool_aliases: list[AliasTerm],
    headless: bool,
    max_cards: int,
) -> dict:
    if sync_playwright is None:
        raise RuntimeError(
            "Playwright is not installed. Install with 'pip install playwright' and then run 'playwright install'."
        )

    results: list[dict] = []
    failures: list[dict] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        for url in urls:
            site = detect_site(url)
            try:
                if site == "Dice":
                    jobs = extract_dice(page, url, requested_attributes, language_aliases, tool_aliases, max_cards)
                elif site == "LinkedIn":
                    jobs = extract_linkedin(page, url, requested_attributes, language_aliases, tool_aliases, max_cards)
                elif site == "Glassdoor":
                    jobs = extract_glassdoor(page, url, requested_attributes, language_aliases, tool_aliases, max_cards)
                else:
                    jobs = extract_generic(page, url, requested_attributes, language_aliases, tool_aliases, max_cards)

                results.append(
                    {
                        "url": url,
                        "site": site,
                        "jobs": [
                            {
                                "source_url": job.source_url,
                                "source_site": job.source_site,
                                "job_url": job.job_url,
                                "attributes": job.attributes,
                            }
                            for job in jobs
                        ],
                    }
                )
            except Exception as exc:  # pragma: no cover
                failures.append({"url": url, "site": site, "reason": str(exc)})
                results.append({"url": url, "site": site, "error": str(exc), "jobs": []})

        context.close()
        browser.close()

    total_jobs = sum(len(item.get("jobs", [])) for item in results)
    return {
        "results": results,
        "summary": {
            "total_urls": len(urls),
            "total_jobs": total_jobs,
            "failures": failures,
        },
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Extract jobs by clicking each left-side job card and reading right-side details, "
            "then output job URL plus attributes from settings/attributes.txt."
        )
    )
    parser.add_argument("--url", action="append", help="Optional URL override. Provide more than once for multiple URLs.")
    parser.add_argument("--settings-dir", default="settings", help="Settings directory path (default: settings).")
    parser.add_argument("--headless", action="store_true", help="Run browser headless.")
    parser.add_argument("--max-cards", type=int, default=50, help="Max visible cards to process per URL.")
    parser.add_argument("--output", help="Optional output JSON file path.")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    settings_dir = Path(args.settings_dir)
    attributes = read_non_comment_lines(settings_dir / "attributes.txt")
    language_aliases = read_alias_terms(settings_dir / "programminglanguages.txt")
    tool_aliases = read_alias_terms(settings_dir / "tools.txt")

    urls = args.url if args.url else read_non_comment_lines(settings_dir / "urls.txt")
    if not urls:
        raise SystemExit("No active URLs found. Check settings/urls.txt and remove comment markers.")

    output = run_extraction(
        urls=urls,
        requested_attributes=attributes,
        language_aliases=language_aliases,
        tool_aliases=tool_aliases,
        headless=bool(args.headless),
        max_cards=max(1, args.max_cards),
    )

    serialized = json.dumps(output, indent=2)
    if args.output:
        Path(args.output).write_text(serialized, encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
