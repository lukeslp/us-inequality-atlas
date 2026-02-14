#!/usr/bin/env python3
"""
Fetch county-level Census ACS 2022 5-year data for the US Inequality Atlas.
Datasets: Gini coefficient, education attainment, unemployment, poverty depth.
"""

import csv
import json
import os
import sys
import time
from datetime import date
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

BASE_URL = "https://api.census.gov/data/2022/acs/acs5"
OUTPUT_DIR = "/home/coolhand/datasets/us-inequality-atlas"

# FIPS state codes to state abbreviations
STATE_FIPS = {
    "01": "AL", "02": "AK", "04": "AZ", "05": "AR", "06": "CA",
    "08": "CO", "09": "CT", "10": "DE", "11": "DC", "12": "FL",
    "13": "GA", "15": "HI", "16": "ID", "17": "IL", "18": "IN",
    "19": "IA", "20": "KS", "21": "KY", "22": "LA", "23": "ME",
    "24": "MD", "25": "MA", "26": "MI", "27": "MN", "28": "MS",
    "29": "MO", "30": "MT", "31": "NE", "32": "NV", "33": "NH",
    "34": "NJ", "35": "NM", "36": "NY", "37": "NC", "38": "ND",
    "39": "OH", "40": "OK", "41": "OR", "42": "PA", "44": "RI",
    "45": "SC", "46": "SD", "47": "TN", "48": "TX", "49": "UT",
    "50": "VT", "51": "VA", "53": "WA", "54": "WV", "55": "WI",
    "56": "WY", "72": "PR",
}


def fetch_census(variables: list[str], max_retries: int = 3) -> list[list[str]]:
    """Fetch county-level data from Census ACS API."""
    var_str = ",".join(variables)
    url = f"{BASE_URL}?get=NAME,{var_str}&for=county:*&in=state:*"
    print(f"  Fetching: {url[:120]}...")

    for attempt in range(max_retries):
        try:
            req = Request(url, headers={"User-Agent": "USInequalityAtlas/1.0"})
            with urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            print(f"  Received {len(data) - 1} rows")
            return data
        except (HTTPError, URLError, TimeoutError) as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
            else:
                raise


def make_fips(state_code: str, county_code: str) -> str:
    """Build 5-digit zero-padded FIPS code."""
    return f"{state_code.zfill(2)}{county_code.zfill(3)}"


def parse_county_name(name_field: str) -> str:
    """Extract county name from Census NAME field (e.g., 'Autauga County, Alabama')."""
    parts = name_field.split(",")
    return parts[0].strip() if parts else name_field.strip()


def safe_float(val, default=None):
    """Convert to float, returning default for missing/null values."""
    if val is None or val == "" or val == "null":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_int(val, default=None):
    """Convert to int, returning default for missing/null values."""
    if val is None or val == "" or val == "null":
        return default
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return default


def pct(numerator, denominator, decimals=2):
    """Calculate percentage, returning None if denominator is 0 or None."""
    if denominator is None or denominator == 0 or numerator is None:
        return None
    return round((numerator / denominator) * 100, decimals)


def write_csv(filepath: str, headers: list[str], rows: list[dict]):
    """Write rows to CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows)} rows to {filepath}")


def write_metadata(filepath: str, meta: dict):
    """Write metadata JSON alongside CSV."""
    json_path = filepath.replace(".csv", "_metadata.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"  Wrote metadata to {json_path}")


# ─────────────────────────────────────────────────────────────
# 1. GINI COEFFICIENT
# ─────────────────────────────────────────────────────────────
def fetch_gini():
    print("\n[1/4] Gini Coefficient (B19083_001E)")
    variables = ["B19083_001E"]
    raw = fetch_census(variables)

    header = raw[0]
    idx = {col: i for i, col in enumerate(header)}

    rows = []
    for row in raw[1:]:
        state_code = row[idx["state"]]
        county_code = row[idx["county"]]
        fips = make_fips(state_code, county_code)
        gini = safe_float(row[idx["B19083_001E"]])

        rows.append({
            "fips": fips,
            "county_name": parse_county_name(row[idx["NAME"]]),
            "state": STATE_FIPS.get(state_code, state_code),
            "gini_index": gini,
        })

    filepath = os.path.join(OUTPUT_DIR, "economic", "gini_by_county.csv")
    headers = ["fips", "county_name", "state", "gini_index"]
    write_csv(filepath, headers, rows)
    write_metadata(filepath, {
        "source": "U.S. Census Bureau, American Community Survey 5-Year Estimates (2022)",
        "table": "B19083",
        "variable": "B19083_001E",
        "description": "Gini Index of Income Inequality by county. Values range from 0 (perfect equality) to 1 (perfect inequality).",
        "geography": "County",
        "record_count": len(rows),
        "collection_date": str(date.today()),
        "api_url": f"{BASE_URL}?get=NAME,B19083_001E&for=county:*&in=state:*",
    })
    return len(rows)


# ─────────────────────────────────────────────────────────────
# 2. EDUCATION ATTAINMENT
# ─────────────────────────────────────────────────────────────
def fetch_education():
    print("\n[2/4] Education Attainment (B15003)")
    variables = [
        "B15003_001E",  # Total 25+
        "B15003_017E",  # HS diploma
        "B15003_018E",  # GED
        "B15003_019E",  # Some college < 1 yr
        "B15003_020E",  # Some college 1+ yr
        "B15003_021E",  # Associate's
        "B15003_022E",  # Bachelor's
        "B15003_023E",  # Master's
        "B15003_024E",  # Professional
        "B15003_025E",  # Doctorate
    ]
    raw = fetch_census(variables)

    header = raw[0]
    idx = {col: i for i, col in enumerate(header)}

    rows = []
    for row in raw[1:]:
        state_code = row[idx["state"]]
        county_code = row[idx["county"]]
        fips = make_fips(state_code, county_code)

        total = safe_int(row[idx["B15003_001E"]])
        hs = safe_int(row[idx["B15003_017E"]], 0)
        ged = safe_int(row[idx["B15003_018E"]], 0)
        some_col_lt1 = safe_int(row[idx["B15003_019E"]], 0)
        some_col_1p = safe_int(row[idx["B15003_020E"]], 0)
        associates = safe_int(row[idx["B15003_021E"]], 0)
        bachelors = safe_int(row[idx["B15003_022E"]], 0)
        masters = safe_int(row[idx["B15003_023E"]], 0)
        professional = safe_int(row[idx["B15003_024E"]], 0)
        doctorate = safe_int(row[idx["B15003_025E"]], 0)

        # HS or higher = HS + GED + some college + associate + bachelor + master + professional + doctorate
        hs_or_higher = hs + ged + some_col_lt1 + some_col_1p + associates + bachelors + masters + professional + doctorate
        # Bachelor's or higher = bachelor + master + professional + doctorate
        bachelors_or_higher = bachelors + masters + professional + doctorate

        rows.append({
            "fips": fips,
            "county_name": parse_county_name(row[idx["NAME"]]),
            "state": STATE_FIPS.get(state_code, state_code),
            "total_25_plus": total,
            "pct_hs_or_higher": pct(hs_or_higher, total),
            "pct_bachelors_or_higher": pct(bachelors_or_higher, total),
        })

    filepath = os.path.join(OUTPUT_DIR, "education", "education_by_county.csv")
    headers = ["fips", "county_name", "state", "total_25_plus", "pct_hs_or_higher", "pct_bachelors_or_higher"]
    write_csv(filepath, headers, rows)
    write_metadata(filepath, {
        "source": "U.S. Census Bureau, American Community Survey 5-Year Estimates (2022)",
        "table": "B15003",
        "variables": variables,
        "description": "Educational attainment for population 25+ by county. pct_hs_or_higher includes HS diploma, GED, some college, associate's, bachelor's, master's, professional, and doctorate degrees. pct_bachelors_or_higher includes bachelor's, master's, professional, and doctorate degrees.",
        "geography": "County",
        "record_count": len(rows),
        "collection_date": str(date.today()),
        "api_url": f"{BASE_URL}?get=NAME,{','.join(variables)}&for=county:*&in=state:*",
    })
    return len(rows)


# ─────────────────────────────────────────────────────────────
# 3. UNEMPLOYMENT
# ─────────────────────────────────────────────────────────────
def fetch_unemployment():
    print("\n[3/4] Unemployment (B23025)")
    variables = [
        "B23025_001E",  # Total 16+
        "B23025_002E",  # In labor force
        "B23025_005E",  # Unemployed
    ]
    raw = fetch_census(variables)

    header = raw[0]
    idx = {col: i for i, col in enumerate(header)}

    rows = []
    for row in raw[1:]:
        state_code = row[idx["state"]]
        county_code = row[idx["county"]]
        fips = make_fips(state_code, county_code)

        total = safe_int(row[idx["B23025_001E"]])
        labor_force = safe_int(row[idx["B23025_002E"]])
        unemployed = safe_int(row[idx["B23025_005E"]])

        rows.append({
            "fips": fips,
            "county_name": parse_county_name(row[idx["NAME"]]),
            "state": STATE_FIPS.get(state_code, state_code),
            "total_16_plus": total,
            "labor_force": labor_force,
            "unemployed": unemployed,
            "labor_force_participation_rate": pct(labor_force, total),
            "unemployment_rate": pct(unemployed, labor_force),
        })

    filepath = os.path.join(OUTPUT_DIR, "economic", "unemployment_by_county.csv")
    headers = ["fips", "county_name", "state", "total_16_plus", "labor_force", "unemployed",
               "labor_force_participation_rate", "unemployment_rate"]
    write_csv(filepath, headers, rows)
    write_metadata(filepath, {
        "source": "U.S. Census Bureau, American Community Survey 5-Year Estimates (2022)",
        "table": "B23025",
        "variables": variables,
        "description": "Employment status for population 16+ by county. Labor force participation rate = labor force / total 16+. Unemployment rate = unemployed / labor force.",
        "geography": "County",
        "record_count": len(rows),
        "collection_date": str(date.today()),
        "api_url": f"{BASE_URL}?get=NAME,{','.join(variables)}&for=county:*&in=state:*",
    })
    return len(rows)


# ─────────────────────────────────────────────────────────────
# 4. POVERTY DEPTH
# ─────────────────────────────────────────────────────────────
def fetch_poverty():
    print("\n[4/4] Poverty Depth (C17002)")
    variables = [
        "C17002_001E",  # Total
        "C17002_002E",  # Under 0.50
        "C17002_003E",  # 0.50 to 0.99
        "C17002_004E",  # 1.00 to 1.24
        "C17002_005E",  # 1.25 to 1.49
    ]
    raw = fetch_census(variables)

    header = raw[0]
    idx = {col: i for i, col in enumerate(header)}

    rows = []
    for row in raw[1:]:
        state_code = row[idx["state"]]
        county_code = row[idx["county"]]
        fips = make_fips(state_code, county_code)

        total = safe_int(row[idx["C17002_001E"]])
        under_050 = safe_int(row[idx["C17002_002E"]], 0)
        r050_099 = safe_int(row[idx["C17002_003E"]], 0)
        r100_124 = safe_int(row[idx["C17002_004E"]], 0)
        r125_149 = safe_int(row[idx["C17002_005E"]], 0)

        # Deep poverty: under 0.50
        # Poverty: under 1.00 (under 0.50 + 0.50-0.99)
        # Near poverty: 1.00-1.49 (1.00-1.24 + 1.25-1.49)
        poverty = under_050 + r050_099
        near_poverty = r100_124 + r125_149

        rows.append({
            "fips": fips,
            "county_name": parse_county_name(row[idx["NAME"]]),
            "state": STATE_FIPS.get(state_code, state_code),
            "total": total,
            "pct_deep_poverty": pct(under_050, total),
            "pct_poverty": pct(poverty, total),
            "pct_near_poverty": pct(near_poverty, total),
        })

    filepath = os.path.join(OUTPUT_DIR, "economic", "poverty_depth_by_county.csv")
    headers = ["fips", "county_name", "state", "total", "pct_deep_poverty", "pct_poverty", "pct_near_poverty"]
    write_csv(filepath, headers, rows)
    write_metadata(filepath, {
        "source": "U.S. Census Bureau, American Community Survey 5-Year Estimates (2022)",
        "table": "C17002",
        "variables": variables,
        "description": "Ratio of income to poverty level by county. pct_deep_poverty = under 0.50 of poverty threshold. pct_poverty = under 1.00 (below poverty line). pct_near_poverty = 1.00-1.49 (near poverty).",
        "geography": "County",
        "record_count": len(rows),
        "collection_date": str(date.today()),
        "api_url": f"{BASE_URL}?get=NAME,{','.join(variables)}&for=county:*&in=state:*",
    })
    return len(rows)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("US Inequality Atlas - Census ACS 2022 Data Fetch")
    print("=" * 60)

    totals = {}
    totals["gini"] = fetch_gini()
    time.sleep(1)  # Be polite to the API
    totals["education"] = fetch_education()
    time.sleep(1)
    totals["unemployment"] = fetch_unemployment()
    time.sleep(1)
    totals["poverty"] = fetch_poverty()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, count in totals.items():
        print(f"  {name}: {count} counties")
    print("\nDone.")
