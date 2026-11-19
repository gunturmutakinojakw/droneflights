# === Stage 16: Быстрые фильтры ===
# Project: DroneFlights
"""drone_flights.filters - fast filters for flight records.

This module provides helpers to quickly filter flight records by
temporal semantics: today, this week, and overdue (past-due) flights.
It operates on plain data structures and depends only on the standard library.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta


def parse_flight_date(value) -> date | None:
    """Return a :class:`datetime.date` from a variety of common inputs.

    Accepts ``date``, ``datetime``, ISO strings (``YYYY-MM-DD`` or
    ``YYYY-MM-DDTHH:MM:SS``), or ``None``.  Returns ``None`` for inputs
    that cannot be interpreted as a date.
    """

    if value is None:
        return None

    if isinstance(value, date) and not isinstance(value, datetime):
        return value

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if "t" in text.lower():
            try:
                return datetime.fromisoformat(text).date()
            except ValueError:
                return None
        try:
            return date.fromisoformat(text)
        except ValueError:
            return None

    return None


def flights_today(flights) -> list:
    """Return flight records whose date is today (inclusive)."""

    today = date.today()
    return [flight for flight in flights if _flight_date(flight) == today]


def flights_this_week(flights, now=None) -> list:
    """Return flight records whose date falls in the current week.

    The week starts on Monday and ends on Sunday.  ``now`` defaults to
    the current date; only the date component is used.
    """

    if now is None:
        now = date.today()
    start = now - timedelta(days=now.weekday())
    end = start + timedelta(days=6)
    return [
        flight for flight in flights
        if start <= _flight_date(flight) <= end
    ]


def overdue_flights(flights, threshold: timedelta = timedelta(days=1)) -> list:
    """Return flight records scheduled before the deadline.

    A flight is considered overdue when its scheduled date is earlier
    than ``now - threshold``.  The ``threshold`` represents the grace
    period after which a flight becomes overdue (defaults to one day).
    """

    if threshold is None:
        threshold = timedelta(days=1)
    now = date.today()
    deadline = now - threshold
    return [
        flight for flight in flights
        if _flight_date(flight) < deadline
    ]


def _flight_date(flight) -> date | None:
    """Extract a date from a flight record.

    Supports records that expose ``flight.date`` or ``flight["date"]``.
    Returns ``None`` if no date information is available.
    """

    if flight is None:
        return None
    if hasattr(flight, "date"):
        return parse_flight_date(flight.date)
    if isinstance(flight, dict):
        return parse_flight_date(flight.get("date"))
    return None
