from abc import ABC, abstractmethod

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
    def createAllCards(self, payload: list[CardIn]) -> None:
        """
        A method to create multiple cards using the provided payload and return the created cards.

        Parameters:
            payload (List[CardIn]): The payload to create the cards.

        Returns:
            None
        """
        raise NotImplementedError

    @abstractmethod
    def getCards(self) -> list[Card]:
        """
        A method to retrieve the cards and their associated information.

        Returns:
            List[Card]: A list of Card objects representing the retrieved cards.
        """
        raise NotImplementedError

    @abstractmethod
    def getCard(self, publicId: str) -> Card:
        """
        A description of the entire function, its parameters, and its return types.

        Args:
            publicId (str): The public ID of the card to retrieve.

        Returns:
            Card: The retrieved card object.
        """
        raise NotImplementedError

    @abstractmethod
    def updateCard(self, publicId: str, payload: CardIn) -> Card:
        """
        Updates a card with the given public ID using the provided payload.

        Args:
            publicId (str): The public ID of the card to be updated.
            payload (CardIn): The payload containing the updated card information.

        Returns:
            Card: The updated card object.
        """
        raise NotImplementedError

    @abstractmethod
    def deleteCard(self, publicId: str) -> None:
        """
        A description of the entire function, its parameters, and its return types.

        Args:
            publicId (str): The public ID of the card to be deleted.

        Returns:
            None
        """
        raise NotImplementedError
