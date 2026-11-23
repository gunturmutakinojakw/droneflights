# === Stage 26: Аномальные значения ===
# Project: DroneFlights
"""Anomaly detection for numeric flight fields using a simple statistical method.

This module provides a small, self-contained helper to flag outlier values
in numeric flight fields (duration, altitude, ...) based on the mean and
standard deviation of the available samples. It relies only on the Python
standard library and does not import anything from the rest of the project.
"""

import statistics


def _collect_values(field_values):
    """Return the list of finite numeric values contained in the samples."""
    collected = []
    for value in field_values:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if number != number:  # skip NaN
            continue
        collected.append(number)
    return collected


def _mean(values):
    if not values:
        return 0.0
    return statistics.fmean(values)


def _standard_deviation(values):
    return statistics.pstdev(values)


def detect_anomalies(values, mean, standard_deviation, k=3.0):
    """Return the subset of samples that look anomalous.

    A value is considered anomalous when it lies more than ``k`` standard
    deviations away from the provided mean. Missing values are ignored.

    Args:
        values: iterable of the numeric field samples.
        mean: expected central value of the field.
        standard_deviation: expected spread of the field.
        k: number of standard deviations used as the outlier threshold.

    Returns:
        A list of the anomalous samples (in their original order).
    """
    threshold = mean + k * standard_deviation
    lower_bound = mean - k * standard_deviation
    anomalies = []
    for value in values:
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if number != number:
            continue
        if number < lower_bound or number > threshold:
            anomalies.append(number)
    return anomalies


def flag_anomalies(field_values, mean=None, standard_deviation=None, k=3.0):
    """Detect anomalies in a field, computing the statistics when needed.

    When ``mean`` or ``standard_deviation`` are not provided they are derived
    from the samples themselves. This keeps the call site simple while still
    producing a meaningful statistical outlier set.

    Args:
        field_values: iterable of the numeric field samples.
        mean: optional expected central value of the field.
        standard_deviation: optional expected spread of the field.
        k: number of standard deviations used as the outlier threshold.

    Returns:
        A list of the anomalous samples (in their original order).
    """
    collected = _collect_values(field_values)
    if not collected:
        return []
    if mean is None:
        mean = _mean(collected)
    if standard_deviation is None:
        standard_deviation = _standard_deviation(collected)
    return detect_anomalies(field_values, mean, standard_deviation, k)
