# Data Output

## Columns

| Column | Type | Description |
|--------|------|-------------|
| `projectID` | string | `OSM_plant:{type}/{id}` |
| `Name` | string | Plant name (may be empty) |
| `Country` | string | Full country name |
| `lat`, `lon` | float | WGS84 coordinates |
| `Fueltype` | string | Primary fuel type |
| `Technology` | string | Generation technology |
| `Set` | string | PP, Store, or CHP |
| `Capacity` | float | MW |
| `DateIn` | int | Commissioning year |

## Export Formats

```python
df.to_csv("plants.csv", index=False)
df.to_excel("plants.xlsx", index=False)
df.to_parquet("plants.parquet", index=False)

# GeoJSON
units.save_geojson_report("plants.geojson")
```

## Data Quality

Capacity sources (priority order):

1. Direct tag: `plant:output:electricity`
2. Aggregated from generators
3. Estimated from geometry (when enabled)

Check completeness:

```python
print(df.isnull().sum())
print(f"Capacity coverage: {df['Capacity'].notna().mean():.0%}")
```
