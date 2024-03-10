from functools import wraps

from flask import request
from werkzeug import exceptions

from services.tokenService import TokenService


def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        apiKey = request.args.get("apiKey")
        if not apiKey:
            raise exceptions.Unauthorized("Missing API Key!")
        user = TokenService.verify(apiKey)
        if not user:
            raise exceptions.Unauthorized("Invalid API Key!")
        return f(*args, **kwargs)

    return decorated
