# === Stage 24: Недельный отчёт ===
# Project: DroneFlights
from datetime import date, timedelta


def build_week_report(flights, batteries):
    """Return a week report dict for flights and batteries."""
    if not flights:
        return {"week": None, "rows": []}

    start = min(f["date"] for f in flights)
    end = start + timedelta(days=6)

    rows = []
    for f in flights:
        if f["date"] < start or f["date"] > end:
            continue
        battery_id = f.get("battery_id")
        batt = next((b for b in batteries if b["id"] == battery_id), None)
        rows.append({
            "date": f["date"],
            "place": f["place"],
            "duration": f["duration"],
            "height": f["height"],
            "battery": batt["id"] if batt else "-",
            "energy": batt["energy"] if batt else "-",
        })

    rows.sort(key=lambda r: (r["date"], r["place"]))

    headers = ["Date", "Place", "Duration(h)", "Height(m)", "Battery", "Energy(Wh)"]
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    table = ["".join(str(headers[i]).ljust(widths[i]) for i in range(len(headers)))]
    table.append("".join("-" * widths[i] for i in range(len(headers))))
    for row in rows:
        line = "".join(str(row[i]).ljust(widths[i]) for i in range(len(headers)))
        table.append(line)

    total_flights = len(rows)
    total_hours = round(sum(r["duration"] for r in rows), 2)
    total_energy = round(sum(r["energy"] for r in rows), 2)

    return {
        "week": (start, end),
        "rows": rows,
        "total_flights": total_flights,
        "total_hours": total_hours,
        "total_energy": total_energy,
    }


def format_week_report(report):
    """Return a text representation of the week report."""
    start, end = report["week"]
    lines = [
        "Week report",
        "From: " + str(start),
        "To: " + str(end),
        "",
    ]
    lines.append("Flights: {}".format(report["total_flights"]))
    lines.append("Total hours: {}".format(report["total_hours"]))
    lines.append("Total energy: {} Wh".format(report["total_energy"]))
    lines.append("")
    lines.append("Date        Place              Duration Height Battery Energy")
    for row in report["rows"]:
        lines.append(
            "{:<10} {:<18} {:<7} {:<6} {:<8} {}".format(
                str(row["date"]),
                row["place"],
                row["duration"],
                row["height"],
                row["battery"],
                row["energy"],
            )
        )
    return "\n".join(lines)
