# === Stage 8: Генерация идентификаторов ===
# Project: DroneFlights
import string


PROJECT_PREFIX = "DF"


def generate_id():
    """Generate a unique identifier with the project prefix and collision check."""
    while True:
        unique = f"{PROJECT_PREFIX}-{string.ascii_lowercase}{string.digits}"
        if unique not in FLIGHTS:
            return unique


FLIGHTS = {}


def add_flight(location, duration, altitude, date):
    flight_id = generate_id()
    FLIGHTS[flight_id] = {
        "id": flight_id,
        "location": location,
        "duration": duration,
        "altitude": altitude,
        "date": date,
    }
    return flight_id


if __name__ == "__main__":
    print(add_flight("Beach", 30, 50, "2025-01-01"))
    print(add_flight("Park", 45, 80, "2025-01-02"))
    print(add_flight("Lake", 20, 30, "2025-01-03"))
