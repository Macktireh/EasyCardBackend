from models.card import Card
from repositories.baseRepositorySQLalchemy import BaseRepositorySQLAlchemy


class CardRepository(BaseRepositorySQLAlchemy[Card]):
    def __init__(self, model: Card) -> None:
        super().__init__(model)


cardRepository = CardRepository(Card)
