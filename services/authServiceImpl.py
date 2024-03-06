from typing import Dict

from werkzeug import exceptions

from models.user import User
from repositories.userRepository import UserRepository
from services.authService import AuthService
from services.tokenService import TokenService
from utils.types import RequestLoginDTO, RequestSignupDTO, TokenPayload
from validators.authValidator import AuthValidator


class AuthServiceImpl(AuthService):
    def __init__(self, userRepository: UserRepository) -> None:
        self.userRepository = userRepository

    def register(self, data: RequestSignupDTO) -> Dict[str, str]:
        AuthValidator.validateSignupRaise(**data)

        if self.userRepository.exists(email=data["email"]):
            raise exceptions.Conflict("User already exists")

        data.pop("passwordConfirm", None)
        self.userRepository.create(**data)

        return dict(message="You have registered successfully.")

    def login(self, data: RequestLoginDTO) -> Dict[str, str]:
        AuthValidator.validateLoginRaise(**data)

        if not (user := self.authenticate(**data)):
            raise exceptions.Unauthorized("Invalid email address or password")

        if not user.isActive:
            raise exceptions.Unauthorized("Your account is not active")

        apiKey = TokenService.generate(TokenPayload(id=user.id, isActive=user.isActive))

        return dict(message="You have logged in successfully.", apiKey=apiKey)

    def generateApiKey(self, apiKey: str) -> Dict[str, str]:
        payload = TokenService.getPayload(apiKey)
        user = self.userRepository.getById(payload["id"])
        apiKey = TokenService.generate(TokenPayload(id=user.id, isActive=user.isActive))
        return dict(apiKey=apiKey)

    def verifyApiKey(self, apiKey: str) -> dict[str, str]:
        user = TokenService.verify(apiKey)
        if not user:
            raise exceptions.Unauthorized("Invalid API Key")
        return dict(message="API Key is valid")

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.userRepository.getByEmail(email)
        if user and user.checkPassword(password):
            return user
        return None
