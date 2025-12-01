# Quality Tracking

Track why OSM elements are rejected during processing.

## Basic Usage

```python
from osm_powerplants import Units, get_config, get_cache_dir
from osm_powerplants.quality.rejection import RejectionTracker
from osm_powerplants.retrieval.client import OverpassAPIClient
from osm_powerplants.workflow import Workflow

config = get_config()
config["missing_name_allowed"] = False  # Strict mode

tracker = RejectionTracker()
units = Units()

with OverpassAPIClient(cache_dir=str(get_cache_dir(config))) as client:
    workflow = Workflow(client, tracker, units, config)
    workflow.process_country_data("Malta")

print(tracker.get_summary_string())
```

## Rejection Reasons

| Reason | OSM Fix |
|--------|---------|
| `Missing source tag` | Add `plant:source` |
| `Missing technology tag` | Add `plant:method` |
| `Missing output tag` | Add `plant:output:electricity` |
| `Capacity placeholder value` | Add actual value |
| `Within existing plant` | Already counted |

## Analysis

```python
from osm_powerplants.models import RejectionReason

# Filter by reason
missing = tracker.get_rejections_by_reason(RejectionReason.MISSING_OUTPUT_TAG)

# Find problematic values
keywords = tracker.get_unique_keyword(RejectionReason.MISSING_SOURCE_TYPE)
# {'coal_gas': 5} → add to source_mapping
```

## Export

```python
tracker.generate_report().to_csv("rejections.csv", index=False)
tracker.save_geojson("rejections.geojson")
tracker.save_geojson_by_reasons("output/")  # One file per reason
```

Open GeoJSON in JOSM or iD editor to fix OSM data.
