# Job Search Agent - Application Logic & Architecture

## Overview
The **Job Search Agent** is a Python-based application that automates job searches across multiple job boards, extracts relevant job information, matches jobs against user-defined criteria, and generates HTML/JSON reports with scoring and recommendations.

---

## Core Components

### 1. **Main Entry Point** (`job_search_agent.py`)
The orchestrator that ties everything together:

- **Load Configuration Files**
  - `urls.txt` - List of job search URLs to scrape (supports comments with `#`)
  - `attributes.txt` - Which job attributes to extract (e.g., Job Title, Programming Language, Salary Range)
  - `targets.txt` - Matching rules to score jobs

- **Process Flow**
  1. For each URL:
     - Detect the job board (Dice, LinkedIn, GlassDoor, Greenhouse, Remotive, or generic)
     - Launch site-specific Selenium extractor
     - Extract all jobs and requested attributes
  2. Score each job against target rules
  3. Calculate match percentage (number of matched rules / total rules × 100)
  4. Flag jobs as "RECOMMENDED" if match % ≥ minimum threshold (default: 75%)
  5. Generate timestamped report directory with:
     - `report.html` - Interactive visual report
     - `report.json` - Raw data for programmatic access
  6. Auto-open HTML report in default browser

- **Command-Line Arguments**
  - `--urls` - Path to URLs file (default: `urls.txt`)
  - `--attributes` - Path to attributes file (default: `attributes.txt`)
  - `--targets` - Path to targets file (default: `targets.txt`)
  - `--match-pct` - Minimum recommendation threshold 0-100 (default: 75)

---

### 2. **Site-Specific Extractors** (`extractors/` directory)

**Base Extractor** (`base.py`)
- Provides Selenium Chrome WebDriver setup with anti-detection measures
- Implements attribute extraction helpers for common job fields
- Supports headless and headful (visible) browser modes

**Extractor Types:**

| Site | Class | Notes |
|------|-------|-------|
| Dice.com | `DiceExtractor` | Standard Selenium scraping |
| Glassdoor | `GlassdoorExtractor` | Handles dynamic content |
| Greenhouse.io | `GreenhouseExtractor` | ATS job board |
| LinkedIn | `LinkedInExtractor` | **Non-headless required** (login walls) |
| Remotive | `RemotiveExtractor` | Remote job specialization |
| Unknown | `GenericExtractor` | Fallback with heuristic CSS selectors |

**Dispatcher** (`dispatcher.py`)
- Routes URLs to appropriate extractor by domain
- Returns `GenericExtractor()` for unrecognized sites

**Attribute Extraction Helpers:**
- **Job Title**: Regex patterns or first non-empty line
- **Programming Languages**: Scans for 20+ known languages (Java, Python, C#, TypeScript, Go, Rust, etc.)
- **Salary Range**: Extracts patterns like "$100,000 - $200,000", "100K–200K", "Up to $300K", "$150K+"

---

### 3. **Matcher** (`matcher.py`)
Evaluates how well extracted job attributes match user-defined target rules.

**Supported Rule Formats:**

1. **Exact Attribute Match**
   ```
   AttributeName=Value
   ```
   - Case-insensitive substring match
   - Example: `Job Title=Senior Engineer`

2. **Multiple Options (OR)**
   ```
   AttributeName=Value1 OR Value2 OR Value3
   ```
   - Matches if ANY option is found in extracted attribute
   - Example: `Programming Language=C# OR .NET OR Java`

3. **Salary Range Inclusion**
   ```
   Salary Range Includes <amount>
   ```
   - Validates if job's salary range spans the specified amount
   - Amount formats: `200000`, `200K`, `$200K`, `$200,000`
   - Handles ranges like "$150K–$250K", "Up to $300K", "$200K+"
   - Example: `Salary Range Includes 200K` (checks if job salary includes $200,000)

**Matching Algorithm:**
- For each target rule:
  - Parse and evaluate against extracted attributes
  - Mark as matched/unmatched
  - Track details (rule, matched status, extracted value)
- Calculate score: `(matched_count / total_rules) × 100`
- Return percentage score and detailed match breakdown

---

### 4. **Reporter** (`reporter.py`)
Generates visual HTML reports using Jinja2 templates.

- Takes scored results and renders interactive report
- Displays:
  - Timestamp of report generation
  - Minimum match % threshold used
  - Total jobs found vs. recommended count
  - Per-job scoring details and match rules
  - Source URLs and job links
- Outputs:
  - `report.html` (auto-opened in browser)
  - `report.json` (raw data export)

---

## Workflow Example

### **Scenario: Find C# Developer Jobs**

#### Step 1: Create `urls.txt`
```
# Remote C# jobs from Dice
https://www.dice.com/jobs?q=C%23&filters.workplaceTypes=Remote

# C# positions on LinkedIn
https://www.linkedin.com/jobs/search/?keywords=C%23

# .NET jobs on Remotive
https://remotive.com/remote-jobs?query=%22.net%22
```

#### Step 2: Create `attributes.txt`
```
Job Title
Programming Language
Salary Range
```

#### Step 3: Create `targets.txt`
```
# Target rules for scoring
Programming Language=C# OR .NET
Job Title=Developer OR Engineer OR Architect
Salary Range Includes 120K
```

#### Step 4: Run the Agent
```bash
python job_search_agent.py --match-pct 70
```

#### Step 5: Output
- **Dice.com**: Finds 45 C# developer jobs, ~70% match rate on average
- **LinkedIn**: Finds 32 positions, 15% blocked by login walls
- **Remotive**: Finds 28 remote .NET roles, 85% match rate
- **Report**: Generated at `reports/2026-08-07_21-10/`
  - 23 jobs recommended (≥70% match)
  - HTML report with color-coded matches
  - JSON export with all raw data

---

## Configuration Examples

### Example 1: Full-Stack Role with Experience Requirements
```
# urls.txt
https://www.dice.com/jobs?q=Full+Stack&filters.experienceLevel=Senior
https://www.linkedin.com/jobs/search/?keywords=full%20stack

# attributes.txt
Job Title
Programming Language
Salary Range

# targets.txt
Job Title=Full Stack
Programming Language=JavaScript OR TypeScript OR React
Programming Language=Java OR Python OR Node.js
Salary Range Includes 150K
```

### Example 2: Solutions Architect in Denver
```
# urls.txt
https://www.dice.com/jobs?q=Solutions+Architect&location=Denver%2C+CO
https://www.glassdoor.com/Job/denver-solutions-architect-jobs

# attributes.txt
Job Title
Programming Language
Salary Range

# targets.txt
Job Title=Solutions Architect OR Principal Architect
Programming Language=Java OR C# OR Python
Salary Range Includes 200K
```

### Example 3: Remote DevOps Position
```
# urls.txt
https://remotive.com/remote-jobs?query=DevOps&employment-type=full-time

# attributes.txt
Job Title
Programming Language

# targets.txt
Job Title=DevOps OR Platform Engineer
Programming Language=Python OR Go OR Rust
```

---

## Key Features

✅ **Multi-Site Support** - Seamlessly extract from Dice, LinkedIn, GlassDoor, Greenhouse, Remotive, or any site  
✅ **Intelligent Extraction** - Automatically identifies job titles, technologies, and salary ranges  
✅ **Flexible Matching** - Supports exact matches, OR logic, and complex salary range validation  
✅ **Anti-Detection** - Masks browser automation to bypass bot detection  
✅ **Batch Processing** - Process 100+ URLs in one run  
✅ **Rich Reporting** - HTML visualization + JSON export  
✅ **Extensible Extractors** - Add new job boards by creating a new extractor class  
✅ **Configuration-Driven** - No code changes needed; configure via text files  

---

## File Structure
```
job-search/
├── job_search_agent.py          # Main entry point
├── matcher.py                   # Job scoring logic
├── reporter.py                  # Report generation
├── urls.txt                     # Search URLs (config)
├── attributes.txt               # Extraction targets (config)
├── targets.txt                  # Matching rules (config)
├── requirements.txt             # Python dependencies
├── extractors/
│   ├── base.py                  # Base class + helpers
│   ├── dispatcher.py            # URL → Extractor routing
│   ├── linkedin.py              # LinkedIn-specific
│   ├── dice.py                  # Dice-specific
│   ├── glassdoor.py             # GlassDoor-specific
│   ├── greenhouse.py            # Greenhouse-specific
│   ├── remotive.py              # Remotive-specific
│   └── generic.py               # Fallback extractor
└── templates/
    └── report.html.j2           # HTML report template
```

---

## Dependencies
- **Selenium** - Browser automation
- **WebDriver Manager** - Chrome driver management
- **Jinja2** - Template rendering
- **Python 3.10+** - Modern syntax (type hints)

---

## Notes

1. **LinkedIn requires non-headless mode** due to aggressive bot detection
2. **Salary extraction** uses regex; ambiguous formats may be missed
3. **Generic extractor** uses CSS class heuristics; may miss jobs on non-standard sites
4. **Selenium drivers** auto-managed but require Chrome/Chromium installed
5. **Report timestamps** use format: `1YYYY-MM-DD_HH-MM` (note leading "1" for sorting)
