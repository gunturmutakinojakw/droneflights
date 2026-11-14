# === Stage 2: Проверка полей ===
# Project: DroneFlights
from datetime import datetime


def normalize_flight_inputs(location, duration, height, date_str):
    location = (location or "").strip()
    duration = float(duration)
    height = float(height)
    date = _parse_date(date_str)
    return location, duration, height, date


def _parse_date(value):
    value = (value or "").strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d.%m.%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError("Date must be in YYYY-MM-DD format")


def validate_flight(flight):
    location, duration, height, date = flight
    errors = []
    if not location:
        errors.append("Flight location cannot be empty")
    if location and len(location) > 128:
        errors.append("Flight location is too long (max 128 characters)")
    if duration <= 0:
        errors.append("Flight duration must be greater than zero")
    if duration > 12 * 60:
        errors.append("Flight duration cannot exceed 12 hours")
    if height <= 0:
        errors.append("Flight height must be greater than zero")
    if height > 5000:
        errors.append("Flight height cannot exceed 5000 meters")
    if not isinstance(date, datetime.date):
        errors.append("Flight date is invalid")
    return errors
