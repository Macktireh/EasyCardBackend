from flask import Blueprint
from flask_restx import Api

from controllers.authController import api as authApi
from controllers.cardController import api as cardApi

router = Blueprint("api", __name__, url_prefix="/api")


api = Api(
    router,
    version="1.0",
    title="EasyCardBackend REST API",
    description="EasyCardBackend API documentation for developers to use it.",
    doc="/docs",
    terms_url="https://www.google.com",
)

api.add_namespace(authApi, path="/auth")
api.add_namespace(cardApi, path="/cards")
