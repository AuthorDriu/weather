from datetime import datetime, timezone

import pandas as pd
import aiohttp

from src.schemes.weather import WeatherRequest
from src.schemes.weather import Coordinates
from src.schemes.weather import Weather
from src.schemes.weather import City

from src.geolocator.geolocator import get_coordinates
from src.geolocator.timezone import get_timezone


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
        coords: Coordinates = None
        if isinstance(target.target, City):
            print(f"Цель из названия города: {target.target.name}")
            coords = get_coordinates(target.target)
            print(f"Координаты: {coords}")
            if not coords:
                return None
        else:
            print(f"Координаты: {target.target}")
            coords = target.target

        weather = await self._do_request(coords)
        return weather
        
    async def _do_request(self, coords: Coordinates) -> list[Weather]:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL_BASE, params=self._params_for(coords)) as resp:
                if resp.status != 200:
                    return None
                
                resp_data = await resp.json()
        
        weather_list = self._get_weathers(resp_data)
        return weather_list
        
    def _get_weathers(self, data: dict) -> Weather:
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
            #'current': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m',
            'hourly': 'temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m'
        }


    