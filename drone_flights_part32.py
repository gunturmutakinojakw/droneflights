# === Stage 32: Сравнение периодов ===
# Project: DroneFlights
from datetime import date, timedelta


def compare_periods(period_a, period_b, date_field="start_date"):
    """Compare two periods by key metrics and return a descriptive result.

    Args:
        period_a: dict with keys start_date, end_date, duration_days.
        period_b: dict with keys start_date, end_date, duration_days.
        date_field: name of the field holding the period start date.

    Returns:
        dict describing the comparison outcome.
    """
    date_a = period_a[date_field]
    date_b = period_b[date_field]

    span_a_days = (period_a["end_date"] - date_a).days
    span_b_days = (period_b["end_date"] - date_b).days

    earlier_start = date_a < date_b
    longer_span = span_a_days >= span_b_days
    overlapping = date_a <= date_b and date_b <= period_a["end_date"]

    if earlier_start and longer_span:
        verdict = "period_a dominates period_b"
    elif later_start := date_b > date_a and span_b_days > span_a_days:
        verdict = "period_b dominates period_a"
    elif overlapping:
        verdict = "periods overlap"
    else:
        verdict = "periods are disjoint"

    return {
        "period_a_start": date_a,
        "period_b_start": date_b,
        "period_a_span_days": span_a_days,
        "period_b_span_days": span_b_days,
        "earlier_start": earlier_start,
        "longer_span": longer_span,
        "overlapping": overlapping,
        "verdict": verdict,
    }


if __name__ == "__main__":
    sample_a = {
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 1, 10),
        "duration_days": 9,
        "location": "Hangar A",
        "max_height_m": 120,
    }
    sample_b = {
        "start_date": date(2024, 2, 1),
        "end_date": date(2024, 2, 15),
        "duration_days": 14,
        "location": "Hangar B",
        "max_height_m": 90,
    }

    result = compare_periods(sample_a, sample_b)
    for key, value in result.items():
        print(f"{key}: {value}")
