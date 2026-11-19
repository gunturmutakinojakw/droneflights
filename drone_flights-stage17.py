# === Stage 17: Поиск дубликатов ===
# Project: DroneFlights
from datetime import date


def normalize_date(value):
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return value.strip()
    return str(value)


def normalize_location(value):
    if value is None:
        return None
    text = str(value).strip().lower()
    replacements = {
        "drone park": "dronepark",
        "dronepark": "dronepark",
        "test field": "testfield",
        "testfield": "testfield",
        "training ground": "trainingground",
        "trainingground": "trainingground",
        "rooftop": "rooftop",
    }
    for original, replacement in replacements.items():
        if original in text:
            text = text.replace(original, replacement)
    return text


def normalize_duration(value):
    if isinstance(value, (int, float)):
        return round(float(value))
    if isinstance(value, str):
        text = value.strip().lower()
        for unit in ("min", "minute", "minutes"):
            if unit in text:
                number = text.split()[0]
                return round(float(number))
        return round(float(text))
    return 0


def normalize_altitude(value):
    if isinstance(value, (int, float)):
        return round(float(value))
    if isinstance(value, str):
        text = value.strip().lower()
        for unit in ("m", "meter", "meters"):
            if unit in text:
                number = text.split()[0]
                return round(float(number))
        return round(float(text))
    return 0


def normalize_flight(flight):
    keys = {
        "location": normalize_location,
        "duration": normalize_duration,
        "altitude": normalize_altitude,
        "date": normalize_date,
    }
    normalized = {}
    for key, function in keys.items():
        if key in flight:
            normalized[key] = function(flight[key])
    return normalized


def find_duplicate_flights(flights):
    if not flights:
        return []
    groups = {}
    for flight in flights:
        signature = normalize_flight(flight)
        groups.setdefault(signature, []).append(flight)
    duplicates = []
    for signature, group in groups.items():
        if len(group) > 1:
            duplicates.extend(group)
    return duplicates


def remove_duplicate_flights(flights):
    seen = set()
    unique = []
    for flight in flights:
        signature = normalize_flight(flight)
        if signature not in seen:
            seen.add(signature)
            unique.append(flight)
    return unique
