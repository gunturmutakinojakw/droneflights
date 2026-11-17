# === Stage 12: Поиск по нескольким словам ===
# Project: DroneFlights
"""Stage 12 of 88 for DroneFlights: multi-word flight search with negation.

This module provides a self-contained search utility that finds flights matching
multiple required terms, while excluding flights that contain terms prefixed with
a hyphen. It works on flight descriptions and uses only the standard library.
"""

import re
from typing import Iterable, List, Optional, Sequence, TypeVar

__all__ = ["FlightSearch", "build_search_terms", "parse_terms"]

T = TypeVar("T")


def build_search_terms(terms: Sequence[str]) -> List[str]:
    """Split each term into individual words, dropping empty tokens.

    The returned list contains only the words that should participate in the
    search; it never contains empty strings.
    """

    tokens: List[str] = []
    for term in terms:
        if term is None:
            continue
        for piece in re.split(r"\s+", term.strip()):
            if piece:
                tokens.append(piece)
    return tokens


def parse_terms(terms: Sequence[str]) -> Tuple[List[str], List[str]]:
    """Separate required words from negated words.

    A word prefixed with a leading hyphen is treated as a negation term: flights
    containing it must be excluded. Everything else is a required term.
    """

    required: List[str] = []
    negated: List[str] = []
    for term in build_search_terms(terms):
        if term.startswith("-"):
            negated.append(term[1:].strip())
        else:
            required.append(term)
    return required, negated


def _words_in_text(text: str) -> set:
    """Return the set of lowercase words found in a piece of text."""

    return set(re.findall(r"[a-z0-9_]+", text.lower()))


class FlightSearch:
    """Search flights by multiple required words with optional negation."""

    def __init__(self, flights: Iterable[T], terms: Sequence[str]) -> None:
        self.required, self.negated = parse_terms(terms)
        self.flights = list(flights)

    def matches(self, description: str) -> bool:
        """Return True if the description satisfies all search conditions."""

        words = _words_in_text(description)
        if not self.required:
            return True
        for word in self.required:
            if word not in words:
                return False
        for word in self.negated:
            if word in words:
                return False
        return True

    def search(self) -> List[T]:
        """Return flights that match the query, preserving input order."""

        return [flight for flight in self.flights if self.matches(flight.description)]

    def count(self) -> int:
        """Return the number of flights matching the query."""

        return len(self.search())
