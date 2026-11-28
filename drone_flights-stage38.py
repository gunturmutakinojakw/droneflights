# === Stage 38: Сериализация ===
# Project: DroneFlights
from __future__ import annotations

from typing import Any, Dict, Optional


CURRENT_FLIGHT_VERSION = 1
CURRENT_BATTERY_VERSION = 1


def _check_version(version: int, current: int, name: str) -> None:
    if version != current:
        raise ValueError(f"Unsupported {name} format version: {version} (expected {current})")


def serialize_flight(flight: Dict[str, Any], *, version: Optional[int] = None) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "type": "flight",
        "location": flight["location"],
        "duration": flight["duration"],
        "altitude": flight["altitude"],
        "date": flight["date"],
    }
    if version is None:
        version = CURRENT_FLIGHT_VERSION
    _check_version(version, CURRENT_FLIGHT_VERSION, "flight")
    if version < 1:
        data["version"] = version
    return data


def serialize_battery(battery: Dict[str, Any], *, version: Optional[int] = None) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "type": "battery",
        "name": battery["name"],
        "capacity_mah": battery["capacity_mah"],
        "charge_percent": battery["charge_percent"],
    }
    if version is None:
        version = CURRENT_BATTERY_VERSION
    _check_version(version, CURRENT_BATTERY_VERSION, "battery")
    if version < 1:
        data["version"] = version
    return data


def deserialize_flight(data: Dict[str, Any]) -> Dict[str, Any]:
    version = data.get("version", CURRENT_FLIGHT_VERSION)
    _check_version(version, CURRENT_FLIGHT_VERSION, "flight")
    return {
        "location": data["location"],
        "duration": data["duration"],
        "altitude": data["altitude"],
        "date": data["date"],
    }


def deserialize_battery(data: Dict[str, Any]) -> Dict[str, Any]:
    version = data.get("version", CURRENT_BATTERY_VERSION)
    _check_version(version, CURRENT_BATTERY_VERSION, "battery")
    return {
        "name": data["name"],
        "capacity_mah": data["capacity_mah"],
        "charge_percent": data["charge_percent"],
    }
