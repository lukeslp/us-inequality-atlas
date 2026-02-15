#!/usr/bin/env python3
"""
Comprehensive validation for US Inequality Atlas dataset
"""

import csv
import sys
from pathlib import Path

def validate_fips(value):
    """Check if FIPS is a valid 5-digit code"""
    try:
        fips_str = str(int(value)).zfill(5)
        return len(fips_str) == 5 and fips_str.isdigit()
    except:
        return False

def validate_range(value, min_val, max_val, allow_null=False):
    """Check if value is within expected range"""
    if value == '' or value is None:
        return allow_null
    try:
        num = float(value)
        return min_val <= num <= max_val
    except:
        return False

def main():
    print("=" * 70)
    print("US INEQUALITY ATLAS - PRE-PUBLICATION VALIDATION")
    print("=" * 70)

    # 1. FIPS JOIN INTEGRITY
    print("\n1. FIPS JOIN INTEGRITY")
    print("-" * 70)

    fips_set = set()
    invalid_fips = []
    duplicate_fips = []
    null_fips = []

    with open('merged/inequality_master.csv', 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            fips = row['fips']

            if not fips or fips.strip() == '':
                null_fips.append((i, row['county_name']))
                continue

            if not validate_fips(fips):
                invalid_fips.append((i, fips, row['county_name']))
                continue

            fips_norm = str(int(fips)).zfill(5)
            if fips_norm in fips_set:
                duplicate_fips.append((i, fips_norm, row['county_name']))
            fips_set.add(fips_norm)

    total_rows = len(fips_set)
    print(f"Total rows: {total_rows}")
    print(f"Expected: 3222")

    if total_rows == 3222:
        print("✓ PASS - Correct row count")
    else:
        print(f"✗ FAIL - Off by {total_rows - 3222}")

    print(f"\nNull FIPS codes: {len(null_fips)}")
    if null_fips:
        print("✗ FAIL - Null FIPS codes found:")
        for line, county in null_fips[:5]:
            print(f"  Line {line}: {county}")
    else:
        print("✓ PASS - No null FIPS codes")

    print(f"\nInvalid FIPS codes: {len(invalid_fips)}")
    if invalid_fips:
        print("✗ FAIL - Invalid FIPS codes found:")
        for line, fips, county in invalid_fips[:5]:
            print(f"  Line {line}: {fips} - {county}")
    else:
        print("✓ PASS - All FIPS codes valid")

    print(f"\nDuplicate FIPS codes: {len(duplicate_fips)}")
    if duplicate_fips:
        print("✗ FAIL - Duplicate FIPS codes found:")
        for line, fips, county in duplicate_fips[:5]:
            print(f"  Line {line}: {fips} - {county}")
    else:
        print("✓ PASS - No duplicate FIPS codes")

    # 2. RANGE VALIDATION
    print("\n\n2. RANGE VALIDATION")
    print("-" * 70)

    range_checks = {
        'gini_index': (0, 1, False),
        'composite_index': (0, 100, False),
        'economic_score': (0, 100, False),
        'education_score': (0, 100, False),
        'healthcare_score': (0, 100, False),
        'housing_score': (0, 100, False),
        'food_score': (0, 100, False),
        'disability_score': (0, 100, False),
        'poverty_rate': (0, 100, False),
        'unemployment_rate': (0, 100, False),
        'disability_rate': (0, 100, False),
        'pct_hs_or_higher': (0, 100, False),
        'pct_bachelors_or_higher': (0, 100, False),
    }

    with open('merged/inequality_master.csv', 'r') as f:
        reader = csv.DictReader(f)

        for col, (min_val, max_val, allow_null) in range_checks.items():
            f.seek(0)
            next(reader)  # skip header

            out_of_range = []
            negatives = []

            for i, row in enumerate(reader, start=2):
                value = row[col]

                if value == '' or value is None:
                    if not allow_null:
                        out_of_range.append((i, value, row['county_name']))
                    continue

                try:
                    num = float(value)
                    if num < 0:
                        negatives.append((i, num, row['county_name']))
                    elif num < min_val or num > max_val:
                        out_of_range.append((i, num, row['county_name']))
                except:
                    out_of_range.append((i, value, row['county_name']))

            print(f"\n{col} [{min_val}-{max_val}]:")

            if negatives:
                print(f"  ✗ FAIL - {len(negatives)} negative values:")
                for line, val, county in negatives[:3]:
                    print(f"    Line {line}: {val} - {county}")

            if out_of_range:
                print(f"  ✗ FAIL - {len(out_of_range)} out of range:")
                for line, val, county in out_of_range[:3]:
                    print(f"    Line {line}: {val} - {county}")

            if not negatives and not out_of_range:
                print(f"  ✓ PASS")

    # 3. SOURCE FILE INTEGRITY
    print("\n\n3. SOURCE FILE INTEGRITY")
    print("-" * 70)

    source_files = [
        'food_deserts/food_desert_merged.csv',
        'healthcare/healthcare_desert_merged.csv',
        'housing/housing_crisis_merged.csv',
        'economic/gini_by_county.csv',
        'economic/unemployment_by_county.csv',
        'economic/poverty_depth_by_county.csv',
        'education/education_by_county.csv',
        'disability/census_disability_by_county_2022.csv',
    ]

    all_present = True
    for filepath in source_files:
        path = Path(filepath)
        if path.exists():
            with open(path, 'r') as f:
                line_count = sum(1 for _ in f) - 1  # subtract header

            status = "✓ PASS" if line_count == 3222 else f"✗ FAIL ({line_count} rows)"
            print(f"{filepath}: {status}")

            if line_count != 3222:
                all_present = False
        else:
            print(f"{filepath}: ✗ FAIL - FILE NOT FOUND")
            all_present = False

    # 4. VISUALIZATION DATA
    print("\n\n4. VISUALIZATION DATA SYNC")
    print("-" * 70)

    vis_path = Path('/home/coolhand/html/datavis/dev/data/inequality_master.csv')
    if vis_path.exists():
        print(f"✓ PASS - Visualization data exists")

        # Quick checksum comparison would be ideal here
        import hashlib

        def file_hash(filepath):
            h = hashlib.md5()
            with open(filepath, 'rb') as f:
                h.update(f.read())
            return h.hexdigest()

        source_hash = file_hash('merged/inequality_master.csv')
        vis_hash = file_hash(vis_path)

        if source_hash == vis_hash:
            print("✓ PASS - Files match exactly")
        else:
            print("✗ FAIL - Files differ")
    else:
        print("✗ FAIL - Visualization data not found")

    # 5. OUTLIER CHECK
    print("\n\n5. OUTLIER SAMPLES")
    print("-" * 70)

    with open('merged/inequality_master.csv', 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Top 5 composite index
    sorted_by_comp = sorted(rows, key=lambda r: float(r['composite_index']) if r['composite_index'] else 0, reverse=True)
    print("\nTop 5 composite_index values:")
    for row in sorted_by_comp[:5]:
        print(f"  {row['fips']} {row['county_name']}: {row['composite_index']}")

    # Top 5 Gini
    sorted_by_gini = sorted(rows, key=lambda r: float(r['gini_index']) if r['gini_index'] else 0, reverse=True)
    print("\nTop 5 gini_index values:")
    for row in sorted_by_gini[:5]:
        print(f"  {row['fips']} {row['county_name']}: {row['gini_index']}")

    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    main()
