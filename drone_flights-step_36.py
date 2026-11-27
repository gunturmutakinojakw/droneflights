# === Stage 36: Активность по дням недели ===
# Project: DroneFlights
"""Weekday activity map for DroneFlights flight journal."""

from collections import Counter


def build_weekday_activity_map(flights):
    """Return a textual map of flights per weekday.

    Args:
        flights: iterable of flight records. Each record is a mapping with
            an 'activity_date' field containing a 'week()' attribute, or a
            datetime-like object exposing 'strftime("%A")'.

    Returns:
        A string listing each weekday alongside its flight count.
    """
    counts = Counter()
    for flight in flights:
        day_name = _extract_weekday(flight)
        counts[day_name] += 1

    lines = ["Weekday activity map:", ""]
    for day_name in sorted(counts):
        lines.append(f"  {day_name:<9}: {counts[day_name]}")
    return "\n".join(lines)


def _extract_weekday(flight):
    """Extract the weekday name from a flight record."""
    date = flight.get("activity_date")
    if date is not None and hasattr(date, "week"):
        return date.week().strftime("%A")
    if date is not None and hasattr(date, "strftime"):
        return date.strftime("%A")
    return "unknown"


def format_activity_summary(flights):
    """Return a one-line summary of total flights and busiest weekday."""
    counts = Counter(_extract_weekday(f) for f in flights)
    if not counts:
        return "No flights recorded."
    busiest_day, busiest_count = counts.most_common(1)[0]
    return (f"Total flights: {sum(counts.values())} | "
            f"Busiest weekday: {busiest_day} ({busiest_count})")
