# === Stage 13: Теги ===
# Project: DroneFlights
from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class Flight:
    location: str
    duration_minutes: int
    altitude_meters: int
    date: str
    tags: Set[str] = field(default_factory=set)


class FlightTagStore:
    def __init__(self) -> None:
        self._flights: Dict[str, Flight] = {}
        self._tags: Dict[str, Set[str]] = {}
        self._by_flight: Dict[str, Set[str]] = {}

    def add_flight(self, flight: Flight) -> None:
        self._flights[flight.location] = flight
        for tag in flight.tags:
            self._tags.setdefault(tag, set()).add(flight.location)
            self._by_flight.setdefault(flight.location, set()).add(tag)

    def remove_flight(self, location: str) -> None:
        flight = self._flights.pop(location, None)
        if flight is None:
            return
        for tag in flight.tags:
            self._tags.get(tag, set()).discard(location)
            self._by_flight.get(location, set()).discard(tag)
            if not self._tags[tag]:
                del self._tags[tag]
            if not self._by_flight[location]:
                del self._by_flight[location]

    def add_tag(self, location: str, tag: str) -> None:
        if location not in self._flights:
            raise KeyError(location)
        if tag in self._by_flight[location]:
            return
        self._by_flight[location].add(tag)
        self._tags.setdefault(tag, set()).add(location)

    def remove_tag(self, location: str, tag: str) -> bool:
        if tag not in self._by_flight[location]:
            return False
        self._by_flight[location].discard(tag)
        self._tags[tag].discard(location)
        if not self._by_flight[location]:
            del self._by_flight[location]
        if not self._tags[tag]:
            del self._tags[tag]
        return True

    def tags_for_flight(self, location: str) -> Set[str]:
        return set(self._by_flight.get(location, set()))

    def flights_by_tag(self, tag: str) -> List[Flight]:
        locations = sorted(self._tags.get(tag, set()))
        return [self._flights[loc] for loc in locations if loc in self._flights]

    def search_by_tag(self, tag: str) -> List[Flight]:
        return self.flights_by_tag(tag)

    def has_tag(self, location: str, tag: str) -> bool:
        return tag in self._by_flight.get(location, set())
