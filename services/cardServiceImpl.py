from typing import List

from models.card import Card
from repositories.cardRepository import CardRepository
from services.cardService import CardService
from utils.types import CardIn


class CardServiceImpl(CardService):
    def __init__(self, cardRepository: CardRepository) -> None:
        self.cardRepository = cardRepository

    def createCard(self, payload: CardIn) -> Card:
        return self.cardRepository.create(**payload)

    def getCards(self) -> List[Card]:
        cards = self.cardRepository.getAll()
        return [card.toDict() for card in cards]

    def getCardById(self, id: int) -> Card:
        return self.cardRepository.getById(id)

    def updateCard(self, id: int, payload: CardIn) -> Card:
        card = self.getCardById(id)
        for key, value in payload.items():
            setattr(card, key, value)
        return self.cardRepository.save(card)

    def deleteCard(self, id: int) -> None:
        return self.cardRepository.delete(id)
