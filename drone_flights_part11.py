# === Stage 11: Текстовый поиск ===
# Project: DroneFlights
import re

def build_text_search(query, text, highlight=True):
    query = query.strip()
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    if not highlight:
        return pattern.sub(query, text, flags=re.IGNORECASE)
    marker = '\033[90m\033[4m\033[93m'
    end_marker = '\033[0m'
    def _wrap(match):
        return f'{marker}{match.group(0)}{end_marker}'
    return pattern.sub(_wrap, text)

def search_flights(query, flights):
    results = [flight for flight in flights if query.lower() in flight.get('location', '').lower()]
    if not results:
        return []
    lines = []
    lines.append(f'Found {len(results)} flight(s) matching "{query}":')
    for index, flight in enumerate(results, start=1):
        location = flight['location']
        duration = flight['duration']
        altitude = flight['altitude']
        date = flight['date']
        location_display = build_text_search(query, location, highlight=True)
        line = f'  {index}. {location_display}'
        line += f' | {duration} min'
        line += f' | {altitude} m'
        line += f' | {date}'
        lines.append(line)
    return lines

class Flight:
    def __init__(self, location, duration, altitude, date):
        self.location = location
        self.duration = duration
        self.altitude = altitude
        self.date = date

    def to_dict(self):
        return {
            'location': self.location,
            'duration': self.duration,
            'altitude': self.altitude,
            'date': self.date,
        }

    def __repr__(self):
        return f'Flight(location={self.location!r}, duration={self.duration!r}, altitude={self.altitude!r}, date={self.date!r})'

def create_flight(location, duration, altitude, date):
    return Flight(location, duration, altitude, date)

if __name__ == '__main__':
    sample = [
        Flight('Central Park, New York', 25, 120, '2024-05-01'),
        Flight('Golden Gate, San Francisco', 30, 90, '2024-05-02'),
        Flight('Times Square, New York', 20, 100, '2024-05-03'),
    ]
    for line in search_flights('new york', sample):
        print(line)
