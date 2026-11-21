# === Stage 22: История изменений ===
# Project: DroneFlights
from datetime import datetime


class FlightChange:
    """A single recorded modification of a flight."""

    def __init__(self, changed_at, field, old_value, new_value):
        self.changed_at = changed_at
        self.field = field
        self.old_value = old_value
        self.new_value = new_value

    def to_dict(self):
        return {
            "changed_at": self.changed_at.isoformat() if isinstance(self.changed_at, datetime) else self.changed_at,
            "field": self.field,
            "old_value": self.old_value,
            "new_value": self.new_value,
        }

    def __repr__(self):
        return (
            f"FlightChange(field={self.field!r}, old={self.old_value!r}, "
            f"new={self.new_value!r}, changed_at={self.changed_at.isoformat() if isinstance(self.changed_at, datetime) else self.changed_at})"
        )


class FlightHistory:
    """Stores the change log for a single flight."""

    def __init__(self):
        self.changes = []

    def add(self, field, old_value, new_value, changed_at=None):
        if changed_at is None:
            changed_at = datetime.now()
        self.changes.append(
            FlightChange(changed_at, field, old_value, new_value)
        )

    def log(self, field, old_value, new_value):
        self.add(field, old_value, new_value)
        return self.changes[-1]

    def get_changes(self):
        return list(self.changes)

    def get_changes_for_field(self, field):
        return [c for c in self.changes if c.field == field]

    def get_history(self):
        return [c.to_dict() for c in self.changes]

    def undo_last(self, field):
        for change in reversed(self.changes):
            if change.field == field:
                return change.new_value
        return None

    def __len__(self):
        return len(self.changes)

    def __repr__(self):
        return f"FlightHistory(changes={len(self.changes)})"
