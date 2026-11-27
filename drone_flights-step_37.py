# === Stage 37: Что требует внимания ===
# Project: DroneFlights
"""DroneFlights stage 37: attention summary for overdue, stuck, and incomplete flights."""

from datetime import datetime

OVERDUE_THRESHOLD = datetime(1970, 1, 1)
STUCK_THRESHOLD = 60


def _parse_date(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.strip())
    return None


def _parse_duration(value):
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        text = value.strip().lower()
        unit = "minute" if "min" in text else "second"
        try:
            return float(text.replace(unit, ""))
        except ValueError:
            return None
    return None


def find_overdue_flights(flights, reference=None):
    reference = reference or datetime.now()
    overdue = []
    for flight in flights:
        flight_date = _parse_date(flight.get("date"))
        if flight_date and flight_date <= OVERDUE_THRESHOLD:
            overdue.append(flight)
    return overdue


def find_stuck_flights(flights):
    stuck = []
    for flight in flights:
        duration = _parse_duration(flight.get("duration"))
        if duration and duration > STUCK_THRESHOLD:
            stuck.append(flight)
    return stuck


def find_incomplete_flights(flights):
    incomplete = []
    for flight in flights:
        required = ("place", "duration", "height", "date")
        if any(flight.get(field) in (None, "") for field in required):
            incomplete.append(flight)
    return incomplete


def build_attention_summary(flights, reference=None):
    overdue = find_overdue_flights(flights, reference)
    stuck = find_stuck_flights(flights)
    incomplete = find_incomplete_flights(flights)
    return {
        "overdue": overdue,
        "stuck": stuck,
        "incomplete": incomplete,
        "total": len(flights),
    }
