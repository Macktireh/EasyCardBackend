from flask_injector import Binder, singleton

from repositories.cardRepository import CardRepository, cardRepository
from repositories.userRepository import UserRepository, userRepository
from services.authService import AuthService
from services.authServiceImpl import AuthServiceImpl
from services.cardNumberExtractorService import CardNumberExtractorService
from services.cardNumberExtractorServiceImpl import CardNumberExtractorServiceImpl
from services.cardService import CardService
from services.cardServiceImpl import CardServiceImpl


def configure(binder: Binder) -> None:
    binder.bind(interface=UserRepository, to=userRepository, scope=singleton)
    binder.bind(interface=CardRepository, to=cardRepository, scope=singleton)
    binder.bind(interface=CardService, to=CardServiceImpl(cardRepository), scope=singleton)
    binder.bind(interface=CardNumberExtractorService, to=CardNumberExtractorServiceImpl(), scope=singleton)
    binder.bind(interface=AuthService, to=AuthServiceImpl(userRepository), scope=singleton)
