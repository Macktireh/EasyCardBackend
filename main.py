

from app import createApp
from config.settings import ConfigName, getEnvVar


app = createApp(getEnvVar("FLASK_ENV", ConfigName.DEVELOPEMENT))

@app.route("/")
def index():
    return "Hello World!"
