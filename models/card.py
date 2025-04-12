from config.app import db
from models import BaseModel


class Card(BaseModel):
    __tablename__ = "cards"

    code = db.Column(db.String(12), unique=True, nullable=False)
    cardType = db.Column(
        db.Enum("500", "1000", "2000", "5000", "10000", name="card_type"), nullable=False
    )
    isValid = db.Column(db.Boolean, default=True, nullable=False)
