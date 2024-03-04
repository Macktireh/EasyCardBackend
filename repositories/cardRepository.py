from models.card import Card
from repositories.baseRepository import BaseRepository


class CardRepository(BaseRepository):
    def __init__(self, model: Card) -> None:
        super().__init__(model)
