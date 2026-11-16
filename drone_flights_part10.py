# === Stage 10: Сортировка записей ===
# Project: DroneFlights
from datetime import datetime


def parse_flight_record(raw):
    """Build a flight record dict from a CSV-like line."""
    parts = raw.split(";")
    location = parts[0]
    duration = int(parts[1])
    altitude = float(parts[2])
    created = datetime.strptime(parts[3], "%Y-%m-%d %H:%M:%S")
    return {
        "location": location,
        "duration": duration,
        "altitude": altitude,
        "created": created,
    }


def sort_key_flight(record, reverse=False):
    """Return a tuple used to sort flight records.

    Primary key: location (case-insensitive, space-normalized).
    Secondary key: creation timestamp.
    ``reverse`` toggles ascending/descending order for both keys.
    """
    normalized_location = " ".join(record["location"].lower().split())
    return (normalized_location, record["created"]), reverse


def sort_flights(flights, reverse=False):
    """Sort a list of flight records.

    Each record is sorted by its location first and then by the
    creation timestamp.  ``reverse=True`` produces descending order,
    otherwise ascending.  The original list is left untouched.
    """
    if not flights:
        return []
    decorated = [(sort_key_flight(record, reverse), record) for record in flights]
    decorated.sort(key=lambda item: item[0], reverse=reverse)
    return [record for _, record in decorated]


def main():
    sample = [
        "Forest Park;45;120.5;2024-03-01 09:10:00",
        "City Center;10;80.0;2024-02-28 14:20:00",
        "Forest park;30;95.0;2024-03-02 08:05:00",
        "Beach;60;150.0;2024-03-01 11:30:00",
    ]
    flights = [parse_flight_record(line) for line in sample]
    ordered = sort_flights(flights, reverse=True)
    for record in ordered:
        print(record["location"], record["duration"], record["altitude"])


if __name__ == "__main__":
    main()
