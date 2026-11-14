# === Stage 6: Связанная сущность ===
# Project: DroneFlights
"""Battery entity for DroneFlights flight log module."""

from datetime import datetime


class Battery:
    """Represents a drone battery with capacity and charge level."""

    def __init__(self, capacity_mah, charge_percent):
        self.id = None
        self.capacity_mah = capacity_mah
        self.charge_percent = charge_percent

    def set_id(self, battery_id):
        """Assign an identifier to the battery."""
        self.id = battery_id

    def update_charge(self, charge_percent):
        """Update the current charge level, clamped to valid range."""
        if not 0 <= charge_percent <= 100:
            raise ValueError("charge_percent must be between 0 and 100")
        self.charge_percent = charge_percent

    def remaining_capacity(self):
        """Return the remaining capacity in milliampere-hours."""
        return round(self.capacity_mah * self.charge_percent / 100.0, 2)

    def is_low(self, threshold=20):
        """Return True if the charge level is at or below the threshold."""
        return self.charge_percent <= threshold

    def __repr__(self):
        return (
            f"Battery(id={self.id}, capacity_mah={self.capacity_mah}, "
            f"charge_percent={self.charge_percent})"
        )


def create_battery(battery_id, capacity_mah, charge_percent):
    """Create and register a new battery with the given identifier."""
    battery = Battery(capacity_mah, charge_percent)
    battery.set_id(battery_id)
    return battery


def create_battery_from_flight(flight, capacity_mah, charge_percent):
    """Create a battery linked to an existing flight by flight identifier."""
    battery = Battery(capacity_mah, charge_percent)
    battery.set_id(f"{flight.id}-battery")
    return battery
