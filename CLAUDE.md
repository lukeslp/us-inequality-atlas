# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

County-level inequality data for ~3,200 US counties from Census ACS, CMS, USDA, and HRSA. All files use 5-digit FIPS codes as the merge key. Has its own git repo at `lukeslp/us-inequality-atlas`.

## Directory Layout

```
us-inequality-atlas/
├── food_deserts/          # 7 files: county-level food access + SNAP gaps
├── healthcare/            # 2 files: healthcare deserts + CMS hospitals
├── housing/               # 1 file: rent burden, income, housing units
├── veterans/              # 10+ files: veteran demographics, PTSD, suicide, VA healthcare
├── economic/              # 3 files: Gini coefficient, unemployment, poverty depth
├── education/             # 1 file: education attainment by county
├── disability/            # 1 file: census disability rates by county
├── cms/                   # 1 file: CMS hospitals (Jan 2026 refresh)
├── merged/                # inequality_master.csv (all dimensions combined)
├── fetch_census_acs.py    # Data pipeline: fetches ACS 2022 data (needs CENSUS_API_KEY)
├── exploration.ipynb      # Jupyter notebook for data exploration
├── dataset-metadata.json  # Kaggle metadata
├── DATASET_CARD.md        # HuggingFace dataset card
└── README.md
```

## Data Pipeline

```bash
# Requires CENSUS_API_KEY environment variable
python3 fetch_census_acs.py
```

Fetches from Census ACS 2022 5-Year API:
- B19083 (Gini coefficient)
- B15003 (Education attainment)
- B23025 (Employment status)
- C17002 (Poverty depth)

Outputs CSVs in `economic/` and `education/` subdirectories.

## Key Merge Pattern

Every county-level CSV uses `fips` (5-digit string) as the primary key:

```python
import pandas as pd
food = pd.read_csv("food_deserts/food_desert_merged.csv", dtype={"fips": str})
health = pd.read_csv("healthcare/healthcare_desert_merged.csv", dtype={"fips": str})
merged = food.merge(health, on="fips")
```

## Integration Points

- **Interactive Atlas** (`~/html/datavis/interactive/atlas/`): Multiple files from this dataset power atlas layers (food-access, housing-burden, housing-crisis, veterans, disability, healthcare-deserts, poverty)
- **Data Trove**: Files symlinked/referenced via `/datavis/data_trove/`

## Platforms

- **GitHub**: `lukeslp/us-inequality-atlas`
- **HuggingFace**: `lukeslp/us-inequality-atlas`
- **Kaggle**: `lucassteuber/us-inequality-atlas`
