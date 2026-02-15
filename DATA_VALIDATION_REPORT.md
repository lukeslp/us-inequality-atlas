# US Inequality Atlas - Pre-Publication Validation Report

**Date:** 2026-02-14
**Dataset:** US Inequality Atlas (enriched from 5 to 10 dimensions)
**Location:** `/home/coolhand/datasets/us-inequality-atlas/`

---

## Executive Summary

**Overall Status: ✓ PASS - READY FOR PUBLICATION**

The dataset has successfully passed all validation checks:
- ✓ FIPS integrity: 3,222 counties, no duplicates, all valid 5-digit codes
- ✓ Range validation: All numeric columns within expected bounds
- ✓ Source file integrity: All 8 source CSVs present with correct row counts
- ✓ Visualization sync: Master CSV matches visualization data exactly
- ✓ Synthetic data scan: Natural distributions, no artificial patterns
- ✓ Metadata consistency: README accurately describes dataset contents

---

## 1. FIPS Join Integrity: ✓ PASS

### Row Count
- **Expected:** 3,222 counties
- **Actual:** 3,222 counties
- **Status:** ✓ PASS

### FIPS Code Quality
- **Null FIPS codes:** 0
- **Invalid FIPS codes:** 0 (all valid 5-digit format)
- **Duplicate FIPS codes:** 0
- **Status:** ✓ PASS

All counties have unique, valid 5-digit FIPS codes in format `SSCCC` (state + county).

---

## 2. Range Validation: ✓ PASS

All numeric columns validated for expected ranges. No negative values, no out-of-range values.

### Indices (0-100 scale)
| Column | Range | Status |
|--------|-------|--------|
| `composite_index` | 0-100 | ✓ PASS |
| `economic_score` | 0-100 | ✓ PASS |
| `education_score` | 0-100 | ✓ PASS |
| `healthcare_score` | 0-100 | ✓ PASS |
| `housing_score` | 0-100 | ✓ PASS |
| `food_score` | 0-100 | ✓ PASS |
| `disability_score` | 0-100 | ✓ PASS |

### Gini Coefficient
| Column | Range | Status |
|--------|-------|--------|
| `gini_index` | 0-1 | ✓ PASS |

### Percentage Columns (0-100 scale)
All percentage columns validated within 0-100 range:
- poverty_rate
- unemployment_rate
- disability_rate
- no_vehicle_pct
- uninsured_rate
- pct_rent_burdened_30
- pct_rent_burdened_50
- pct_deep_poverty
- pct_poverty
- pct_near_poverty
- pct_hs_or_higher
- pct_bachelors_or_higher
- labor_force_participation

**Status:** ✓ PASS - No values out of range, no negative values where impossible.

---

## 3. Source File Integrity: ✓ PASS

All 8 source CSV files present with expected row counts.

| Source File | Row Count | Status |
|-------------|-----------|--------|
| `food_deserts/food_desert_merged.csv` | 3,222 | ✓ PASS |
| `healthcare/healthcare_desert_merged.csv` | 3,222 | ✓ PASS |
| `housing/housing_crisis_merged.csv` | 3,222 | ✓ PASS |
| `economic/gini_by_county.csv` | 3,222 | ✓ PASS |
| `economic/unemployment_by_county.csv` | 3,222 | ✓ PASS |
| `economic/poverty_depth_by_county.csv` | 3,222 | ✓ PASS |
| `education/education_by_county.csv` | 3,222 | ✓ PASS |
| `disability/census_disability_by_county_2022.csv` | 3,222 | ✓ PASS |

All source files match the master CSV row count exactly.

---

## 4. Visualization Data Sync: ✓ PASS

- **Location:** `/home/coolhand/html/datavis/dev/data/inequality_master.csv`
- **Status:** ✓ PASS - File exists
- **MD5 Hash Match:** ✓ PASS - Files match exactly

The visualization data is an exact copy of the master CSV, ensuring choropleth maps and scatter plots use the same validated data.

---

## 5. Synthetic Data Scan: ✓ PASS

### Round Number Analysis

Checked for suspiciously uniform distributions (indicator of synthetic/fabricated data).

| Column | Total Values | Round Values | % Round | Status |
|--------|--------------|--------------|---------|--------|
| `composite_index` | 3,222 | 304 | 9.4% | ✓ PASS |
| `gini_index` | 3,222 | 0 | 0.0% | ✓ PASS |
| `poverty_rate` | 3,222 | 81 | 2.5% | ✓ PASS |
| `unemployment_rate` | 3,222 | 94 | 2.9% | ✓ PASS |

All columns show natural distributions (< 10% round numbers). Gini coefficients show excellent precision (0% round).

### Distribution Uniformity

Coefficient of variation (CV) measures distribution spread. Very low CV (< 0.1) can indicate synthetic data.

| Column | Mean | Std Dev | CV | Status |
|--------|------|---------|-----|--------|
| `composite_index` | 49.99 | 15.29 | 0.306 | ✓ PASS |
| `poverty_rate` | 15.10 | 7.70 | 0.510 | ✓ PASS |

Both show normal variation (CV > 0.3), indicating real-world data with natural geographic disparities.

### County Name Validation

- **Generic/test names:** 0 (✓ PASS)
- **Duplicate state-county combos:** 0 (✓ PASS)

No evidence of placeholder data ("Test County", "Sample County", etc.). All county names appear authentic.

---

## 6. Outlier Samples

### Top 5 Most Unequal Counties (Composite Index)

| FIPS | County, State | Composite Index |
|------|---------------|-----------------|
| 48505 | Zapata County, Texas | 90.1 |
| 48427 | Starr County, Texas | 89.5 |
| 28163 | Yazoo County, Mississippi | 89.1 |
| 29155 | Pemiscot County, Missouri | 89.1 |
| 22009 | Avoyelles Parish, Louisiana | 88.8 |

### Top 5 Highest Gini Coefficients (Income Inequality)

| FIPS | County, State | Gini Index |
|------|---------------|------------|
| 35021 | Harding County, New Mexico | 0.721 |
| 72097 | Mayagüez Municipio, Puerto Rico | 0.618 |
| 72127 | San Juan Municipio, Puerto Rico | 0.611 |
| 22035 | East Carroll Parish, Louisiana | 0.606 |
| 35019 | Guadalupe County, New Mexico | 0.605 |

These outliers are geographically plausible:
- Texas border counties (Zapata, Starr) have known economic challenges
- Mississippi Delta counties (Yazoo, East Carroll) have documented inequality
- Puerto Rico municipalities reflect island-specific economic conditions
- New Mexico rural counties (Harding, Guadalupe) show expected rural disparities

**Status:** ✓ PASS - Outliers are consistent with documented regional inequality patterns.

---

## 7. Metadata Consistency: ✓ PASS

### README Accuracy

The README claims the dataset covers:
1. Food deserts ✓
2. Healthcare access ✓
3. Housing affordability ✓
4. Hospital infrastructure ✓ (separate CMS file)
5. Income inequality (Gini) ✓
6. Education attainment ✓
7. Unemployment ✓
8. Poverty depth ✓
9. Veteran demographics ✓ (state-level only, not in master CSV)
10. Disability prevalence ✓

### Column Mapping

| Dimension | Columns in Master CSV | Status |
|-----------|----------------------|--------|
| Food deserts | food_score, poverty_rate, no_vehicle_pct | ✓ |
| Healthcare | healthcare_score, uninsured_rate, hospital_closure_risk | ✓ |
| Housing | housing_score, pct_rent_burdened_30, pct_rent_burdened_50, median_gross_rent, rent_to_income_ratio | ✓ |
| Economic | economic_score, gini_index, unemployment_rate, labor_force_participation | ✓ |
| Poverty | pct_deep_poverty, pct_poverty, pct_near_poverty | ✓ |
| Education | education_score, pct_hs_or_higher, pct_bachelors_or_higher | ✓ |
| Disability | disability_score, disability_rate | ✓ |
| Composite | composite_index | ✓ |

**Status:** ✓ PASS - README accurately describes dataset dimensions and sources.

**Notes:**
- Veteran data is state-level only (separate directory, not in county master CSV)
- Hospital infrastructure (hospital count, closures) is in separate CMS file

---

## Recommendations

### For Publication

1. **Kaggle:** Create as PRIVATE first, review on web UI, then make public
   - Title: "US Inequality Atlas" (18 chars, within 6-50 limit)
   - Subtitle: "County-level inequality across 10 dimensions" (46 chars, within 20-80 limit)
   - Slug: `us-inequality-atlas` (19 chars, within 3-50 limit)

2. **HuggingFace:** Upload `merged/inequality_master.csv` as main file
   - Use existing `README.md` as dataset card (already has YAML frontmatter)
   - Include all source CSVs for reproducibility

3. **Data Trove:** Already synced to `/home/coolhand/html/datavis/dev/data/`

### For Documentation

The README could add a section on the composite index calculation methodology. Currently it shows the results but not the formula. Consider adding:

```markdown
## Composite Index Methodology

The composite_index (0-100 scale, higher = worse inequality) is calculated as the weighted average of 6 dimension scores:

composite_index = mean([economic_score, education_score, healthcare_score, housing_score, food_score, disability_score])

Each dimension score is percentile-ranked (0 = best, 100 = worst) based on the national distribution.
```

### For Future Enrichment

Potential additions for future versions:
- Transportation access (commute times, public transit availability)
- Environmental justice (pollution exposure, climate risk)
- Digital divide (broadband access, device ownership)
- Childcare availability (provider density, cost burden)

---

## Validation Tools Used

1. **Python CSV module** (proper quote handling for county names with commas)
2. **Custom validation script** (`validate_dataset.py`)
3. **MD5 hash comparison** (file integrity check)
4. **Statistical analysis** (distribution uniformity, coefficient of variation)

---

## Sign-Off

**Validator:** Data Guardian (geepers_doublecheck agent)
**Date:** 2026-02-14
**Result:** ✓ READY FOR PUBLICATION

All validation checks passed. The dataset contains authentic, well-structured county-level inequality data with no evidence of synthetic patterns or data quality issues.

---

## Appendix: Column Reference

### Master CSV Schema (28 columns)

| # | Column | Type | Range | Description |
|---|--------|------|-------|-------------|
| 1 | fips | string | 5 digits | County FIPS code (primary key) |
| 2 | county_name | string | -- | County name with state suffix |
| 3 | state | string | 2 chars | State abbreviation |
| 4 | total_pop | float | >0 | Total county population (Census ACS 2022) |
| 5 | composite_index | float | 0-100 | Overall inequality index (higher = worse) |
| 6 | economic_score | float | 0-100 | Economic inequality percentile |
| 7 | education_score | float | 0-100 | Educational attainment percentile |
| 8 | healthcare_score | float | 0-100 | Healthcare access percentile |
| 9 | housing_score | float | 0-100 | Housing affordability percentile |
| 10 | food_score | float | 0-100 | Food desert severity percentile |
| 11 | disability_score | float | 0-100 | Disability prevalence percentile |
| 12 | poverty_rate | float | 0-100 | Percent below poverty line |
| 13 | no_vehicle_pct | float | 0-100 | Percent households without vehicle |
| 14 | uninsured_rate | float | 0-100 | Percent without health insurance |
| 15 | hospital_closure_risk | float | 0-100 | Hospital closure risk score |
| 16 | pct_rent_burdened_30 | float | 0-100 | Percent spending >30% income on rent |
| 17 | pct_rent_burdened_50 | float | 0-100 | Percent spending >50% income on rent |
| 18 | median_gross_rent | float | >0 | Median gross rent ($) |
| 19 | rent_to_income_ratio | float | 0-100 | Rent as % of median income |
| 20 | gini_index | float | 0-1 | Gini coefficient (0 = equality, 1 = max inequality) |
| 21 | unemployment_rate | float | 0-100 | Unemployment rate (%) |
| 22 | labor_force_participation | float | 0-100 | Labor force participation rate (%) |
| 23 | pct_deep_poverty | float | 0-100 | Percent below 50% poverty line |
| 24 | pct_poverty | float | 0-100 | Percent below 100% poverty line |
| 25 | pct_near_poverty | float | 0-100 | Percent below 125% poverty line |
| 26 | pct_hs_or_higher | float | 0-100 | Percent high school graduate or higher |
| 27 | pct_bachelors_or_higher | float | 0-100 | Percent bachelor's degree or higher |
| 28 | disability_rate | float | 0-100 | Percent with a disability |

---

**End of Report**
