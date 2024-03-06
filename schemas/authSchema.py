from flask_restx import Namespace, fields


class AuthSchema:
    api = Namespace("Auth", description="auth related operations")

    login = api.model(
        "login",
        {
            "email": fields.String(required=True, description="user email address"),
            "password": fields.String(required=True, description="user password"),
        },
    )

    signup = api.model(
        "signup",
        {
            "name": fields.String(required=True, description="user name"),
            "email": fields.String(required=True, description="user email address"),
            "password": fields.String(required=True, description="user password"),
            "passwordConfirm": fields.String(required=True, description="user password confirm"),
        },
    )

    token = api.model("token", {"token": fields.String(description="user api token")})
