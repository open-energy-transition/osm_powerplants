# Examples

## Run

```bash
cd examples
python 01_basic_usage.py
```

## List

| # | File | Purpose |
|---|------|---------|
| 1 | `01_basic_usage.py` | Single country extraction |
| 2 | `02_multiple_countries.py` | Multiple countries |
| 3 | `03_configuration.py` | Config options |
| 4 | `04_export_formats.py` | CSV, JSON, GeoJSON |
| 5 | `05_rejection_analysis.py` | Quality tracking |
| 6 | `06_regional_queries.py` | Bbox/radius queries |
| 7 | `07_cache_management.py` | Cache behavior |
| 8 | `08_data_analysis.py` | Pandas analysis |
| 9 | `09_rejection_geojson.py` | Export for JOSM |
| 10 | `10_rejection_keywords.py` | Config tuning |
| 11 | `11_update_from_cache.py` | Reprocess from API cache |

## Notes

- Small countries (Luxembourg, Cyprus) for fast execution
- First run downloads from API; subsequent runs use cache
