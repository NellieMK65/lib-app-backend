from pydantic import BaseModel

class CatalogueModel(BaseModel):
    name: str
    description: str
    image: str
    booking_fee: int
    author: str
    genre_id: int
    date_published: str

class BookingModel(BaseModel):
    name: str
    phone: str
    booking_from: str
    booking_to: str
    catalogue_id: int
