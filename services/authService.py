from abc import ABC, abstractmethod
from typing import Dict

from models.user import User
from utils.types import RequestLoginDTO, RequestSignupDTO


class AuthService(ABC):
    @abstractmethod
    def register(self, data: RequestSignupDTO) -> Dict[str, str]:
        """
        Register a new user with the provided signup data.

        Args:
            data (RequestSignupDTO): The signup data for the new user.

        Returns:
            Dict[str, str]: A dictionary containing a message confirming successful registration.
        """
        raise NotImplementedError

    @abstractmethod
    def login(self, data: RequestLoginDTO) -> Dict[str, str]:
        """
        Authenticate user and generate an API key for successful login.

        Args:
            data (RequestLoginDTO): The login request data.

        Returns:
            Dict[str, str]: A dictionary containing a success message and the generated API key.
        """
        raise NotImplementedError

    @abstractmethod
    def generateApiKey(self, user: User) -> Dict[str, str]:
        """
        Generate an API key for the given user and return it as a dictionary.

        Args:
            apiKey (str): The API key to be used for generation.

        Returns:
            Dict[str, str]: A dictionary containing the generated API key.
        """
        raise NotImplementedError

    @abstractmethod
    def verifyApiKey(self, apiKey: str) -> Dict[str, str]:
        """
        Verify the API key and return a dictionary with a message indicating its validity.

        Args:
            apiKey (str): The API key to be verified.

        Returns:
            dict[str, str]: A dictionary with a message indicating the validity of the API key.
        """
        raise NotImplementedError

    @abstractmethod
    def authenticate(self, email: str, password: str) -> User | None:
        """
        Authenticate a user with the given email and password.

        :param email: A string representing the user's email.
        :param password: A string representing the user's password.
        :return: Either a User object if authentication is successful, or None if authentication fails.
        """
        raise NotImplementedError
