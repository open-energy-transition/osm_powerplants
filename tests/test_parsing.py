"""Tests for parsing utilities."""


def test_capacity_extractor_init():
    """Test CapacityExtractor initialization."""
    from osm_powerplants import get_config
    from osm_powerplants.parsing.capacity import CapacityExtractor
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    config = get_config()
    extractor = CapacityExtractor(tracker, config)
    assert extractor is not None


def test_capacity_extractor_basic():
    """Test basic capacity extraction."""
    from osm_powerplants import get_config
    from osm_powerplants.parsing.capacity import CapacityExtractor
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    config = get_config()
    extractor = CapacityExtractor(tracker, config)

    element = {"id": 1, "type": "node", "tags": {"plant:output:electricity": "100 MW"}}
    success, value, source = extractor.basic_extraction(
        element, "plant:output:electricity"
    )
    assert success
    assert value == 100.0


def test_capacity_extractor_units():
    """Test capacity extraction with MW units."""
    from osm_powerplants import get_config
    from osm_powerplants.parsing.capacity import CapacityExtractor
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    config = get_config()
    extractor = CapacityExtractor(tracker, config)

    # MW - basic extraction handles MW
    element = {"id": 1, "type": "node", "tags": {"plant:output:electricity": "50 MW"}}
    success, value, _ = extractor.basic_extraction(element, "plant:output:electricity")
    assert success
    assert value == 50.0


def test_capacity_extractor_placeholder():
    """Test capacity extraction rejects placeholders."""
    from osm_powerplants import get_config
    from osm_powerplants.parsing.capacity import CapacityExtractor
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    config = get_config()
    extractor = CapacityExtractor(tracker, config)

    element = {"id": 1, "type": "node", "tags": {"plant:output:electricity": "yes"}}
    success, value, _ = extractor.basic_extraction(element, "plant:output:electricity")
    assert not success
