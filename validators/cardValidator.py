from http import HTTPStatus
from typing import List

from flask_restx import abort

from utils.types import CardIn


class CardValidator:
    @staticmethod
    def validateCode(code: str) -> bool:
        return len(code) == 12 and code.isdigit()

    @staticmethod
    def validateCardType(cardType: str) -> bool:
        return cardType in ["500", "1000", "2000", "5000", "10000"]

    @staticmethod
    def validateRaise(payload: CardIn, message: str = "The information provided is not valid") -> None:
        errors = {}

        required_fields = ["code", "cardType"]

        for field in required_fields:
            if not payload.get(field):
                errors[field] = f"{field.capitalize()} is required"

        if not CardValidator.validateCode(payload["code"]):
            errors["code"] = "Code is invalid, must be 12 digits"

        if not CardValidator.validateCardType(payload["cardType"]):
            errors["cardType"] = (
                f"Card type is invalid, '{payload['cardType']}' is not one of ['500', '1000', '2000', '5000', '10000']"
            )

        if errors:
            abort(HTTPStatus.BAD_REQUEST, message=message, errors=errors)

    @staticmethod
    def validateList(payload: List[CardIn]) -> None:
        codes = [card["code"] for card in payload]
        if len(set(codes)) != len(codes):
            abort(HTTPStatus.BAD_REQUEST, message="All codes must be unique")
