from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.schemes.weather import City, WeatherRequest, Weather
from src.open_meteo_api.client import WeatherClient


app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/')
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name='index.html',
    )


@app.get('/api/fetch')
async def fetch_weather(request: Request, city: str) -> Weather | None:
    city = City(name=city)
    weather_req = WeatherRequest(target=city)
    weather_client = WeatherClient()
    weather = await weather_client.get(weather_req)
    return weather if weather else None
