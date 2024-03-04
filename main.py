from flask_injector import FlaskInjector
from flask_migrate import Migrate

from admin import registerAdmin
from config.app import createApp, db
from config.provider import configure
from config.settings import ConfigName, getEnvVar
from urls.api import router as routes

ENV = getEnvVar("FLASK_ENV", ConfigName.DEVELOPEMENT)

app = createApp(ENV)

migrate = Migrate(app, db)

if ENV == ConfigName.DEVELOPEMENT:
    registerAdmin(app, db)

app.register_blueprint(routes)

@app.route("/")
def index() -> str:
    return "Hello World!"


FlaskInjector(app=app, modules=[configure])
