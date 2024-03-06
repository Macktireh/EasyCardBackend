from typing import NoReturn

from config.app import bcrypt, db
from models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=True)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    passwordHash = db.Column(db.Text, nullable=False)

    @property
    def password(self) -> NoReturn:
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password: str) -> None:
        self.passwordHash = bcrypt.generate_password_hash(password).decode("utf-8")

    def checkPassword(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.passwordHash, password)

    def __repr__(self) -> str:
        return f"<User '{self.email}'>"
