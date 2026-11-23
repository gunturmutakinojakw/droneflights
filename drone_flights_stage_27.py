# === Stage 27: Серии по дням ===
# Project: DroneFlights
from collections import defaultdict


def group_consecutive_flights(flights):
    """Group flights into runs of consecutive days.

    A run is a maximal sequence of flights whose dates differ by exactly
    one day. Each run is returned as a list of flights ordered by date.
    """
    ordered = sorted(flights, key=lambda flight: flight.date)

    groups = []
    current = []

    for flight in ordered:
        if not current:
            current = [flight]
            continue

        previous = current[-1]
        expected = previous.date + _one_day()
        if flight.date == expected:
            current.append(flight)
        else:
            groups.append(current)
            current = [flight]

    if current:
        groups.append(current)

    return groups


def _one_day():
    from datetime import timedelta

    return timedelta(days=1)


def longest_flight_streak(flights):
    """Return the length of the longest consecutive-day streak.

    Flights on the same day are counted as one day. Returns 0 when there
    are no flights at all.
    """
    groups = group_consecutive_flights(flights)
    return max((len(group) for group in groups), default=0)


def flights_with_gap(flights, gap_days):
    """Return flights whose consecutive-day run is shorter than gap_days.

    Runs of length greater than or equal to gap_days are dropped; the
    remaining flights keep their original relative order.
    """
    ordered = sorted(flights, key=lambda flight: flight.date)
    groups = group_consecutive_flights(ordered)

    result = []
    for group in groups:
        if len(group) < gap_days:
            result.extend(group)

    return result


def remove_short_streaks(flights, min_streak):
    """Drop runs shorter than min_streak, merging the rest.

    Flights that belong to a qualifying run are kept in date order.
    """
    ordered = sorted(flights, key=lambda flight: flight.date)
    groups = group_consecutive_flights(ordered)

    kept = []
    for group in groups:
        if len(group) >= min_streak:
            kept.extend(group)

    return sorted(kept, key=lambda flight: flight.date)
