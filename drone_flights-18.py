# === Stage 18: Слияние записей ===
# Project: DroneFlights
from datetime import date


def _max_by_key(a, b, key):
    return a if key(a) >= key(b) else b


def _first_non_null(a, b):
    return a if a is not None else b


def _sum_value(a, b):
    return a + b


def merge_flights(first, second):
    """Combine two flight records into a single flight.

    For each field a winner is selected:
      * location  -> first non-empty value
      * duration  -> maximum
      * altitude  -> maximum
      * date      -> latest calendar date

    Any of the arguments may be None; the result is None when both are None.
    """
    if first is None and second is None:
        return None

    location = _first_non_null(first.get("location"), second.get("location"))
    duration = _max_by_key(first.get("duration"), second.get("duration"),
                           key=lambda value: value or 0)
    altitude = _max_by_key(first.get("altitude"), second.get("altitude"),
                           key=lambda value: value or 0)
    date_ = _max_by_key(first.get("date"), second.get("date"),
                        key=lambda value: value or date.min)

    return {
        "location": location,
        "duration": duration,
        "altitude": altitude,
        "date": date_,
    }
