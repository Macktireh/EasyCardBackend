from flask_injector import singleton

from models.card import Card
from models.user import User
from repositories.cardRepository import CardRepository
from repositories.userRepository import UserRepository
from services.authService import AuthService
from services.authServiceImpl import AuthServiceImpl
from services.cardNumberExtractorService import CardNumberExtractorService
from services.cardNumberExtractorServiceImpl import CardNumberExtractorServiceImpl
from services.cardService import CardService
from services.cardServiceImpl import CardServiceImpl


def configure(binder):
    binder.bind(
        UserRepository,
        to=UserRepository(model=Card),
        scope=singleton,
    )
    binder.bind(
        CardRepository,
        to=CardRepository(model=Card),
        scope=singleton,
    )
    binder.bind(
        CardService,
        to=CardServiceImpl(cardRepository=CardRepository(model=Card)),
        scope=singleton,
    )
    binder.bind(
        CardNumberExtractorService,
        to=CardNumberExtractorServiceImpl(),
        scope=singleton,
    )
    binder.bind(
        AuthService,
        to=AuthServiceImpl(userRepository=UserRepository(model=User)),
        scope=singleton,
    )
