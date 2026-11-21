# === Stage 21: Статусы записей ===
# Project: DroneFlights
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum, auto
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Flight:
    """A single drone flight with its lifecycle status."""

    place: str
    duration: int  # minutes
    altitude: int  # meters
    date: date
    status: "FlightStatus" = FlightStatus.PLANED

    def __post_init__(self) -> None:
        if self.duration < 0:
            raise ValueError("duration must be non-negative")
        if self.altitude < 0:
            raise ValueError("altitude must be non-negative")
        if not isinstance(self.place, str) or not self.place.strip():
            raise ValueError("place must be a non-empty string")


class FlightStatus(str, Enum):
    """Lifecycle stages of a drone flight."""

    PLANED = auto()
    SCHEDULED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()

    def __str__(self) -> str:
        return self.name.lower()


TRANSITIONS: Dict[FlightStatus, Tuple[FlightStatus, ...]] = {
    FlightStatus.PLANED: (FlightStatus.SCHEDULED, FlightStatus.CANCELLED),
    FlightStatus.SCHEDULED: (FlightStatus.IN_PROGRESS, FlightStatus.CANCELLED),
    FlightStatus.IN_PROGRESS: (FlightStatus.COMPLETED, FlightStatus.CANCELLED),
    FlightStatus.COMPLETED: (),
    FlightStatus.CANCELLED: (),
}


def can_transition(current: FlightStatus, target: FlightStatus) -> bool:
    """Return True if moving from current to target is allowed."""
    return target in TRANSITIONS.get(current, ())


def all_statuses() -> List[FlightStatus]:
    """Return every lifecycle status in definition order."""
    return list(FlightStatus)


def valid_targets(status: FlightStatus) -> List[FlightStatus]:
    """Return the statuses reachable from the given status."""
    return list(TRANSITIONS.get(status, ()))


def status_flow() -> str:
    """Render the transition table as a readable text diagram."""
    lines: List[str] = []
    for status in FlightStatus:
        targets = TRANSITIONS.get(status, ())
        if targets:
            arrows = " -> ".join(
                f"{status.name} -> {t.name}" for t in targets
            )
            lines.append(f"{arrows}")
        else:
            lines.append(f"{status.name} (terminal)")
    return "\n".join(lines)


def flight_status_path(start: FlightStatus, goal: FlightStatus) -> List[FlightStatus]:
    """Return a shortest path from start to goal, or None if unreachable."""
    from collections import deque

    if start == goal:
        return [start]
    visited: set[FlightStatus] = {start}
    queue: deque[Tuple[FlightStatus, List[FlightStatus]]] = deque([(start, [start])])
    while queue:
        current, path = queue.popleft()
        for nxt in TRANSITIONS.get(current, ()):
            if nxt == goal:
                return path + [nxt]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None
