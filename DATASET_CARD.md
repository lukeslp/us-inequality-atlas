---
license: mit
task_categories:
  - tabular-classification
  - feature-extraction
language:
  - en
tags:
  - inequality
  - food-deserts
  - healthcare
  - housing
  - veterans
  - disability
  - education
  - economics
  - gini-coefficient
  - census
  - fips
  - county-level
  - united-states
pretty_name: US Inequality Atlas
size_categories:
  - 1K<n<10K
---

# US Inequality Atlas

County-level inequality data for all ~3,200 US counties, keyed on 5-digit FIPS codes. Covers food deserts, healthcare access, housing affordability, hospital infrastructure, veteran demographics, disability prevalence, income inequality (Gini coefficient), education attainment, unemployment, and poverty depth.

- **Repository:** [github.com/lukeslp/us-inequality-atlas](https://github.com/lukeslp/us-inequality-atlas)
- **Part of:** [Data Trove](https://dr.eamer.dev/datavis/data_trove/)
- **Author:** [Luke Steuber](https://lukesteuber.com)

## Categories

| Category | Key File | Records | Source |
|----------|----------|---------|--------|
| Food Deserts | `food_deserts/food_desert_merged.csv` | 3,222 | Census ACS + USDA |
| Healthcare | `healthcare/healthcare_desert_merged.csv` | 3,222 | Census ACS + HRSA |
| Housing | `housing/housing_crisis_merged.csv` | 3,222 | Census ACS 2022 |
| Hospitals | `cms/cms_hospitals_20260121.csv` | 5,421 | CMS Hospital Compare |
| Veterans | `veterans/military_firearm_merged_analysis.csv` | 54 | Census + CDC + VA |
| Economic (Gini) | `economic/gini_by_county.csv` | 3,222 | Census ACS 2022 (B19083) |
| Economic (Unemployment) | `economic/unemployment_by_county.csv` | 3,222 | Census ACS 2022 (B23025) |
| Economic (Poverty Depth) | `economic/poverty_depth_by_county.csv` | 3,222 | Census ACS 2022 (C17002) |
| Education | `education/education_by_county.csv` | 3,222 | Census ACS 2022 (B15003) |
| Disability | `disability/census_disability_by_county_2022.csv` | 3,222 | Census ACS 2022 (S1810) |

## FIPS Code Convention

All files use 5-digit FIPS codes (`state_fips + county_fips`): `"01001"` = Autauga County, Alabama.

## Sources

- [Census ACS](https://data.census.gov) (public domain)
- [USDA Food Access Atlas](https://www.ers.usda.gov/data-products/food-access-research-atlas/)
- [CMS Hospital Compare](https://data.cms.gov)
- [HRSA HPSA](https://data.hrsa.gov)

## License

MIT. Source data is US federal (public domain). Compiled by [Luke Steuber](https://lukesteuber.com).
