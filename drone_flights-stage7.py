# === Stage 7: Связи между сущностями ===
# Project: DroneFlights
"""Stage 7: retrieve all batteries for a given flight and check link integrity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional

from droneflights.flight import Flight


@dataclass(frozen=True)
class Battery:
    """A battery attached to a flight."""

    id: str
    capacity_mah: int
    level_percent: int


@dataclass(frozen=True)
class LinkIntegrity:
    """Result of the integrity check between a flight and its batteries."""

    flight_id: str
    connected_batteries: int
    all_batteries: int
    is_intact: bool


def get_flight_batteries(
    flight: Flight,
    batteries: Iterable[Battery],
) -> List[Battery]:
    """Return every battery whose flight matches the given flight."""

    return [battery for battery in batteries if battery.flight_id == flight.id]


def check_link_integrity(
    flight: Flight,
    batteries: Iterable[Battery],
) -> LinkIntegrity:
    """Check whether the flight-battery link is intact.

    The link is intact when at least one battery is connected and every
    connected battery refers back to the same flight.
    """

    flight_id = flight.id
    connected = get_flight_batteries(flight, batteries)
    connected_ids = {battery.flight_id for battery in connected}
    is_intact = len(connected) > 0 and connected_ids == {flight_id}
    return LinkIntegrity(flight_id, len(connected), len(list(batteries)), is_intact)


def build_flight(
    flight_id: str,
    location: str,
    duration_minutes: int,
    altitude_m: float,
    launch_date: date,
) -> Flight:
    """Build a simple flight record for testing purposes."""

    return Flight(flight_id, location, duration_minutes, altitude_m, launch_date)


def demonstrate() -> None:
    """Run a small self-contained demonstration of the stage."""

    flight = build_flight(
        flight_id="DRN-001",
        location="Hangar A",
        duration_minutes=12,
        altitude_m=80.0,
        launch_date=date(2024, 5, 1),
    )
    batteries = [
        Battery("BAT-1", 5000, 90),
        Battery("BAT-2", 5000, 40),
        Battery("BAT-3", 3000, 100),
    ]
    connected = get_flight_batteries(flight, batteries)
    integrity = check_link_integrity(flight, batteries)
    print(f"Flight: {flight.id}")
    print(f"Connected batteries: {len(connected)}")
    print(f"Integrity intact: {integrity.is_intact}")


if __name__ == "__main__":
    demonstrate()
