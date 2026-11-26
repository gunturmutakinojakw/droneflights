# === Stage 34: Ключевые метрики ===
# Project: DroneFlights
from datetime import datetime


def format_flight(flight):
    return (
        f"Flight id={flight['id']} "
        f"location={flight['location']} "
        f"duration={flight['duration']} min "
        f"altitude={flight['altitude']} m "
        f"date={flight['date'].strftime('%Y-%m-%d')}"
    )


def compute_flight_stats(flights):
    if not flights:
        return {"count": 0, "total_minutes": 0, "avg_duration": 0.0}

    total_minutes = sum(f["duration"] for f in flights)
    count = len(flights)
    return {
        "count": count,
        "total_minutes": total_minutes,
        "avg_duration": total_minutes / count,
    }


def compute_battery_stats(batteries):
    if not batteries:
        return {"count": 0, "total_capacity": 0, "avg_capacity": 0.0}

    total_capacity = sum(b["capacity"] for b in batteries)
    count = len(batteries)
    return {
        "count": count,
        "total_capacity": total_capacity,
        "avg_capacity": total_capacity / count,
    }


def render_flight_table(flights):
    header = f"{'ID':<5} {'Location':<15} {'Duration':>8} {'Altitude':>9} {'Date':>10}"
    print(header)
    print("-" * len(header))
    for flight in flights:
        print(
            f"{flight['id']:<5} "
            f"{flight['location']:<15} "
            f"{flight['duration']:>8} "
            f"{flight['altitude']:>9} "
            f"{flight['date'].strftime('%Y-%m-%d'):>10}"
        )


def render_summary_block(stats):
    print("=" * 40)
    print("PROJECT SUMMARY")
    print("=" * 40)
    for key, value in stats.items():
        label = key.replace("_", " ").title()
        print(f"  {label:<20}: {value}")
    print("=" * 40)


def print_flight_journal(flights, batteries):
    print_flight_table(flights)
    flight_stats = compute_flight_stats(flights)
    battery_stats = compute_battery_stats(batteries)
    combined_stats = {**flight_stats, **battery_stats}
    render_summary_block(combined_stats)
