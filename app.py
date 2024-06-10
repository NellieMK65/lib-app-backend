from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.genre import Genre
from models.catalogue import Catalogue
from models.user import User
from models.booking import Booking
from validation_models import CatalogueModel, BookingModel

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
    catalogues = Catalogue.find_all()

    return catalogues

@app.post('/catalogue')
def save_catalogue(data: CatalogueModel):
    catalogue = Catalogue(data.name, data.description, data.image, data.booking_fee, data.author, data.genre_id, data.date_published)
    catalogue.save()

    return catalogue.to_dict()

@app.post('/booking')
def book_catalogue(data: BookingModel):
    #  check if user exists
    user = User.find_one_by_phone(data.phone)
    catalogue = Catalogue.find_one(data.catalogue_id)

    if user:
        booking = Booking(data.booking_from, data.booking_to, catalogue.booking_fee, catalogue.id, user.id)
        booking.save()

        catalogue.is_booked = True
        catalogue.update()

        return {"message": "Booking successful"}
    else:
        user = User(data.name, data.phone)
        user.save()

        booking = Booking(data.booking_from, data.booking_to, catalogue.booking_fee, catalogue.id, user.id)
        booking.save()

        return {"message": "Booking successful"}
