import unittest
from http import HTTPStatus

from flask import Flask
from flask_injector import FlaskInjector
from flask_testing import TestCase

from config.app import createApp, db
from config.providers import configure
from repositories.userRepository import userRepository
from urls.api import router


class AuthControllerTestCase(TestCase):
    singupEndpoint = "/api/auth/signup"
    loginEndpoint = "/api/auth/login"
    verifyEndpoint = "/api/auth/verify"

    def create_app(self) -> Flask:
        app = createApp("testing")
        app.register_blueprint(router)
        FlaskInjector(app=app, modules=[configure])
        return app

    def setUp(self) -> None:
        db.create_all()
        self.data = {
            "email": "jacksmith@gmail.com",
            "name": "Jack Smith",
            "password": "Test@123",
            "passwordConfirm": "Test@123",
        }
        self.user1 = userRepository.create(name="Bob Johnson", email="bob.johnson@example.com", password=self.data["password"])
        self.user2 = userRepository.create(
            name="Alice Smith",
            email="alice.doe@example.com",
            password=self.data["password"],
            isActive=False,
        )

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_controller_auth_signup_success(self) -> None:
        response = self.client.post(self.singupEndpoint, json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_controller_auth_signup_fail(self) -> None:
        # case: passwords do not match
        data = self.data.copy()
        data["passwordConfirm"] = "Test@1234"
        response = self.client.post(self.singupEndpoint, json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        # case: invalid email
        data = self.data.copy()
        data["email"] = "bob.doe@"
        response = self.client.post(self.singupEndpoint, json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        # case: user already exists
        data = self.data.copy()
        data["email"] = "bob.johnson@example.com"
        response = self.client.post(self.singupEndpoint, json=data)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)

    def test_controller_auth_login_success(self) -> None:
        data = {"email": self.user1.email, "password": self.data["password"]}
        response = self.client.post(self.loginEndpoint, json=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_controller_auth_login_fail(self) -> None:
        # case: user does not exist
        data = {"email": "user.does.not@example.com", "password": self.data["password"]}
        response = self.client.post(self.loginEndpoint, json=data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: password is incorrect
        data = {"email": self.user1.email, "password": "Test@1234"}
        response = self.client.post(self.loginEndpoint, json=data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: user is not active
        data = {"email": self.user2.email, "password": self.data["password"]}
        response = self.client.post(self.loginEndpoint, json=data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_controller_auth_verify_api_key_success(self) -> None:
        data = {"email": self.user1.email, "password": self.data["password"]}
        response = self.client.post(self.loginEndpoint, json=data)
        apiKey = response.json["apiKey"]
        response = self.client.get(f"{self.verifyEndpoint}?apiKey={apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_controller_auth_verify_api_key_fail(self) -> None:
        apiKey = "invalid"
        response = self.client.get(f"{self.verifyEndpoint}?apiKey={apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


if __name__ == "__main__":
    unittest.main()
