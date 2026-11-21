# === Stage 20: Избранное ===
# Project: DroneFlights
from datetime import date
from typing import List, Optional


class Flight:
    def __init__(self, location: str, duration: int, altitude: int, flight_date: date):
        self.location = location
        self.duration = duration
        self.altitude = altitude
        self.flight_date = flight_date
        self.is_favorite = False

    def toggle_favorite(self) -> None:
        self.is_favorite = not self.is_favorite

    def mark_favorite(self) -> None:
        self.is_favorite = True

    def unmark_favorite(self) -> None:
        self.is_favorite = False


class FlightJournal:
    def __init__(self):
        self.flights: List[Flight] = []

    def add_flight(self, flight: Flight) -> None:
        self.flights.append(flight)

    def get_favorite_flights(self) -> List[Flight]:
        return [flight for flight in self.flights if flight.is_favorite]

    def count_favorite_flights(self) -> int:
        return len(self.get_favorite_flights())
