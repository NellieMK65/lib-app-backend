from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CatalogueModel(BaseModel):
    name: str
    description: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/catalogue')
def get_catalogues():
    return [{"name": "Inferno"}]

@app.post('/catalogue')
def save_catalogue(data: CatalogueModel):
    print(data)
