import random 
import string
import hashlib

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

from peewee import DoesNotExist

from src.schemes.weather import City, Coordinates
from src.models.cities import CityModel


_geolocator = Nominatim(user_agent="test_weather_app")


def _hash(city: City) -> bytes:
    sha256 = hashlib.sha256(
        city.name.strip().lower().encode()
    ).digest()
    return sha256[:8]


def _from_database(city: City) -> tuple[bool, Coordinates | None]:
    """from_database()

    Принимает город, возвращает два значения:
        bool - существует ли данная запись в базе данных
        Coordinates | None - если существует и указаны координаты, то вернёт координаты, иначе None
    """
    hash = _hash(city)
    try:
        row: CityModel = CityModel.select().where(CityModel.hash == hash).get()

    except DoesNotExist:
        return False, None
    
    if row.longitude is None and row.latitude is None:
        return True, None
    
    coords = Coordinates(latitude=row.latitude, longitude=row.longitude)
    return True, coords


def _from_geolocator(city: City) -> Coordinates | None:
    global _geolocator
    try:
        location = _geolocator.geocode(city.name)

    except Exception:
        return None

    if not location:
        return None

    coords = Coordinates(latitude=location.latitude, longitude=location.longitude)
    return coords


def get_coordinates(city: City) -> Coordinates:
    found, coords = _from_database(city)
    if not found:
        coords = _from_geolocator(city)
        if coords is None:
            latitude = None
            longitude = None
        else:
            latitude = coords.latitude
            longitude = coords.longitude
        
        hash = _hash(city)
        CityModel.insert(hash=hash, latitude=latitude, longitude=longitude).execute()

    return coords