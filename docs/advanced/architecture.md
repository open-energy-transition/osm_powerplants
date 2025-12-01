# Architecture

## Package Structure

```
osm_powerplants/
├── cli.py           # Command-line interface
├── core.py          # Configuration, paths
├── interface.py     # High-level API
├── models.py        # Unit, Units, RejectionReason
├── workflow.py      # Processing orchestration
├── retrieval/       # Overpass API, caching
├── parsing/         # OSM element parsing
├── enhancement/     # Clustering, reconstruction
└── quality/         # Rejection tracking
```

## Data Flow

```
Countries → Validate → Retrieve (cache/API) → Parse → Enhance → Validate → DataFrame
```

1. **Validate**: Check country names via pycountry
2. **Retrieve**: Check cache hierarchy, query Overpass API if needed
3. **Parse**: Extract fuel type, technology, capacity from OSM tags
4. **Enhance**: Cluster generators, reconstruct plants from orphans
5. **Validate**: Ensure valid fuel types, technologies, sets

## Key Classes

**Unit**: Single power plant with all attributes

**Units**: Collection with filtering and export methods

**Workflow**: Orchestrates the processing pipeline

**OverpassAPIClient**: Handles API queries with retry and caching

**RejectionTracker**: Records why elements fail processing
