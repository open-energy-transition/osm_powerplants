# Processing Pipeline

## Overview

```
Input → Cache Check → API Query → Parse Elements → Enhance → Output
```

## Cache Check

```
CSV cache (fast) → Units cache → API cache → Fresh API query
```

## Overpass Query

```sql
[out:json][timeout:300];
area["ISO3166-1"="DE"][admin_level=2]->.boundaryarea;
(node["power"="plant"](area.boundaryarea);
 way["power"="plant"](area.boundaryarea);
 relation["power"="plant"](area.boundaryarea););
out body;
```

## Tag Extraction

Priority order for each field:

- **Fuel**: `plant:source` → `generator:source`
- **Technology**: `plant:method` → `plant:type`
- **Capacity**: `plant:output:electricity` (parsed: `50 MW` → 50.0)

## Enhancement

**Reconstruction**: When plant lacks tags but contains generators, aggregate generator info.

**Clustering**: Group nearby solar/wind generators into farms (DBSCAN).

## Capacity Parsing

| Input | Output (MW) |
|-------|-------------|
| `50 MW` | 50.0 |
| `1.5GW` | 1500.0 |
| `100kWp` | 0.1 |
