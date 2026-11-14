# === Stage 5: Удаление и восстановление ===
# Project: DroneFlights
"""Module: flights_deletion

Adds delete and soft-delete (recoverable) behaviour for flights.
"""

from datetime import datetime


class Flight:
    """A drone flight record."""

    def __init__(self, location, duration, altitude, date):
        self.location = location
        self.duration = duration
        self.altitude = altitude
        self.date = date
        self.deleted = False
        self.deleted_at = None
        self.soft_deleted = False

    def soft_delete(self):
        """Flag the flight as soft-deleted but keep the record."""
        self.soft_deleted = True
        self.deleted_at = datetime.now()

    def hard_delete(self):
        """Remove the flight entirely."""
        self.deleted = True
        self.deleted_at = datetime.now()
        self.soft_deleted = False

    def recover(self):
        """Restore a previously soft-deleted flight."""
        if self.soft_deleted:
            self.soft_deleted = False
            self.deleted_at = None

    def is_active(self):
        """Return True if the flight is available in the journal."""
        return not self.deleted and not self.soft_deleted


class FlightJournal:
    """Stores flights and supports soft-delete and hard-delete."""

    def __init__(self):
        self._flights = []

    def add_flight(self, flight):
        self._flights.append(flight)

    def find_flight(self, location, date):
        for flight in self._flights:
            if flight.location == location and flight.date == date:
                return flight
        return None

    def soft_delete_flight(self, flight):
        """Soft-delete a flight so it can be recovered later."""
        flight.soft_delete()

    def recover_flight(self, flight):
        """Restore a soft-deleted flight."""
        flight.recover()

    def hard_delete_flight(self, flight):
        """Permanently remove a flight from the journal."""
        flight.hard_delete()

    def active_flights(self):
        """Return only the flights that are currently active."""
        return [f for f in self._flights if f.is_active()]

    def all_flights(self):
        """Return every stored flight, including soft-deleted ones."""
        return list(self._flights)


if __name__ == "__main__":
    journal = FlightJournal()
    flight = Flight("park", 12, 50, "2025-01-01")
    journal.add_flight(flight)
    journal.soft_delete_flight(flight)
    print("active:", journal.active_flights())
    journal.recover_flight(flight)
    print("active:", journal.active_flights())
    journal.hard_delete_flight(flight)
    print("active:", journal.active_flights())
