# Job Search Agent

An automated job search agent that visits multiple job sites, extracts job descriptions, and matches them against target attributes.

## Requirements

- Python 3.10+
- Google Chrome or Chromium (for Selenium)
- ChromeDriver matching your Chrome version (auto-managed via `webdriver-manager`)

## Installation

```bash
cd C:\Working\Storage\Dev\GitHub\AIAssistants\job-search
pip install -r requirements.txt
```

## Usage

```bash
python job_search_agent.py
```

The script defaults to:

- `urls.txt`
- `attributes.txt`
- `targets.txt`
- `--match-pct 75`

All values can still be overridden:

```bash
python job_search_agent.py \
  --urls urls.txt \
  --attributes attributes.txt \
  --targets targets.txt \
  --match-pct 75
```

### Arguments

| Argument | Description |
|----------|-------------|
| `--urls` | Path to a file containing one search URL per line. Defaults to `urls.txt` in the script directory |
| `--attributes` | Path to a file listing the attributes to extract (e.g. `Job Title`, `Programming Language`, `Salary Range`). Defaults to `attributes.txt` |
| `--targets` | Path to a file listing target attribute values (e.g. `Job Title=Solutions Architect`). Defaults to `targets.txt` |
| `--match-pct` | Integer 0–100. Jobs scoring ≥ this value are flagged as **recommended**. Defaults to `75` |

## Input File Formats

### urls.txt
One URL per line. Blank lines and lines starting with `#` are ignored.

```
https://www.dice.com/jobs?q=Solutions+Architect&...
https://www.linkedin.com/jobs/search/?keywords=solutions+architect&...
```

### attributes.txt
One attribute name per line.

```
Job Title
Programming Language
Salary Range
```

### targets.txt
One target rule per line. Supported operators:

| Syntax | Meaning |
|--------|---------|
| `Job Title=Solutions Architect` | Exact (case-insensitive) match |
| `Job Title=Solutions Architect OR Software Engineer` | Match if any listed value matches |
| `Salary Range Includes 200K` | The discovered salary range must span $200,000 (i.e. min ≤ 200K ≤ max) |
| `Programming Language=Python` | Exact match |

```
Job Title=Solutions Architect
Programming Language=Python OR Java OR C#
Salary Range Includes 200K
```

## Output

Reports are written to:

```
C:\Working\Storage\Dev\GitHub\AIAssistants\job-search\reports\1YYYY-MM-DD_HH-MM\
```

Each run produces:
- `report.html` — human-readable HTML report
- `report.json` — machine-readable JSON of all results

After the files are written, the script opens `report.html` in your browser.

## Supported Job Sites

| Site | Extraction Method |
|------|-------------------|
| Dice | Selenium — clicks each job card in the left panel |
| Glassdoor | Selenium — clicks each job card, handles sign-in wall |
| Greenhouse | Selenium — standard job board |
| LinkedIn | Selenium — clicks each job card (login may be required for full details) |
| Remotive | requests + BeautifulSoup (static HTML) |

## Alternative AI Tools

For richer LLM-based attribute extraction, consider:

| Tool / Model | How to use |
|---|---|
| **OpenAI GPT-4o** | Replace the regex extractors in `extractors/base.py` with a call to the OpenAI Chat Completions API. Send the raw job description text and ask it to return JSON with the required attributes. |
| **Anthropic Claude 3.5 Sonnet** | Same pattern — pipe job text into a Claude prompt asking for structured extraction. Excellent at reasoning about salary ranges stated in non-standard prose. |
| **LangChain + any LLM** | Use LangChain's `WebBaseLoader` + an extraction chain to scrape and parse in one pipeline. Simplifies site-specific handling. |
| **Playwright + AI SDK** | Microsoft's Playwright MCP server can be driven by an LLM agent to handle complex JS-heavy pages better than Selenium. |
| **Bright Data / ScrapingBee** | Proxy-based scraping APIs that handle bot-detection on LinkedIn / Glassdoor, reducing need for manual Selenium cookie handling. |
