# === Stage 9: Фильтрация записей ===
# Project: DroneFlights
from datetime import date


class FlightDurationFilter:
    """Filter flights by duration value or date range."""

    def __init__(self, min_duration=None, max_duration=None,
                 start_date=None, end_date=None):
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.start_date = start_date
        self.end_date = end_date

    def matches_duration(self, flight):
        if self.min_duration is not None and flight.duration < self.min_duration:
            return False
        if self.max_duration is not None and flight.duration > self.max_duration:
            return False
        return True

    def matches_date_range(self, flight):
        if self.start_date is not None and flight.date < self.start_date:
            return False
        if self.end_date is not None and flight.date > self.end_date:
            return False
        return True

    def matches(self, flight):
        return (self.matches_duration(flight)
                and self.matches_date_range(flight))


def filter_flights(flights, min_duration=None, max_duration=None,
                   start_date=None, end_date=None):
    """Filter a list of flights by duration and/or date range.

    Args:
        flights: iterable of flight records.
        min_duration: minimum flight duration (inclusive).
        max_duration: maximum flight duration (inclusive).
        start_date: earliest allowed date (inclusive).
        end_date: latest allowed date (inclusive).

    Returns:
        A new list containing only the flights matching all criteria.
    """
    if not flights:
        return []

    if min_duration is None and max_duration is None \
            and start_date is None and end_date is None:
        return list(flights)

    duration_min = None
    duration_max = None
    date_start = None
    date_end = None

    if min_duration is not None:
        duration_min = min_duration
    if max_duration is not None:
        duration_max = max_duration
    if start_date is not None:
        date_start = start_date
    if end_date is not None:
        date_end = end_date

    filtered = []
    for flight in flights:
        if duration_min is not None and flight.duration < duration_min:
            continue
        if duration_max is not None and flight.duration > duration_max:
            continue
        if date_start is not None and flight.date < date_start:
            continue
        if date_end is not None and flight.date > date_end:
            continue
        filtered.append(flight)

    return filtered


def filter_flights_by_duration(flights, min_duration=None, max_duration=None):
    """Filter flights by duration value.

    Args:
        flights: iterable of flight records.
        min_duration: minimum flight duration (inclusive).
        max_duration: maximum flight duration (inclusive).

    Returns:
        A new list containing only the flights matching the duration criteria.
    """
    return filter_flights(flights, min_duration=min_duration,
                          max_duration=max_duration)


def filter_flights_by_date_range(flights, start_date=None, end_date=None):
    """Filter flights by date range.

    Args:
        flights: iterable of flight records.
        start_date: earliest allowed date (inclusive).
        end_date: latest allowed date (inclusive).

    Returns:
        A new list containing only the flights matching the date range.
    """
    return filter_flights(flights, start_date=start_date, end_date=end_date)


if __name__ == "__main__":
    sample_flights = [
        {"id": 1, "location": "A", "duration": 25, "date": date(2024, 1, 5)},
        {"id": 2, "location": "B", "duration": 40, "date": date(2024, 1, 10)},
        {"id": 3, "location": "C", "duration": 55, "date": date(2024, 2, 15)},
        {"id": 4, "location": "D", "duration": 30, "date": date(2024, 2, 20)},
    ]

    by_duration = filter_flights_by_duration(
        sample_flights, min_duration=30, max_duration=50)
    print("By duration [30, 50]:")
    for flight in by_duration:
        print(flight)

    by_date = filter_flights_by_date_range(
        sample_flights, start_date=date(2024, 1, 1), end_date=date(2024, 1, 31))
    print("\nBy date range Jan 2024:")
    for flight in by_date:
        print(flight)

    combined = filter_flights(
        sample_flights, min_duration=30,
        start_date=date(2024, 1, 1), end_date=date(2024, 2, 10))
    print("\nCombined duration >= 30 and Jan 2024:")
    for flight in combined:
        print(flight)
