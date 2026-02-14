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

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Data Sources](https://img.shields.io/badge/Sources-Census%20ACS%20%7C%20CMS%20%7C%20USDA%20%7C%20HRSA-green)](https://data.census.gov)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-HuggingFace-yellow)](https://huggingface.co/datasets/lukeslp/us-inequality-atlas)
[![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-20BEFF)](https://www.kaggle.com/datasets/lucassteuber/us-inequality-atlas)

County-level inequality data for all ~3,200 US counties, keyed on 5-digit FIPS codes. Covers food deserts, healthcare access, housing affordability, hospital infrastructure, veteran demographics, disability prevalence, income inequality (Gini coefficient), education attainment, unemployment, and poverty depth.

I assembled this from Census ACS, CMS, USDA, and HRSA data for the inequality visualization series at [dr.eamer.dev/datavis](https://dr.eamer.dev/datavis/). Every file uses FIPS codes as the merge key, so you can join any combination.

Part of the [Data Trove](https://dr.eamer.dev/datavis/data_trove/) collection.

---

## What's Inside

### Food Deserts (`food_deserts/`)

| File | Records | Source |
|------|---------|--------|
| `food_desert_merged.csv` | 3,222 counties | Census ACS 2021 + USDA Food Access Atlas 2019 |
| `state_rankings.json` | 50 states | Aggregated state-level rankings |
| `worst_counties.json` | Top worst | Counties with highest food desert scores |
| `children_impact.json` | -- | Child food insecurity indicators |
| `snap_gap_states.json` | 50 states | SNAP coverage gaps |
| `regional_analysis.json` | -- | Regional breakdowns |
| `national_summary.json` | -- | National aggregate stats |

### Healthcare (`healthcare/`)

| File | Records | Source |
|------|---------|--------|
| `healthcare_desert_merged.csv` | 3,222 counties | Census ACS 2022 + HRSA HPSA |
| `cms_hospitals_2025.csv` | 5,421 hospitals | CMS Hospital Compare |

### Housing (`housing/`)

| File | Records | Source |
|------|---------|--------|
| `housing_crisis_merged.csv` | 3,222 counties | Census ACS 2022 (rent burden, income, units) |

### Veterans (`veterans/`)

| File | Records | Source |
|------|---------|--------|
| `military_firearm_merged_analysis.csv` | 54 states/territories | Census ACS + CDC + VA |
| `military_firearm_veterans.csv` | -- | Veteran population by state |
| `military_firearm_ptsd.csv` | -- | PTSD and mental health indicators |
| `military_firearm_suicide.csv` | -- | Veteran suicide rates |
| `military_firearm_va_healthcare.csv` | -- | VA healthcare enrollment |
| `military_firearm_firearms.csv` | -- | Firearm ownership rates |
| + 4 more CSVs with metadata | -- | Active duty, FFL, economic impact, spouse employment |

### CMS Hospitals (`cms/`)

| File | Records | Source |
|------|---------|--------|
| `cms_hospitals_20260121.csv` | 5,421 hospitals | CMS Hospital Compare (Jan 2026 refresh) |

### Source Data (`source/`)

| File | Size | Description |
|------|------|-------------|
| `food_access_atlas_2019.xlsx` | 82 MB | Raw USDA Food Access Research Atlas (Git LFS) |

---

## FIPS Codes

Every county-level file uses 5-digit FIPS codes as the primary key:

```
State FIPS (2 digits) + County FIPS (3 digits)
Example: "01001" = Autauga County, Alabama
```

This means you can merge any combination of datasets:

```python
import pandas as pd

food = pd.read_csv("food_deserts/food_desert_merged.csv", dtype={"fips": str})
health = pd.read_csv("healthcare/healthcare_desert_merged.csv", dtype={"fips": str})
housing = pd.read_csv("housing/housing_crisis_merged.csv", dtype={"fips": str})

merged = food.merge(health, on="fips", suffixes=("_food", "_health"))
merged = merged.merge(housing, on="fips")
```

---

## Quick Start

### Python

```python
import pandas as pd

# Load any county-level dataset
df = pd.read_csv("food_deserts/food_desert_merged.csv", dtype={"fips": str})

# Worst counties for food access
worst = df.nlargest(20, "poverty_rate")
print(worst[["fips", "name", "poverty_rate", "no_vehicle_pct"]])
```

### D3.js

```javascript
const data = await d3.csv("healthcare/healthcare_desert_merged.csv");
// FIPS codes ready for choropleth mapping
```

---

## Data Sources

| Source | Agency | URL |
|--------|--------|-----|
| American Community Survey | Census Bureau | [data.census.gov](https://data.census.gov) |
| Food Access Research Atlas | USDA ERS | [ers.usda.gov](https://www.ers.usda.gov/data-products/food-access-research-atlas/) |
| Hospital Compare | CMS | [data.cms.gov](https://data.cms.gov/provider-data/dataset/xubh-q36u) |
| Health Professional Shortage Areas | HRSA | [data.hrsa.gov](https://data.hrsa.gov) |
| Veteran Statistics | VA + CDC | Multiple sources |

---

## Related

- [Data Trove](https://dr.eamer.dev/datavis/data_trove/) -- full dataset catalog
- [lukesteuber.com](https://lukesteuber.com) -- portfolio
- [HuggingFace Dataset](https://huggingface.co/datasets/lukeslp/us-inequality-atlas)
- [Kaggle Dataset](https://www.kaggle.com/datasets/lucassteuber/us-inequality-atlas)

---

## Author

**Luke Steuber**
- [lukesteuber.com](https://lukesteuber.com)
- [dr.eamer.dev](https://dr.eamer.dev)
- [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com) on Bluesky

## License

MIT. See [LICENSE](LICENSE).

Source data is from US federal agencies (public domain).
