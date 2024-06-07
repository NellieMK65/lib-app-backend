from pydantic import BaseModel

class CatalogueModel(BaseModel):
    name: str
    description: str
    image: str
    booking_fee: int
    author: str
    genre_id: int
    date_published: str
