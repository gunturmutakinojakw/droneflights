# === Stage 39: Экспорт в JSON ===
# Project: DroneFlights
"""
droneflights.export_json.py

JSON export utilities for the DroneFlights flight journal.
Standalone module using only the standard library.
"""

import json
from collections import OrderedDict


def _prepare_record(record):
    """Return an ordered, JSON-serialisable representation of a record."""
    ordered = OrderedDict()
    ordered["flight_id"] = record["flight_id"]
    ordered["location"] = record["location"]
    ordered["duration_minutes"] = record["duration_minutes"]
    ordered["altitude_meters"] = record["altitude_meters"]
    ordered["date"] = record["date"]
    ordered["battery"] = record["battery"]
    return ordered


def record_to_json(record):
    """Serialise a single flight record to a JSON string with sorted keys."""
    return json.dumps(_prepare_record(record), indent=4, sort_keys=True)


def records_to_json(records):
    """Serialise a list of flight records to an indented JSON string."""
    ordered = [_prepare_record(r) for r in records]
    ordered.sort(key=lambda r: r["flight_id"])
    return json.dumps(ordered, indent=4, sort_keys=True)
