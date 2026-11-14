"""Pure-Python unit tests for cold_chain_detector periodic and gap behavior."""

from datetime import UTC, datetime, timedelta

from app.services.cold_chain_detector import detect_temperature_violations


def _reading(t0: datetime, minutes: int, temp: float) -> dict[str, object]:
    return {
        "recorded_at": (t0 + timedelta(minutes=minutes)).isoformat(),
        "temperature_celsius": temp,
    }


def test_periodic_out_of_range_readings_persist_beyond_merge_gap() -> None:
    """10-min consecutive high-temp readings must not split on merge_gap_minutes=5."""
    t0 = datetime(2026, 10, 19, 8, 0, 0, tzinfo=UTC)
    readings = [
        _reading(t0, 0, 12.0),
        _reading(t0, 10, 13.0),
        _reading(t0, 20, 12.5),
        _reading(t0, 30, 4.0),
    ]

    violations = detect_temperature_violations(
        readings,
        min_temp_celsius=2.0,
        max_temp_celsius=8.0,
        delay_minutes=15,
        merge_gap_minutes=5,
    )

    assert len(violations) == 1
    assert violations[0].violation_type == "high_temp"
    assert violations[0].duration_minutes == 20.0
    assert violations[0].peak_temperature_celsius == 13.0


def test_brief_safe_recovery_merges_and_longer_recovery_splits() -> None:
    """Safe gap <= merge_gap_minutes merges; > merge_gap_minutes separates excursions."""
    t0 = datetime(2026, 10, 19, 10, 0, 0, tzinfo=UTC)

    merged_readings = [
        _reading(t0, 0, 12.0),
        _reading(t0, 20, 12.2),
        _reading(t0, 23, 5.0),
        _reading(t0, 25, 13.5),
        _reading(t0, 45, 11.8),
        _reading(t0, 52, 4.0),
    ]
    merged = detect_temperature_violations(
        merged_readings, delay_minutes=30, merge_gap_minutes=5
    )
    assert len(merged) == 1
    assert merged[0].duration_minutes == 45.0

    split_readings = [
        _reading(t0, 0, 12.0),
        _reading(t0, 20, 12.2),
        _reading(t0, 26, 5.0),
        _reading(t0, 28, 13.5),
        _reading(t0, 48, 11.8),
        _reading(t0, 55, 4.0),
    ]
    split = detect_temperature_violations(
        split_readings, delay_minutes=30, merge_gap_minutes=5
    )
    assert split == []


def test_large_sensor_outage_splits_consecutive_excursions() -> None:
    """Out-of-range readings separated by > max_sensor_gap_minutes do not bridge."""
    t0 = datetime(2026, 10, 19, 14, 0, 0, tzinfo=UTC)
    readings = [
        _reading(t0, 0, 12.0),
        _reading(t0, 20, 12.5),
        _reading(t0, 110, 13.0),
        _reading(t0, 130, 12.2),
        _reading(t0, 140, 4.0),
    ]

    violations = detect_temperature_violations(
        readings,
        delay_minutes=30,
        merge_gap_minutes=5,
        max_sensor_gap_minutes=60.0,
    )

    assert violations == []
