import warnings

from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

from admin.cardAdmin import CardAdmin
from admin.userAdmin import UserAdmin
from models.card import Card
from models.user import User


def registerAdmin(app: Flask, db: SQLAlchemy) -> None:
    admin = Admin(app, name="Control Panel")

    with warnings.catch_warnings():
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(CardAdmin(Card, db.session))
