# === Stage 35: Взвешенный рейтинг ===
# Project: DroneFlights
import statistics
from dataclasses import dataclass


@dataclass(frozen=True)
class FlightScore:
    value: float
    max_value: float
    components: dict


WEIGHTS = {
    "distance": 0.35,
    "altitude": 0.30,
    "duration": 0.35,
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _score_distance(distance_km: float) -> float:
    return clamp(distance_km / 20.0, 0.0, 1.0)


def _score_altitude(altitude_m: float) -> float:
    return clamp(altitude_m / 120.0, 0.0, 1.0)


def _score_duration(minutes: float) -> float:
    return clamp(minutes / 30.0, 0.0, 1.0)


def score_flight(distance_km: float, altitude_m: float, duration_minutes: float, weights: dict | None = None) -> FlightScore:
    weights = weights or WEIGHTS
    raw = {
        "distance": _score_distance(distance_km),
        "altitude": _score_altitude(altitude_m),
        "duration": _score_duration(duration_minutes),
    }
    weighted_sum = sum(weights[name] * raw[name] for name in weights)
    total_weight = sum(weights.values())
    normalized = weighted_sum / total_weight if total_weight else 0.0
    return FlightScore(value=normalized, max_value=1.0, components=dict(raw))


def rank_flights(flights: list[tuple[str, float, float, float]], weights: dict | None = None) -> list[tuple[str, FlightScore]]:
    scored = [(name, score_flight(*flight, weights=weights)) for name, flight in flights]
    scored.sort(key=lambda pair: pair[1].value, reverse=True)
    return scored


def average_component(component: str, flights: list[tuple[str, float, float, float]], weights: dict | None = None) -> float:
    scores = [score for _, score in rank_flights(flights, weights=weights)]
    return statistics.mean([s.components[component] for s in scores]) if scores else 0.0


if __name__ == "__main__":
    sample = [
        ("flight-001", 15.0, 90.0, 25.0),
        ("flight-002", 30.0, 100.0, 40.0),
        ("flight-003", 5.0, 60.0, 10.0),
    ]
    results = rank_flights(sample)
    for name, score in results:
        print(f"{name}: {score.value:.3f} -> {score.components}")
