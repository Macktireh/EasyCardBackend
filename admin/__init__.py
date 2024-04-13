import warnings

from flask import Flask
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy

from admin.cardAdmin import CardAdmin
from admin.userAdmin import UserAdmin
from models.card import Card
from models.user import User


def registerAdmin(app: Flask, db: SQLAlchemy) -> None:
    admin = Admin(app, name="Control Panel")

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "Fields missing from ruleset", UserWarning)
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(CardAdmin(Card, db.session))

    admin.add_link(MenuLink(name="API Docs", category="", url="/api/docs"))
    admin.add_link(MenuLink(name="Logout", category="", url="/admin/auth/logout"))
