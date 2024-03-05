from flask_injector import singleton

from models.card import Card
from repositories.cardRepository import CardRepository
from services.cardNumberExtractorService import CardNumberExtractorService
from services.cardService import CardService


def configure(binder):
    binder.bind(
        CardRepository,
        to=CardRepository(model=Card),
        scope=singleton,
    )
    binder.bind(
        CardService,
        to=CardService(cardRepository=CardRepository(model=Card)),
        scope=singleton,
    )
    binder.bind(
        CardNumberExtractorService,
        to=CardNumberExtractorService(),
        scope=singleton,
    )
