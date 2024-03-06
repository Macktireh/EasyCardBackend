from abc import ABC, abstractmethod
from typing import List

from models.card import Card
from utils.types import CardIn


class CardService(ABC):
    @abstractmethod
    def createCard(self, payload: CardIn) -> Card:
        """
        A method to create a card using the provided payload and return the created card.

        Parameters:
            payload (CardIn): The payload to create the card.

        Returns:
            Card: The created card.
        """
        raise NotImplementedError

    @abstractmethod
    def getCards(self) -> List[Card]:
        """
        A method to retrieve the cards and their associated information.

        Returns:
            List[Card]: A list of Card objects representing the retrieved cards.
        """
        raise NotImplementedError

    @abstractmethod
    def getCardById(self, id: int) -> Card:
        raise NotImplementedError

    @abstractmethod
    def updateCard(self, id: int, payload: CardIn) -> Card:
        raise NotImplementedError

    @abstractmethod
    def deleteCard(self, id: int) -> None:
        raise NotImplementedError
