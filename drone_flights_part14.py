# === Stage 14: Группировка ===
# Project: DroneFlights
from collections import defaultdict
from datetime import date


def group_flights_by_duration(flights):
    """Group flights by their duration and count how many are in each group.

    Args:
        flights: An iterable of flight records. Each record must expose a
            ``duration`` attribute (for example, a ``Flight`` instance).

    Returns:
        A dictionary mapping each distinct duration value to the number of
        flights that share it. The original order of first appearance is
        preserved using an insertion-ordered dict.
    """
    groups = defaultdict(int)
    for flight in flights:
        groups[flight.duration] += 1
    return dict(groups)


def group_flights_by_duration_sorted(flights):
    """Group flights by duration and return them sorted by duration.

    Args:
        flights: An iterable of flight records, each with a ``duration``
            attribute.

    Returns:
        A list of ``(duration, count)`` tuples ordered by ascending duration.
    """
    counts = group_flights_by_duration(flights)
    return sorted(counts.items())


def summarize_duration_distribution(flights):
    """Build a human-readable summary of the flight duration distribution.

    Args:
        flights: An iterable of flight records, each with a ``duration``
            attribute.

    Returns:
        A multi-line string describing each duration group and its count,
        followed by the total number of flights.
    """
    grouped = group_flights_by_duration_sorted(flights)
    lines = []
    for duration, count in grouped:
        lines.append(f"duration={duration} count={count}")
    total = sum(count for _, count in grouped)
    lines.append(f"total_flights={total}")
    return "\n".join(lines)


if __name__ == "__main__":
    class Flight:
        def __init__(self, place, duration, altitude, flight_date):
            self.place = place
            self.duration = duration
            self.altitude = altitude
            self.flight_date = flight_date

    sample = [
        Flight("A", 10, 50, date(2024, 1, 1)),
        Flight("B", 25, 80, date(2024, 1, 2)),
        Flight("C", 10, 60, date(2024, 1, 3)),
        Flight("D", 25, 70, date(2024, 1, 4)),
    ]
    print(summarize_duration_distribution(sample))
