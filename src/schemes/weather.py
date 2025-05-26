from datetime import datetime
from pydantic import BaseModel


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class City(BaseModel):
    """City
    хранит название города, чтоб в дальнейшем получить координаты
    """
    name: str


class WeatherRequest(BaseModel):
    target: Coordinates | City


class Weather(BaseModel):
    """Weather
    Описание погоды в определённый момент времени (сначала текущая, потом прогноз)
    """

    time: datetime
    temperature: float
    relative_humidity: float
    wind_speed: float
    wind_direction: int

    forecast: list['Weather'] | None = None


