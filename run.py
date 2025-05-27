import uvicorn
from src import app

from src.models.cities import CityModel
CityModel.create_table()


uvicorn.run(app)