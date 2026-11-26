# === Stage 31: Прогноз сроков ===
# Project: DroneFlights
from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass
class FlightForecast:
    """Nearest-term forecast derived from previous flight intervals."""

    flight_id: str
    previous_intervals: list[float]
    horizon_days: float = 1.0

    def expected_next_interval(self) -> float:
        """Return the mean of the previous intervals as the expected value."""
        if not self.previous_intervals:
            return 0.0
        return mean(self.previous_intervals)

    def forecast_date(self, base_date: datetime.date) -> datetime.date:
        """Return the predicted date of the next flight."""
        from datetime import timedelta

        return base_date + timedelta(days=self.expected_next_interval())

    def confidence(self) -> float:
        """Return a simple coefficient of variation of the intervals."""
        if not self.previous_intervals:
            return 1.0
        avg = mean(self.previous_intervals)
        if avg <= 0:
            return 1.0
        variance = sum((i - avg) ** 2 for i in self.previous_intervals) / len(self.previous_intervals)
        return variance ** 0.5 / avg


def build_flight_forecast(
    flight_id: str,
    previous_intervals: list[float],
    horizon_days: float = 1.0,
) -> FlightForecast:
    """Construct a forecast object from a flight id and prior intervals."""
    return FlightForecast(
        flight_id=flight_id,
        previous_intervals=previous_intervals,
        horizon_days=horizon_days,
    )
