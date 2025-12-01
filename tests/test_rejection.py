"""Tests for rejection tracking."""


def test_rejection_tracker_init():
    """Test RejectionTracker initialization."""
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    assert tracker.get_total_count() == 0


def test_rejection_tracker_add():
    """Test adding rejections."""
    from osm_powerplants.models import RejectionReason
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()

    tracker.add_rejection(
        element_id=123,
        element_type="node",
        reason=RejectionReason.MISSING_SOURCE_TAG,
        details="No source tag found",
    )

    assert tracker.get_total_count() == 1


def test_rejection_tracker_summary():
    """Test rejection summary."""
    from osm_powerplants.models import RejectionReason
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()

    tracker.add_rejection(
        element_id=1, element_type="node", reason=RejectionReason.MISSING_SOURCE_TAG
    )
    tracker.add_rejection(
        element_id=2, element_type="node", reason=RejectionReason.MISSING_SOURCE_TAG
    )
    tracker.add_rejection(
        element_id=3, element_type="way", reason=RejectionReason.CAPACITY_ZERO
    )

    summary = tracker.get_summary()
    assert summary[RejectionReason.MISSING_SOURCE_TAG.value] == 2
    assert summary[RejectionReason.CAPACITY_ZERO.value] == 1


def test_rejection_tracker_filter_by_reason():
    """Test filtering rejections by reason."""
    from osm_powerplants.models import RejectionReason
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    tracker.add_rejection(
        element_id=1, element_type="node", reason=RejectionReason.MISSING_SOURCE_TAG
    )
    tracker.add_rejection(
        element_id=2, element_type="way", reason=RejectionReason.CAPACITY_ZERO
    )
    tracker.add_rejection(
        element_id=3, element_type="node", reason=RejectionReason.MISSING_SOURCE_TAG
    )

    filtered = tracker.get_rejections_by_reason(RejectionReason.MISSING_SOURCE_TAG)
    assert len(filtered) == 2


def test_rejection_tracker_generate_report():
    """Test report generation."""
    from osm_powerplants.models import RejectionReason
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    tracker.add_rejection(
        element_id=123,
        element_type="node",
        reason=RejectionReason.MISSING_SOURCE_TAG,
        country="Germany",
    )

    report = tracker.generate_report()
    assert len(report) == 1
    assert "element_id" in report.columns
    assert "reason" in report.columns


def test_rejection_tracker_keywords():
    """Test keyword tracking."""
    from osm_powerplants.models import RejectionReason
    from osm_powerplants.quality.rejection import RejectionTracker

    tracker = RejectionTracker()
    tracker.add_rejection(
        element_id=1,
        element_type="node",
        reason=RejectionReason.MISSING_SOURCE_TYPE,
        keywords="coal_gas",
    )
    tracker.add_rejection(
        element_id=2,
        element_type="node",
        reason=RejectionReason.MISSING_SOURCE_TYPE,
        keywords="coal_gas",
    )

    keywords = tracker.get_unique_keyword(RejectionReason.MISSING_SOURCE_TYPE)
    assert keywords.get("coal_gas") == 2
