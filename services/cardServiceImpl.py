from typing import List

from werkzeug import exceptions

from models.card import Card
from repositories.cardRepository import CardRepository
from services.cardService import CardService
from utils.types import CardIn
from validators.cardValidator import CardValidator


class CardServiceImpl(CardService):
    def __init__(self, cardRepository: CardRepository) -> None:
        self.cardRepository = cardRepository

    def createCard(self, payload: CardIn) -> Card:
        CardValidator.validateRaise(payload)
        if self.cardRepository.exists(code=payload["code"]):
            raise exceptions.Conflict("Card already exists")
        return self.cardRepository.create(**payload)

    def createAllCards(self, payload: List[CardIn]) -> None:
        CardValidator.validateList(payload)
        for i, card in enumerate(payload):
            CardValidator.validateRaise(card, f"The information provided by card #{i+1} is not valid")
            if self.cardRepository.exists(code=card["code"]):
                raise exceptions.Conflict(f"Card #{i+1} already exists")
        self.cardRepository.createAll(payload)

    def getCards(self) -> List[Card]:
        return self.cardRepository.getAll()

    def getCard(self, publicId: str) -> Card:
        return self.cardRepository.getOr404(publicId=publicId)

    def updateCard(self, publicId: str, payload: CardIn) -> Card:
        card = self.cardRepository.getOr404(publicId=publicId)
        for key, value in payload.items():
            setattr(card, key, value)
        return self.cardRepository.save(card)

    def deleteCard(self, publicId: str) -> None:
        card = self.cardRepository.getOr404(publicId=publicId)
        self.cardRepository.delete(card)
