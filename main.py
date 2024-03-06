from flask import redirect
from flask_injector import FlaskInjector
from flask_migrate import Migrate

from admin import registerAdmin
from commands import createsuperuser, postman
from config.app import createApp, db
from config.provider import configure
from config.settings import ConfigName
from urls.api import router as apiRouter
from utils.functions import getEnvVar

ENV = getEnvVar("FLASK_ENV", ConfigName.DEVELOPEMENT)

app = createApp(ENV)

migrate = Migrate(app, db)

if ENV == ConfigName.DEVELOPEMENT:
    registerAdmin(app, db)

app.register_blueprint(apiRouter)


@app.route("/")
def index() -> str:
    return redirect("/api/docs")


app.cli.add_command(createsuperuser)
app.cli.add_command(postman)

FlaskInjector(app=app, modules=[configure])
