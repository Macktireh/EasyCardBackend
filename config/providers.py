from flask_injector import singleton

from repositories.cardRepository import CardRepository, cardRepository
from repositories.userRepository import UserRepository, userRepository
from services.authService import AuthService
from services.authServiceImpl import AuthServiceImpl
from services.cardNumberExtractorService import CardNumberExtractorService
from services.cardNumberExtractorServiceImpl import CardNumberExtractorServiceImpl
from services.cardService import CardService
from services.cardServiceImpl import CardServiceImpl


def configure(binder):
    binder.bind(
        UserRepository,
        to=userRepository,
        scope=singleton,
    )
    binder.bind(
        CardRepository,
        to=cardRepository,
        scope=singleton,
    )
    binder.bind(
        CardService,
        to=CardServiceImpl(cardRepository),
        scope=singleton,
    )
    binder.bind(
        CardNumberExtractorService,
        to=CardNumberExtractorServiceImpl(),
        scope=singleton,
    )
    binder.bind(
        AuthService,
        to=AuthServiceImpl(userRepository),
        scope=singleton,
    )
