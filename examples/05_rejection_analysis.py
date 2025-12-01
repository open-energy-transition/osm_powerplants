#!/usr/bin/env python3
"""
Example 5: Rejection Analysis
=============================

Track why OSM elements are rejected during processing.
Uses strict config to demonstrate rejection tracking.
"""

from osm_powerplants import Units, get_cache_dir, get_config
from osm_powerplants.models import RejectionReason
from osm_powerplants.quality.rejection import RejectionTracker
from osm_powerplants.retrieval.client import OverpassAPIClient
from osm_powerplants.workflow import Workflow

config = get_config()
cache_dir = str(get_cache_dir(config))

# Strict config to capture all data quality issues
config["missing_name_allowed"] = False
config["missing_technology_allowed"] = False
config["missing_start_date_allowed"] = False

tracker = RejectionTracker()
units = Units()

with OverpassAPIClient(cache_dir=cache_dir) as client:
    workflow = Workflow(client, tracker, units, config)
    workflow.process_country_data("Malta")

# Summary
print(f"Valid units: {len(units)}")
print(f"Rejected elements: {tracker.get_total_count()}")

# Breakdown by reason
print("\n=== Rejection Reasons ===")
for reason, count in tracker.get_summary().items():
    print(f"  {reason}: {count}")

# Detailed statistics
stats = tracker.get_statistics()
print("\n=== Statistics ===")
print(f"  With coordinates: {stats['has_coordinates']}")
print(f"  Countries: {list(stats['by_country'].keys())}")

# Filter by specific reason
print("\n=== Missing Output Tag Details ===")
missing_output = tracker.get_rejections_by_reason(RejectionReason.MISSING_OUTPUT_TAG)
for r in missing_output[:3]:
    print(f"  {r.url}")

# Export report
report = tracker.generate_report()
if not report.empty:
    report.to_csv("malta_rejections.csv", index=False)
    print(f"\nSaved: malta_rejections.csv ({len(report)} rows)")
