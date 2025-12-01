"""Tests for interface validation."""


def test_valid_fueltypes():
    """Test VALID_FUELTYPES constant."""
    from osm_powerplants.interface import VALID_FUELTYPES

    assert "Solar" in VALID_FUELTYPES
    assert "Wind" in VALID_FUELTYPES
    assert "Hydro" in VALID_FUELTYPES
    assert "Nuclear" in VALID_FUELTYPES
    assert "Natural Gas" in VALID_FUELTYPES


def test_valid_technologies():
    """Test VALID_TECHNOLOGIES constant."""
    from osm_powerplants.interface import VALID_TECHNOLOGIES

    assert "PV" in VALID_TECHNOLOGIES
    assert "Onshore" in VALID_TECHNOLOGIES
    assert "Offshore" in VALID_TECHNOLOGIES
    assert "Run-Of-River" in VALID_TECHNOLOGIES
    assert "Pumped Storage" in VALID_TECHNOLOGIES


def test_valid_sets():
    """Test VALID_SETS constant."""
    from osm_powerplants.interface import VALID_SETS

    assert "PP" in VALID_SETS
    assert "Store" in VALID_SETS
    assert "CHP" in VALID_SETS


def test_validate_and_standardize_df():
    """Test DataFrame validation and standardization."""
    import pandas as pd

    from osm_powerplants.interface import validate_and_standardize_df

    df = pd.DataFrame(
        {
            "projectID": ["1", "2"],
            "Country": ["Germany", "France"],
            "Fueltype": ["Solar", "Wind"],
            "Technology": ["PV", "Onshore"],
            "Capacity": [10.0, 20.0],
            "config_hash": ["abc", "def"],  # metadata to remove
        }
    )

    result = validate_and_standardize_df(df)

    assert "config_hash" not in result.columns
    assert "projectID" in result.columns
    assert len(result) == 2


def test_validate_countries_mixed_formats():
    """Test validation with mixed country formats."""
    from osm_powerplants import validate_countries

    valid, codes = validate_countries(["Germany", "FR", "ESP"])

    assert len(valid) == 3
    assert codes["Germany"] == "DE"
    assert codes["FR"] == "FR"
    assert codes["ESP"] == "ES"


def test_validate_countries_common_names():
    """Test validation with common country name variants."""
    from osm_powerplants import validate_countries

    # USA variant
    valid, codes = validate_countries(["USA"])
    assert codes["USA"] == "US"


def test_validate_countries_empty():
    """Test validation with empty list returns empty."""
    from osm_powerplants import validate_countries

    valid, codes = validate_countries([])
    assert len(valid) == 0
    assert len(codes) == 0
