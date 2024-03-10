from datetime import datetime
from uuid import uuid4

from config.app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    publicId = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid4().hex))
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
