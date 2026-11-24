# === Stage 28: Топ записей ===
# Project: DroneFlights
"""Top-N flight records module for DroneFlights."""


def top_n_flights(records, key, n):
    """Return the top n records sorted by the given key in descending order.

    Args:
        records: iterable of flight records (dicts or objects).
        key: name of the attribute to rank by.
        n: number of records to return.

    Returns:
        A new list containing up to n records with the highest key values.
    """
    if n is None or n <= 0:
        return []

    def _getter(record):
        return getattr(record, key)

    return sorted(records, key=_getter, reverse=True)[:n]


if __name__ == "__main__":
    flights = [
        {"flight_id": "A1", "location": "North", "duration": 120, "height": 50},
        {"flight_id": "B2", "location": "South", "duration": 300, "height": 120},
        {"flight_id": "C3", "location": "East", "duration": 180, "height": 80},
        {"flight_id": "D4", "location": "West", "duration": 90, "height": 40},
        {"flight_id": "E5", "location": "Center", "duration": 240, "height": 100},
    ]

    print("Top 3 flights by duration:")
    for record in top_n_flights(flights, "duration", 3):
        print(record)

    print("\nTop 2 flights by height:")
    for record in top_n_flights(flights, "height", 2):
        print(record)
