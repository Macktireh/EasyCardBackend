from abc import ABC, abstractmethod
from typing import Dict

from models.user import User
from utils.types import RequestLoginDTO, RequestSignupDTO


class AuthService(ABC):
    @abstractmethod
    def register(self, data: RequestSignupDTO) -> Dict[str, str]:
        raise NotImplementedError

    def login(self, data: RequestLoginDTO) -> Dict[str, str]:
        raise NotImplementedError

    def generateApiKey(self, user: User) -> Dict[str, str]:
        raise NotImplementedError

    def verifyApiKey(self, apiKey: str) -> Dict[str, str]:
        raise NotImplementedError

    def authenticate(self, email: str, password: str) -> User | None:
        raise NotImplementedError
