from enum import Enum
from typing import TypedDict


class RequestLoginDTO(TypedDict):
    email: str
    password: str


class RequestSignupDTO(RequestLoginDTO):
    name: str
    passwordConfirm: str


class CardIn(TypedDict):
    code: str
    cardType: str


class TokenPayload(TypedDict):
    publicId: int
    isActive: bool


class TypeEnum(str, Enum):
    CARD_500 = "500"
    CARD_1000 = "1000"
    CARD_2000 = "2000"
    CARD_5000 = "5000"
    CARD_10000 = "10000"
