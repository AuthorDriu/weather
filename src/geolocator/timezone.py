from datetime import timezone
from timezonefinder import TimezoneFinder

from src.schemes.weather import Coordinates


_tz_finder = TimezoneFinder()


def get_timezone(coords: Coordinates) -> str | None:
    tz = _tz_finder.timezone_at(lng=coords.longitude, lat=coords.latitude)
    return timezone(tz)