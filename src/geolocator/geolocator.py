from geopy.geocoders import Nominatim

from src.schemes.weather import City, Coordinates


_geolocator = Nominatim(user_agent='weather app')


def get_coordinates(city: City) -> Coordinates | None:
    location = _geolocator.geocode(city.name)
    print(f"Найдены координаты: {location.latitude} {location.longitude}")

    if not location:
        return None

    coords = Coordinates(latitude=location.latitude, longitude=location.longitude)
    return coords
