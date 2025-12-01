# SPDX-FileCopyrightText: Contributors to osm-powerplants
#
# SPDX-License-Identifier: MIT

"""
Core configuration and path utilities for osm_powerplants.
"""

import logging
from pathlib import Path

import yaml
from platformdirs import user_cache_dir, user_config_dir

logger = logging.getLogger(__name__)

# Package directories
PACKAGE_DIR = Path(__file__).parent
CONFIG_DIR = user_config_dir("osm-powerplants")
CACHE_DIR = user_cache_dir("osm-powerplants")

# Ensure cache directory exists (config dir created only when needed)
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)


def get_default_config_path() -> Path:
    """Get path to the default config file.

    Search order (first found wins):
    1. User config (~/.config/osm-powerplants/config.yaml)
    2. Project root (for development)
    3. Bundled in package (fallback)
    """
    # 1. User config directory (highest priority - user overrides)
    user_config = Path(CONFIG_DIR) / "config.yaml"
    if user_config.exists():
        return user_config

    # 2. Project root (for development)
    pkg_config = PACKAGE_DIR.parent.parent / "config.yaml"
    if pkg_config.exists():
        return pkg_config

    # 3. Bundled in package (fallback for pip-installed)
    return PACKAGE_DIR / "config.yaml"


def _ensure_user_config() -> Path:
    """Copy bundled config to user config directory if it doesn't exist.

    Returns the user config path.
    """
    user_config_dir = Path(CONFIG_DIR)
    user_config = user_config_dir / "config.yaml"

    if not user_config.exists():
        # Find bundled config
        bundled_config = PACKAGE_DIR / "config.yaml"
        if bundled_config.exists():
            user_config_dir.mkdir(parents=True, exist_ok=True)
            import shutil

            shutil.copy(bundled_config, user_config)
            logger.info(f"Created user config at {user_config}")

    return user_config


def get_config(filename: str | None = None) -> dict:
    """
    Load configuration from YAML file.

    Parameters
    ----------
    filename : str, optional
        Path to configuration file. If None, uses default location
        and ensures user config exists.

    Returns
    -------
    dict
        Configuration dictionary
    """
    if filename is not None:
        config_path = Path(filename)
    else:
        # Ensure user config exists (copies bundled if needed)
        _ensure_user_config()
        config_path = get_default_config_path()

    if not config_path.exists():
        logger.warning(f"Config file not found: {config_path}")
        return {}

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    return config


def get_cache_dir(config: dict | None = None) -> Path:
    """
    Get cache directory path.

    Parameters
    ----------
    config : dict, optional
        Configuration with optional cache_dir override

    Returns
    -------
    Path
        Cache directory path
    """
    if config and config.get("cache_dir"):
        cache_dir = Path(config["cache_dir"]).expanduser()
    else:
        cache_dir = Path(CACHE_DIR)

    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir
