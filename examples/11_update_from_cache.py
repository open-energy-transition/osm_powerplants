"""Example: Reprocess from API cache.

Use --update to skip CSV cache and rebuild from API cache.
Useful when API cache was updated but CSV cache is stale.
"""

import os

from osm_powerplants import get_cache_dir, get_config
from osm_powerplants.interface import process_countries

config = get_config()
cache_dir = str(get_cache_dir(config))
csv_cache_path = os.path.join(cache_dir, "osm_data.csv")

# Reprocess Germany from API cache (skips CSV cache)
df = process_countries(
    countries=["Germany"],
    csv_cache_path=csv_cache_path,
    cache_dir=cache_dir,
    update=True,  # Skip CSV cache
    osm_config=config,
)

print(f"Processed {len(df)} plants, {df['Capacity'].sum():.0f} MW")
