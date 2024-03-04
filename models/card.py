from datetime import datetime
from enum import Enum

from config.app import db


class TypeEnum(str, Enum):
    CARD_500 = "500"
    CARD_1000 = "1000"
    CARD_2000 = "2000"
    CARD_5000 = "5000"
    CARD_10000 = "10000"


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    code = db.Column(db.String(12), unique=True, nullable=False)
    type = db.Column(db.Enum(TypeEnum), nullable=False)
    isValid = db.Column(db.Boolean, default=True, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
