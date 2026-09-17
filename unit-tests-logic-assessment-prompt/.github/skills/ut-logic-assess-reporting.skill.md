# Skill: ut-logic-assess-reporting

## Goal
Generate the final Markdown report from computed lists and metrics.

## Inputs
- All required lists.
- Summary metrics.
- `detail_level`: `standard` or `detailed`.

## Mandatory Sections (Always)
1. `Untested Classes`
2. `Not Tested Class Elements`
3. `Logic Covered`
4. `Logic Not Covered`
5. `Summary`
   - `Untested Class Percent`
   - `Untested Element Percent` (per class)
   - `Overall Untested Elements Percent`
   - `Logic Not Covered Percent` (per class)

## Additional Sections (Detailed Mode)
- `Classes`
- `Class Logic`
- `Unit Test Classes`
- `Unit Test Elements`
- `Tested Class Elements`

## Formatting Rules
- Use Markdown tables for all lists.
- Show `N/A` values with a short reason line directly below the metric table.
- Keep section names exact.

## Narrative Rules
- Keep prose concise and evidence-based.
- Do not claim coverage for unresolved mappings.
