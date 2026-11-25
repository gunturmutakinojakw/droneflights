# === Stage 29: Текстовая гистограмма ===
# Project: DroneFlights
from collections import Counter

BLOCK = "#"
def build_height_histogram(heights):
    if not heights:
        return ""
    low = min(heights)
    high = max(heights)
    span = high - low
    buckets = 10
    bins = [0] * (buckets + 1)
    for h in heights:
        idx = int((h - low) / span * buckets)
        if idx == buckets:
            idx = buckets - 1
        bins[idx] += 1
    max_count = max(bins)
    width = 40
    lines = [f"{'Height':>10} | {'Range':>15} | {'Count':>6} | {'Bars':<40}"]
    for i in range(buckets + 1):
        low_edge = low + i * span / buckets
        high_edge = low + (i + 1) * span / buckets
        label = f"{low_edge:.0f}-{high_edge:.0f}"
        bars = BLOCK * (bins[i] * width // max_count)
        lines.append(f"{label:>10} | {label:>15} | {bins[i]:>6} | {bars}")
    return "\n".join(lines)
