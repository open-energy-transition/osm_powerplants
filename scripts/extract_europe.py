#!/usr/bin/env python3
"""
Full European extraction script.

Processes all 36 European countries (excluding Kosovo) with a single client
and shared Units instance for optimal performance.

Usage:
    python scripts/extract_europe.py [--clear-cache]
"""

import argparse
import shutil
import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from osm_powerplants import Units, get_cache_dir, get_config
from osm_powerplants.interface import validate_countries
from osm_powerplants.quality.rejection import RejectionTracker
from osm_powerplants.retrieval.client import OverpassAPIClient
from osm_powerplants.workflow import Workflow

EUROPEAN_COUNTRIES = [
    "Albania",
    "Austria",
    "Belgium",
    "Bosnia and Herzegovina",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Moldova",
    "Montenegro",
    "Netherlands",
    "North Macedonia",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Serbia",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "Ukraine",
    "United Kingdom",
]


def clear_cache(cache_dir: Path) -> None:
    """Remove all cache files."""
    if cache_dir.exists():
        print(f"Clearing cache: {cache_dir}")
        shutil.rmtree(cache_dir)
        cache_dir.mkdir(parents=True)
        print("Cache cleared.")
    else:
        print(f"Cache directory does not exist: {cache_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract European power plants from OSM"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear all cache before processing",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="osm_europe.csv",
        help="Output CSV file (default: osm_europe.csv)",
    )
    args = parser.parse_args()

    # Load config
    config = get_config()
    cache_dir = get_cache_dir(config)

    print(f"Cache directory: {cache_dir}")
    print(f"Output file: {args.output}")
    print(f"Countries: {len(EUROPEAN_COUNTRIES)}")

    # Clear cache if requested
    if args.clear_cache:
        clear_cache(cache_dir)

    # Validate countries
    valid_countries, country_codes = validate_countries(
        EUROPEAN_COUNTRIES, config.get("omitted_countries", [])
    )
    print(f"Validated {len(valid_countries)} countries")

    # Single Units instance for all countries
    all_units = Units()
    all_rejections = RejectionTracker()

    # Get client params
    api_config = config.get("overpass_api", {})
    client_params = {
        "cache_dir": str(cache_dir),
        "api_url": api_config.get("api_url", "https://overpass-api.de/api/interpreter"),
        "timeout": api_config.get("timeout", 1200),
        "max_retries": api_config.get("max_retries", 3),
        "retry_delay": api_config.get("retry_delay", 60),
        "show_progress": api_config.get("show_progress", True),
    }

    # Process all countries with single client
    with OverpassAPIClient(**client_params) as client:
        for i, country in enumerate(valid_countries, 1):
            print(f"\n{'='*60}")
            print(
                f"Processing {i}/{len(valid_countries)}: {country} ({country_codes[country]})"
            )
            print("=" * 60)

            country_units = Units()
            country_tracker = RejectionTracker()

            workflow = Workflow(
                client=client,
                rejection_tracker=country_tracker,
                units=country_units,
                config=config,
            )

            try:
                workflow.process_country_data(country)

                # Add to global collection
                for unit in country_units:
                    all_units.add_unit(unit)

                # Merge rejections
                for rej_list in country_tracker.rejected_elements.values():
                    for rej in rej_list:
                        all_rejections.rejected_elements.setdefault(rej.id, []).append(
                            rej
                        )

                print(f"✓ {country}: {len(country_units)} plants")
                print(country_tracker.get_summary_string())

            except Exception as e:
                print(f"✗ {country}: Error - {e}")
                continue

    # Summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print("=" * 60)

    df = all_units.to_dataframe()
    total_capacity = df["Capacity"].sum() if "Capacity" in df.columns else 0

    print(f"Total plants: {len(df):,}")
    print(f"Total capacity: {total_capacity:,.0f} MW ({total_capacity/1000:,.1f} GW)")
    print(f"Total rejections: {all_rejections.get_total_count():,}")

    # By country
    if len(df) > 0:
        print("\nTop 10 countries by capacity:")
        by_country = df.groupby("Country")["Capacity"].agg(["count", "sum"])
        by_country.columns = ["Plants", "Capacity_MW"]
        by_country = by_country.sort_values("Capacity_MW", ascending=False)
        print(by_country.head(10).to_string())

        print("\nBy fuel type:")
        by_fuel = df.groupby("Fueltype")["Capacity"].agg(["count", "sum"])
        by_fuel.columns = ["Plants", "Capacity_MW"]
        by_fuel = by_fuel.sort_values("Capacity_MW", ascending=False)
        print(by_fuel.to_string())

    # Save output
    df.to_csv(args.output, index=False)
    print(f"\n✓ Saved {len(df)} plants to {args.output}")

    # Save rejection summary
    rejection_file = args.output.replace(".csv", "_rejections.txt")
    with open(rejection_file, "w") as f:
        f.write(all_rejections.get_summary_string())
    print(f"✓ Saved rejection summary to {rejection_file}")


if __name__ == "__main__":
    main()
