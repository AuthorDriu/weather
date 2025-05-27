from datetime import datetime, timezone

import aiohttp

from src.schemes.weather import WeatherRequest
from src.schemes.weather import Coordinates
from src.schemes.weather import Weather
from src.schemes.weather import City

from src.geolocator.geolocator import get_coordinates


API_URL_BASE = 'http://api.open-meteo.com/v1/forecast'


class WeatherClient:
    """WeatherClient
    Предназначен упростить доступ к api open-meteo,
    так как как не совсем оно понятно как делать,
    а времени разбираться нет

    Должен реализовывать async get(WeatherRequest) -> Weather
    """

    def __init__(self):
        pass

    async def get(self, target: WeatherRequest) -> Weather | None:
        """WeatherClient.get(target: WeatherRequest)

        Возвращает текущую погоду и почасовой прогноз для заданной цели,
        если по какой-то причине получить прогноз не удалось, возвращается None

        Args:
            target (WeatherRequest): цель, для которой ищется прогноз погоды

        Returns:
            Weather | None: Прогноз погоды или None
        """
        coords: Coordinates = None
        if isinstance(target.target, City):
            coords = get_coordinates(target.target)
            if not coords:
                return None
        else:
            coords = target.target

        weather = await self._fetch_weather(coords)
        return weather
        
    async def _fetch_weather(self, coords: Coordinates) -> Weather:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL_BASE, params=self._params_for(coords)) as resp:
                if resp.status != 200:
                    return None
                
                resp_data = await resp.json()
        
        weather = self._get_current_weather(resp_data)
        weather_list = self._get_forecast_weather(resp_data)

        if len(weather_list) != 0:
            weather.forecast = weather_list

        return weather
    
    def _get_current_weather(self, data: dict) -> Weather:
        time = data['current']['time']
        temperature = data['current']['temperature_2m']
        humidity = data['current']['relative_humidity_2m']
        wind_speed = data['current']['wind_speed_10m']
        wind_direction = data['current']['wind_direction_10m']

        weather = Weather(
            time=datetime.fromisoformat(time),
            temperature=temperature,
            relative_humidity=humidity,
            wind_speed=wind_speed,
            wind_direction=wind_direction
        )
        return weather

    def _get_forecast_weather(self, data: dict) -> Weather:
        weather_list: list[Weather] = []

        times = data['hourly']['time']
        temperature = data['hourly']['temperature_2m']
        humidity = data['hourly']['relative_humidity_2m']
        wind_speed = data['hourly']['wind_speed_10m']
        wind_direction = data['hourly']['wind_direction_10m']

        for _weather in zip(times, temperature, humidity, wind_speed, wind_direction):
            weather = Weather(
                time=datetime.fromisoformat(_weather[0]),
                temperature=_weather[1],
                relative_humidity=_weather[2],
                wind_speed=_weather[3],
                wind_direction=_weather[4]
            )
            weather_list.append(weather)
        
        return weather_list

    def _params_for(self, coords: Coordinates) -> dict:
        return {
            'longitude': coords.longitude,
            'latitude': coords.latitude,
            'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m',
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m'
        }


    