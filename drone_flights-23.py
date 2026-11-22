# === Stage 23: Просмотр истории ===
# Project: DroneFlights
from datetime import datetime

# Compact flight history viewer: renders a single flight record concisely.

# Format a flight date as YYYY-MM-DD for compact display.
def format_flight_date(date_value):
    if date_value is None:
        return "unknown"
    try:
        parsed = datetime.fromisoformat(date_value)
        return parsed.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return str(date_value)


# Format a flight record into a single compact line of text.
def render_flight_line(flight):
    if flight is None:
        return "no flight"
    location = flight.get("location", "unknown")
    duration = flight.get("duration", 0)
    height = flight.get("height", 0)
    date = format_flight_date(flight.get("date"))
    return f"FLIGHT {location} | {duration} min | {height} m | {date}"


# Build a compact history view for one flight record.
def show_flight_history(flight):
    line = render_flight_line(flight)
    return f"History:\n{line}"


if __name__ == "__main__":
    sample = {
        "location": "Central Park",
        "duration": 12,
        "height": 45,
        "date": "2024-05-17",
    }
    print(show_flight_history(sample))
