from enum import Enum

from config.app import db
from models import BaseModel


class TypeEnum(str, Enum):
    CARD_500 = "500"
    CARD_1000 = "1000"
    CARD_2000 = "2000"
    CARD_5000 = "5000"
    CARD_10000 = "10000"


class Card(BaseModel):
    __tablename__ = "cards"

    code = db.Column(db.String(12), unique=True, nullable=False)
    type = db.Column(db.Enum(TypeEnum), nullable=False)
    isValid = db.Column(db.Boolean, default=True, nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "code": self.code,
            "type": self.type,
            "isValid": self.isValid,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
