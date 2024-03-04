from flask import Blueprint

from urls.api import router as routerApi

routes = Blueprint("app", __name__)

routes.register_blueprint(routerApi)
