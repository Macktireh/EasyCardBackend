from typing import TypedDict


class RequestLoginDTO(TypedDict):
    email: str
    password: str


class RequestSignupDTO(RequestLoginDTO):
    name: str
    passwordConfirm: str


class CardIn(TypedDict):
    code: str
    type: str


class TokenPayload(TypedDict):
    id: int
    isActive: bool
