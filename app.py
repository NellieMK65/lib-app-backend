from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.genre import Genre
from models.catalogue import Catalogue
from validation_models import CatalogueModel

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_credentials = True, allow_methods = ["*"], allow_headers = ["*"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/genres')
def genres():
    genres = Genre.find_all()

    return genres


@app.get('/catalogue')
def get_catalogues():
    return [{"name": "Inferno"}]

@app.post('/catalogue')
def save_catalogue(data: CatalogueModel):
    catalogue = Catalogue(data.name, data.description, data.image, data.booking_fee, data.author, data.genre_id, data.date_published)
    catalogue.save()

    return catalogue.to_dict()
