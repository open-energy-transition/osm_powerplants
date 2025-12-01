# CLI Reference

## Commands

### process

```bash
osm-powerplants process <countries> [options]
```

| Option | Description |
|--------|-------------|
| `-o`, `--output` | Output CSV path (default: `osm_data.csv`) |
| `-c`, `--config` | Custom config file |
| `--force-refresh` | Ignore all cache, re-download from API |
| `--update` | Reprocess from API cache (skip CSV cache) |

```bash
osm-powerplants process Germany -o germany.csv
osm-powerplants process France Spain Italy -o europe.csv
osm-powerplants process DE FR ES -o countries.csv  # ISO codes
osm-powerplants process "United States" -o usa.csv  # Quotes for spaces
```

### info

```bash
osm-powerplants info
```

Shows config file path, cache directory, and current settings.

## Country Names

Accepts: full names, ISO-2, ISO-3, common variations.

Invalid names show suggestions:

```
❌ 'Germny'
   ℹ️  Did you mean: 'Germany', 'Armenia'
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error |
