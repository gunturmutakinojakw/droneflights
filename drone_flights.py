# === Stage 1: Каркас модуля ===
# Project: DroneFlights
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


@dataclass
class Flight:
    location: str
    duration_minutes: int
    altitude_meters: int
    date: date


def make_demo_flights() -> List[Flight]:
    today = date.today()
    return [
        Flight(
            location="Central Park",
            duration_minutes=18,
            altitude_meters=90,
            date=today,
        ),
        Flight(
            location="Riverside",
            duration_minutes=45,
            altitude_meters=120,
            date=today + timedelta(days=1),
        ),
        Flight(
            location="Hilltop",
            duration_minutes=30,
            altitude_meters=60,
            date=today + timedelta(days=2),
        ),
    ]


def main() -> None:
    flights = make_demo_flights()
    print("DroneFlights - Flight Log")
    print("=" * 30)
    for flight in flights:
        print(f"{flight.location} | {flight.duration_minutes} min | "
              f"{flight.altitude_meters} m | {flight.date}")
    print(f"Total flights: {len(flights)}")


if __name__ == "__main__":
    main()
