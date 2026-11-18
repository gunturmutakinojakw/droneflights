# === Stage 15: Постраничный вывод ===
# Project: DroneFlights
from typing import List, Tuple


class PaginationError(ValueError):
    """Raised when pagination parameters are invalid."""


def validate_page_params(page: int, page_size: int) -> Tuple[int, int]:
    """Return a validated (page, page_size) pair.

    Both values must be positive integers; page_size has no upper bound
    for this module, but must be at least 1.
    """
    if not isinstance(page, int) or isinstance(page, bool):
        raise PaginationError("page must be an integer")
    if not isinstance(page_size, int) or isinstance(page_size, bool):
        raise PaginationError("page_size must be an integer")
    if page < 1:
        raise PaginationError("page must be >= 1")
    if page_size < 1:
        raise PaginationError("page_size must be >= 1")
    return page, page_size


def paginate_flights(flights: List[dict], page: int, page_size: int) -> List[dict]:
    """Return the slice of flights for the requested page.

    Each flight is expected to be a mapping with at least a 'flight_id'
    key. Missing entries are filled with sensible defaults so the caller
    never has to guard against absent fields.
    """
    page, page_size = validate_page_params(page, page_size)
    total = len(flights)
    start = (page - 1) * page_size
    end = start + page_size
    if start >= total:
        return []
    sliced = flights[start:end]
    for flight in sliced:
        flight.setdefault("flight_id", None)
        flight.setdefault("location", None)
        flight.setdefault("duration_minutes", None)
        flight.setdefault("altitude_m", None)
        flight.setdefault("flight_date", None)
    return sliced


def page_metadata(total: int, page: int, page_size: int) -> dict:
    """Build a small metadata block describing the pagination state."""
    page, page_size = validate_page_params(page, page_size)
    total_pages = (total + page_size - 1) // page_size
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
