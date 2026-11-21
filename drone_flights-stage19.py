# === Stage 19: Массовое обновление ===
# Project: DroneFlights
from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

__all__ = ("BatchUpdate", "PreviewResult", "apply_batch_update", "preview_batch_update")


@dataclass
class PreviewResult:
    applied: list
    skipped: list
    changed_fields: dict

    @property
    def total(self) -> int:
        return len(self.applied)


@dataclass
class BatchUpdate:
    predicate: Callable[["Flight"], bool]
    changes: dict
    dry_run: bool = False
    preview: Optional[PreviewResult] = field(default=None, repr=False)

    def matches(self, flight: "Flight") -> bool:
        return self.predicate(flight)

    def target_fields(self) -> list:
        return list(self.changes.keys())


def preview_batch_update(
    flights: Iterable["Flight"],
    batch: BatchUpdate,
) -> PreviewResult:
    applied: list = []
    skipped: list = []
    changed_fields: dict = {}

    for flight in flights:
        if not batch.matches(flight):
            skipped.append(flight)
            continue

        new_values = {
            key: value for key, value in batch.changes.items() if key in flight
        }
        applied.append((flight, new_values))
        for key, value in new_values.items():
            changed_fields.setdefault(key, []).append(value)

    result = PreviewResult(
        applied=[flight for flight, _ in applied],
        skipped=skipped,
        changed_fields=changed_fields,
    )
    batch.preview = result
    return result


def apply_batch_update(
    flights: list,
    batch: BatchUpdate,
) -> PreviewResult:
    if batch.preview is not None:
        raise ValueError("BatchUpdate already has a preview; re-run preview first.")

    result = preview_batch_update(flights, batch)
    if batch.dry_run:
        return result

    for flight, new_values in result.applied:
        for key, value in new_values.items():
            setattr(flight, key, value)

    return result
