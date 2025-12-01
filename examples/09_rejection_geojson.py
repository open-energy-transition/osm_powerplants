#!/usr/bin/env python3
"""
Example 9: Rejection GeoJSON Export
===================================

Export rejected elements as GeoJSON for visualization
in mapping tools (JOSM, iD editor, geojson.io).

Usage in JOSM:
  1. Run this script to generate GeoJSON files
  2. Open JOSM → File → Open → select GeoJSON
  3. Click points to see rejection details
  4. Use osm_element URL to edit and fix
"""

from osm_powerplants import Units, get_cache_dir, get_config
from osm_powerplants.models import RejectionReason
from osm_powerplants.quality.rejection import RejectionTracker
from osm_powerplants.retrieval.client import OverpassAPIClient
from osm_powerplants.workflow import Workflow

config = get_config()
cache_dir = str(get_cache_dir(config))

# Strict settings to capture rejections
config["missing_name_allowed"] = False
config["missing_technology_allowed"] = False
config["missing_start_date_allowed"] = False

tracker = RejectionTracker()
units = Units()

with OverpassAPIClient(cache_dir=cache_dir) as client:
    workflow = Workflow(client, tracker, units, config)
    workflow.process_country_data("Malta")

print(f"Total rejections: {tracker.get_total_count()}")

# Export all rejections
tracker.save_geojson("malta_rejections.geojson")
print("Saved: malta_rejections.geojson")

# Export by reason (separate files for targeted fixing)
tracker.save_geojson_by_reasons(".", prefix="malta")

# Export single reason
if tracker.get_rejections_by_reason(RejectionReason.MISSING_OUTPUT_TAG):
    tracker.save_geojson(
        "malta_missing_capacity.geojson", reason=RejectionReason.MISSING_OUTPUT_TAG
    )
    print("Saved: malta_missing_capacity.geojson")

# Show GeoJSON structure
geojson = tracker.generate_geojson()
if geojson["features"]:
    print("\n=== GeoJSON Feature Properties ===")
    props = geojson["features"][0]["properties"]
    for key in ["osm_element", "rejection_reason", "rejection_keywords"]:
        print(f"  {key}: {props.get(key)}")
