import contextlib
from http import HTTPStatus

from flask import get_flashed_messages, redirect
from flask_injector import FlaskInjector
from flask_migrate import Migrate
from werkzeug.wrappers.response import Response

from commands import createsuperuser, dcards, gcards, postman, test
from config.app import createApp, db
from config.providers import configure
from config.settings import ConfigName, GlobalConfig
from urls.api import router as apiRouter

app = createApp(GlobalConfig.ENV)

migrate = Migrate(app, db)

if GlobalConfig.ENV == ConfigName.DEVELOPEMENT:
    with contextlib.suppress(Exception):
        from admin import registerAdmin

        registerAdmin(app, db)

app.register_blueprint(apiRouter)


@app.route("/")
def index() -> Response:
    return redirect("/api/docs")


@app.route("/health-check")
def health_check() -> Response:
    return Response(response="OK", status=HTTPStatus.OK)


app.cli.add_command(createsuperuser)
app.cli.add_command(gcards)
app.cli.add_command(dcards)
app.cli.add_command(postman)
app.cli.add_command(test)

FlaskInjector(app=app, modules=[configure])

app.jinja_env.globals.update(
    {"url_for": app.url_for, "get_flashed_messages": get_flashed_messages}
)
