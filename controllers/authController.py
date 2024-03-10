from http import HTTPStatus

from flask import request
from flask_injector import inject
from flask_restx import Resource

from middlewares.authMiddleware import api_key_required
from schemas.authSchema import AuthSchema
from services.authService import AuthService

api = AuthSchema.api


@api.route("/signup")
@inject
class SignupController(Resource):
    def __init__(self, authService: AuthService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.authService = authService

    @api.response(HTTPStatus.CREATED, "User successfully registered.")
    @api.doc("user signup")
    @api.expect(AuthSchema.signup, validate=True)
    def post(self):
        """User Signup"""
        return self.authService.register(request.json), HTTPStatus.CREATED


@api.route("/login")
@inject
class LoginController(Resource):
    def __init__(self, authService: AuthService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.authService = authService

    @api.response(HTTPStatus.OK, "User successfully login.")
    @api.doc("user login")
    @api.expect(AuthSchema.login, validate=True)
    def post(self):
        """User Login"""
        return self.authService.login(request.json)


@api.route("/generate")
@inject
class GenerateApiKeyController(Resource):
    def __init__(self, authService: AuthService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.authService = authService

    @api.doc("generate api key")
    @api.marshal_with(AuthSchema.token)
    @api_key_required
    def get(self):
        """Generate api key"""
        return self.authService.generateApiKey(request.args.get("apiKey"))


@api.route("/verify")
@inject
class VerifyApiKeyController(Resource):
    def __init__(self, authService: AuthService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.authService = authService

    @api.doc("verify api key")
    @api.marshal_with(AuthSchema.token)
    @api_key_required
    def get(self):
        """Verify api key"""
        return self.authService.verifyApiKey(request.args.get("apiKey"))
