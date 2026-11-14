# === Stage 4: Редактирование записей ===
# Project: DroneFlights
ALLOWED_FLIGHT_FIELDS = {"location", "duration", "altitude", "date"}


def can_update_flight(flight, proposed_changes):
    if not isinstance(flight, dict):
        return False
    if not isinstance(proposed_changes, dict):
        return False
    allowed = proposed_changes.keys() & ALLOWED_FLIGHT_FIELDS
    for key in allowed:
        if flight.get(key) is None:
            return False
    return True


def update_flight(flight, proposed_changes):
    if not can_update_flight(flight, proposed_changes):
        return flight, False
    updated = dict(flight)
    for key in proposed_changes:
        if key in ALLOWED_FLIGHT_FIELDS:
            updated[key] = proposed_changes[key]
    return updated, True


def apply_flight_updates(flights, flight_id, proposed_changes):
    flights = list(flights)
    for index, flight in enumerate(flights):
        if flight.get("id") == flight_id:
            updated, ok = update_flight(flight, proposed_changes)
            flights[index] = updated
            return flights, ok
    return flights, False
