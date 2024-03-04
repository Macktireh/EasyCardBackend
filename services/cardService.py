from repositories.cardRepository import CardRepository
from utils.types import CardIn


class CardService:

    def __init__(self, cardRepository: CardRepository) -> None:
        self.cardRepository = cardRepository


    def getCards(self):
        return self.cardRepository.getAll()

    def createCard(self, payload: CardIn):
        return self.cardRepository.create(**payload)

