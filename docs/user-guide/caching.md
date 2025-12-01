# Caching

Three-level cache system for fast repeated queries.

## Cache Levels

| Level | Location | Content |
|-------|----------|---------|
| 1 | `osm_data.csv` | Final processed output |
| 2 | `processed_units.json` | Processed Unit objects |
| 3 | `*_dc/` directories | Raw OSM elements |

## Cache Location

| OS | Path |
|----|------|
| Linux | `~/.cache/osm-powerplants/` |
| macOS | `~/Library/Caches/osm-powerplants/` |
| Windows | `%LOCALAPPDATA%\osm-powerplants\Cache\` |

Custom location:

```yaml
cache_dir: /path/to/cache
```

## Force Refresh

Re-download all data from Overpass API:

```bash
osm-powerplants process Germany --force-refresh
```

Note: For large countries (Germany, France), this can take several minutes due to API queries.

## Update from API Cache

When analyzing rejections or debugging, you may run processing with `--force-refresh` which updates the API cache. To then update the CSV output without re-downloading:

```bash
osm-powerplants process Germany --update -o germany.csv
```

This skips the CSV cache but reuses the API cache, saving time for large countries.

**Typical workflow:**

```bash
# 1. Force refresh to get latest OSM data (slow for large countries)
osm-powerplants process Germany --force-refresh -o germany.csv

# 2. Analyze rejections, tune config...

# 3. Reprocess with updated config (fast - uses API cache)
osm-powerplants process Germany --update -o germany.csv
```

## Clear Cache

```bash
rm -rf ~/.cache/osm-powerplants/*
```

## Config Hash

Cache is automatically invalidated when processing parameters change. The config hash is computed from:

- `source_mapping`, `technology_mapping`
- `plants_only`, `missing_*_allowed`
- `capacity_extraction`, `units_clustering`, `units_reconstruction`

## Performance

| Cache Hit | Speedup |
|-----------|---------|
| CSV | 50-100x |
| Units | 10-30x |
| API | 2-5x |
