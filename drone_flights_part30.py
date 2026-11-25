# === Stage 30: Износ батарей ===
# Project: DroneFlights
"""Battery wear estimation module for the DroneFlights flight journal."""


class BatteryWearEstimator:
    """Estimates battery degradation from flight cycles and durations."""

    def __init__(self, cycles_at_full_capacity=500.0,
                 hours_at_full_capacity=500.0):
        self.cycles_at_full_capacity = cycles_at_full_capacity
        self.hours_at_full_capacity = hours_at_full_capacity

    def estimate_cycle_wear(self, completed_cycles):
        """Return the fraction of capacity lost per full charge cycle."""
        if completed_cycles < 0:
            raise ValueError("completed_cycles must be non-negative")
        return min(completed_cycles / self.cycles_at_full_capacity, 1.0)

    def estimate_time_wear(self, total_hours):
        """Return the fraction of capacity lost from calendar time."""
        if total_hours < 0:
            raise ValueError("total_hours must be non-negative")
        return min(total_hours / self.hours_at_full_capacity, 1.0)

    def estimate_remaining_capacity(self, completed_cycles, total_hours):
        """Return the estimated remaining capacity fraction (0.0 to 1.0)."""
        cycle_wear = self.estimate_cycle_wear(completed_cycles)
        time_wear = self.estimate_time_wear(total_hours)
        return max(0.0, 1.0 - cycle_wear - time_wear)


def compute_flight_hours(duration_minutes):
    """Convert a flight duration in minutes to hours."""
    return duration_minutes / 60.0


def estimate_battery_health(flight):
    """Estimate the health of a battery from a flight record.

    Args:
        flight: an object with ``cycles`` and ``duration_minutes`` attributes.

    Returns:
        The estimated remaining capacity fraction (0.0 to 1.0).
    """
    estimator = BatteryWearEstimator()
    hours = compute_flight_hours(flight.duration_minutes)
    return estimator.estimate_remaining_capacity(flight.cycles, hours)


class Battery:
    """A simple battery record used by the flight journal."""

    def __init__(self, identifier, cycles=0, duration_minutes=0.0):
        self.identifier = identifier
        self.cycles = cycles
        self.duration_minutes = duration_minutes

    def health(self, estimator):
        """Return the estimated remaining capacity fraction for this battery."""
        return estimator.estimate_remaining_capacity(
            self.cycles, self.duration_minutes
        )


if __name__ == "__main__":
    demo_battery = Battery("B001", cycles=300, duration_minutes=2400.0)
    estimator = BatteryWearEstimator()
    print("Battery", demo_battery.identifier,
          "remaining capacity:", round(demo_battery.health(estimator) * 100, 1), "%")
