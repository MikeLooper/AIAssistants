# Skill: ut-logic-assess-coverage-metrics

## Goal
Calculate required coverage percentages from produced lists.

## Inputs
- `Classes`
- `Untested Classes`
- `Tested Class Elements`
- `Not Tested Class Elements`
- `Class Logic`
- `Logic Not Covered`

## Outputs
### Summary Metrics
- `Untested Class Percent`
- `Untested Element Percent` (per class)
- `Overall Untested Elements Percent`
- `Logic Not Covered Percent` (per class)

## Required Formulas
1. `Untested Class Percent`
- `(Number of Untested Classes / Number of code classes) * 100`

2. `Untested Element Percent` (per class)
- `(Number of Not Tested Class Elements / (Number of Tested Class Elements + Number of Not Tested Class Elements)) * 100`

3. `Overall Untested Elements Percent`
- `(Total Not Tested Elements / (Total Tested Elements + Total Not Tested Elements)) * 100`

4. `Logic Not Covered Percent` (per class)
- `(Number of Logic Not Covered / Number of code class logic branches) * 100`

## Zero-Denominator Handling
- If any denominator is `0`, emit `N/A` with reason:
  - No discovered classes.
  - No discovered class elements for class.
  - No discovered logic branches for class.

## Precision
- Default display precision: two decimals.
