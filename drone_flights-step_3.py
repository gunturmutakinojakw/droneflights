# === Stage 3: Хранилище в памяти ===
# Project: DroneFlights
from datetime import datetime


class Flight:
    """In-memory record of a drone flight."""

    def __init__(self, flight_id, location, duration_minutes, altitude_m, date):
        self.flight_id = flight_id
        self.location = location
        self.duration_minutes = duration_minutes
        self.altitude_m = altitude_m
        self.date = date

    def __repr__(self):
        return (
            f"Flight(id={self.flight_id!r}, location={self.location!r}, "
            f"duration={self.duration_minutes}m, altitude={self.altitude_m}m, "
            f"date={self.date!r})"
        )


class FlightStore:
    """Simple memory-backed store for Flight records."""

    def __init__(self):
        self._flights = {}

    def add(self, flight):
        """Insert or replace a flight by its identifier."""
        self._flights[flight.flight_id] = flight
        return flight

    def get(self, flight_id):
        """Return the flight with the given identifier or None."""
        return self._flights.get(flight_id)

    def list_all(self):
        """Return all stored flights ordered by their identifier."""
        return [self._flights[key] for key in sorted(self._flights)]

    def __len__(self):
        return len(self._flights)
