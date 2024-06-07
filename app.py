from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.catalogue import Genre

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_credentials = True, allow_methods = ["*"], allow_headers = ["*"])

class CatalogueModel(BaseModel):
    name: str
    description: str

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
    print(data)
