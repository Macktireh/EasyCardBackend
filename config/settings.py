import os
import secrets
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

from utils.functions import getEnvVar

BASE_DIR = Path(__file__).resolve().parent.parent
load = load_dotenv(os.path.join(BASE_DIR, ".env"))

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
PATH_TESSERACT_CMD = getEnvVar("PATH_TESSERACT_CMD", required=False)
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
API_TOKEN_EXPIRES = 60 * 60 * 24 * 7


class GlobalConfig:
    DEBUG = False
    FLASK_DEBUG = False
    FLASK_ENV = getEnvVar("FLASK_ENV", "development")
    SECRET_KEY = getEnvVar("SECRET_KEY", secrets.token_hex(32))
    SECURITY_PASSWORD_SALT = getEnvVar("SECURITY_PASSWORD_SALT", secrets.token_hex(32))
    SQLALCHEMY_ECHO = False

    TYPE_DATABASE = getEnvVar("TYPE_DATABASE", "sqlite")
    SQLALCHEMY_DATABASE_URI_SQLITE = "sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3")
    if TYPE_DATABASE == "postgresql":
        SQLALCHEMY_DATABASE_URI = f"postgresql://{getEnvVar('POSTGRES_USER')}:{getEnvVar('POSTGRES_PASSWORD')}@{getEnvVar('POSTGRES_HOST')}:{getEnvVar('POSTGRES_PORT')}/{getEnvVar('POSTGRES_DB')}"  # noqa
    else:
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_SQLITE
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True


class DevelopmentConfig(GlobalConfig):
    DEVELOPMENT = True
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PREFERRED_URL_SCHEME = "http"


class TestingConfig(GlobalConfig):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "db_test.sqlite3")
    PREFERRED_URL_SCHEME = "http"


class ProductionConfig(GlobalConfig):
    PRODUCTION = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{getEnvVar('POSTGRES_USER')}:{getEnvVar('POSTGRES_PASSWORD')}@{getEnvVar('POSTGRES_HOST')}:{getEnvVar('POSTGRES_PORT')}/{getEnvVar('POSTGRES_DB')}"  # noqa


class PostmanConfig(DevelopmentConfig):
    SERVER_NAME = getEnvVar("SERVER_NAME", "localhost:5000")
    APPLICATION_ROOT = getEnvVar("APPLICATION_ROOT", "/")


class ConfigName(str, Enum):
    DEVELOPEMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    POSTMAN = "postman"


configByName = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig, postman=PostmanConfig
)
