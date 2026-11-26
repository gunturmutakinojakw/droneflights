# === Stage 33: Календарная сетка ===
# Project: DroneFlights
import calendar
from datetime import date


class BatteryCalendar:
    """Renders a battery's monthly charge states as a text grid."""

    def __init__(self, battery_id, charges):
        self.battery_id = battery_id
        self.charges = charges

    def _state_for(self, day):
        for entry in self.charges:
            if entry.day == day:
                return entry.state
        return "?"

    def render(self, month, year):
        header = "{title} {battery} {year}".format(
            title=calendar.month_name[month],
            battery=self.battery_id,
            year=year,
        )
        first = date(year, month, 1)
        last = date(year, month, calendar.monthrange(year, month)[1])
        start = first - date(year, month, 1 - first.weekday())
        grid = calendar.monthgrid(start, last)
        rows = ["{header:30}".format(header=header)]
        for week in grid:
            cells = []
            for day in week:
                day = day or date(year, month, -1)
                cells.append("{:2}:{}".format(day.day, self._state_for(day)))
            rows.append("".join(cells))
        return "\n".join(rows)


class ChargeEntry:
    """A single daily charge reading for a battery."""

    def __init__(self, day, state):
        self.day = day
        self.state = state
