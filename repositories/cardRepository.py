from models.card import Card
from repositories.baseRepositorySQLalchemy import BaseRepositorySQLalchemy


class CardRepository(BaseRepositorySQLalchemy):
    def __init__(self, model: Card) -> None:
        super().__init__(model)
