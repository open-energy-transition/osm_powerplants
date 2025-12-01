# Configuration

Config file location: `~/.config/osm-powerplants/config.yaml`

## Main Options

```yaml
force_refresh: false          # Ignore cache, re-download
plants_only: true             # Skip standalone generators
missing_name_allowed: true    # Accept unnamed plants
missing_technology_allowed: false
missing_start_date_allowed: true
```

## Capacity Extraction

```yaml
capacity_extraction:
  enabled: true

capacity_estimation:
  enabled: false  # Estimate from geometry (solar)
```

## Clustering & Reconstruction

```yaml
units_clustering:
  enabled: false  # Group nearby generators

units_reconstruction:
  enabled: true   # Rebuild plants from orphaned generators
  min_generators_for_reconstruction: 2
```

## Source Mapping

Maps OSM tags to standardized fuel types:

```yaml
source_mapping:
  Solar: [solar, solar;battery, photovoltaic]
  Wind: [wind, wind;solar]
  Hydro: [hydro, hydro;oil, water]
  Natural Gas: [gas, gas;oil]
  # ... see config.yaml for complete list
```

## Technology Mapping

```yaml
technology_mapping:
  PV: [photovoltaic, solar_photovoltaic_panel]
  Onshore: [horizontal_axis, wind_turbine]
  Run-Of-River: [run-of-the-river, francis_turbine]
  # ... see config.yaml for complete list
```

## API Settings

```yaml
overpass_api:
  timeout: 1200
  max_retries: 3
  retry_delay: 60
```

## Custom Config

```bash
osm-powerplants process Spain -c my-config.yaml -o spain.csv
```

```python
config = get_config("/path/to/my-config.yaml")
```
