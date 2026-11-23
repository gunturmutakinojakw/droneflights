# === Stage 25: Месячный отчёт ===
# Project: DroneFlights
from collections import defaultdict


def generate_month_report(flights, month, year):
    """Build a monthly report with totals and comparison to the prior month.

    Args:
        flights: iterable of flight dicts with keys place, duration, height, date.
        month: integer month (1-12) of the report period.
        year: integer year of the report period.

    Returns:
        dict with keys:
          total_flights, total_duration, avg_duration,
          total_height, avg_height, max_flight,
          prev_month_flights, prev_month_duration,
          prev_month_avg_duration,
          growth_percent (None when no previous month data),
          by_place (place -> count).
    """
    current_key = (year, month)
    previous_key = (year, month - 1) if month > 1 else (year - 1, 12)

    by_place = defaultdict(int)
    durations = []
    heights = []
    max_flight = None

    for flight in flights:
        by_place[flight["place"]] += 1
        durations.append(flight["duration"])
        heights.append(flight["height"])
        if max_flight is None or flight["duration"] > max_flight["duration"]:
            max_flight = flight

    total_flights = len(durations)
    total_duration = sum(durations)
    avg_duration = total_duration / total_flights if total_flights else 0.0
    total_height = sum(heights)
    avg_height = total_height / len(heights) if heights else 0.0

    prev_durations = [
        f["duration"] for f in flights if _flight_month(f, previous_key)
    ]
    prev_total_flights = len(prev_durations)
    prev_total_duration = sum(prev_durations)
    prev_avg_duration = (
        prev_total_duration / prev_total_flights if prev_total_flights else 0.0
    )

    growth_percent = None
    if total_flights:
        growth_percent = (
            (total_flights - prev_total_flights) / prev_total_flights * 100.0
            if prev_total_flights else None
        )

    return {
        "month": month,
        "year": year,
        "total_flights": total_flights,
        "total_duration": total_duration,
        "avg_duration": avg_duration,
        "total_height": total_height,
        "avg_height": avg_height,
        "max_flight": max_flight,
        "prev_month_flights": prev_total_flights,
        "prev_month_duration": prev_total_duration,
        "prev_month_avg_duration": prev_avg_duration,
        "growth_percent": growth_percent,
        "by_place": dict(by_place),
    }


def _flight_month(flight, key):
    year, month = key
    return flight["year"] == year and flight["month"] == month
