#!/usr/bin/env python3
"""
Example 10: Rejection Keyword Analysis
======================================

Identify problematic OSM tag values to improve config mappings.
Keywords show actual values that failed to match source_mapping
or technology_mapping in config.
"""

from osm_powerplants import Units, get_cache_dir, get_config
from osm_powerplants.models import RejectionReason
from osm_powerplants.quality.rejection import RejectionTracker
from osm_powerplants.retrieval.client import OverpassAPIClient
from osm_powerplants.workflow import Workflow

config = get_config()
cache_dir = str(get_cache_dir(config))

# Strict settings
config["missing_name_allowed"] = False
config["missing_technology_allowed"] = False

tracker = RejectionTracker()
units = Units()

with OverpassAPIClient(cache_dir=cache_dir) as client:
    workflow = Workflow(client, tracker, units, config)
    workflow.process_country_data("Malta")

print(f"Rejections: {tracker.get_total_count()}\n")

# Analyze keywords for each reason
for reason in tracker.get_unique_rejection_reasons():
    keywords = tracker.get_unique_keyword(reason)
    if keywords:
        print(f"{reason.value}:")
        for kw, count in keywords.items():
            print(f"  '{kw}': {count}")
        print()

# Practical use: find values to add to config
print("=== Config Improvement Suggestions ===")
source_keywords = tracker.get_unique_keyword(RejectionReason.MISSING_SOURCE_TYPE)
if source_keywords:
    print("Add to source_mapping:")
    for kw in source_keywords:
        print(f"  - '{kw}'")

tech_keywords = tracker.get_unique_keyword(RejectionReason.MISSING_TECHNOLOGY_TYPE)
if tech_keywords:
    print("Add to technology_mapping:")
    for kw in tech_keywords:
        print(f"  - '{kw}'")
