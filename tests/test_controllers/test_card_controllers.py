import os
import unittest
from http import HTTPStatus
from io import BytesIO
from random import randint

from flask import Flask
from flask_injector import FlaskInjector
from flask_testing import TestCase

from config.app import createApp, db
from config.providers import configure
from repositories.cardRepository import cardRepository
from repositories.userRepository import userRepository
from urls.api import router
from utils.functions import createImage
from utils.types import TypeEnum


class CardControllerTestCase(TestCase):
    cardEndpoint = "/api/cards"
    cardExtractEndpoint = "/api/cards/extract"
    loginEndpoint = "/api/auth/login"

    def create_app(self) -> Flask:
        app = createApp("testing")
        app.register_blueprint(router)
        FlaskInjector(app=app, modules=[configure])
        return app

    def setUp(self) -> None:
        db.create_all()
        self.data = {
            "code": "123456789012",
            "cardType": TypeEnum.CARD_1000,
        }
        self.cards = {
            "cards": [
                {
                    "code": str(randint(100000000000, 999999999999)),
                    "cardType": TypeEnum.CARD_500,
                },
                {
                    "code": str(randint(100000000000, 999999999999)),
                    "cardType": TypeEnum.CARD_1000,
                },
                {
                    "code": str(randint(100000000000, 999999999999)),
                    "cardType": TypeEnum.CARD_2000,
                },
                {
                    "code": str(randint(100000000000, 999999999999)),
                    "cardType": TypeEnum.CARD_5000,
                },
                {
                    "code": str(randint(100000000000, 999999999999)),
                    "cardType": TypeEnum.CARD_10000,
                },
            ]
        }
        self.card = cardRepository.create(code=str(randint(100000000000, 999999999999)), cardType=TypeEnum.CARD_500)
        cardRepository.create(code=str(randint(100000000000, 999999999999)), cardType=TypeEnum.CARD_1000)
        cardRepository.create(code=str(randint(100000000000, 999999999999)), cardType=TypeEnum.CARD_2000)

        self.user1 = userRepository.create(name="Bob Johnson", email="bob.johnson@example.com", password="Test@123")
        self.apiKey = self.client.post(
            self.loginEndpoint, json={"email": self.user1.email, "password": "Test@123"}
        ).json["apiKey"]

        size = (180, 650)
        list_text = ["Serial Number:", f"0000123456789            {self.data['code']}"]
        self.file_path = "test_image.jpg"
        createImage(size, list_text, self.file_path)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        os.remove(self.file_path)

    def test_controller_card_list_success(self) -> None:
        response = self.client.get(f"{self.cardEndpoint}?apiKey={self.apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_controller_card_list_fail(self) -> None:
        # case: invalid api key
        response = self.client.get(f"{self.cardEndpoint}?apiKey=invalid")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no api key
        response = self.client.get(f"{self.cardEndpoint}")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_controller_card_create_success(self) -> None:
        response = self.client.post(f"{self.cardEndpoint}?apiKey={self.apiKey}", json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_controller_card_create_fail(self) -> None:
        # case: invalid api key
        response = self.client.post(f"{self.cardEndpoint}?apiKey=invalid", json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no api key
        response = self.client.post(f"{self.cardEndpoint}", json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: card already exists
        data = {"code": self.card.code, "cardType": self.card.cardType}
        response = self.client.post(f"{self.cardEndpoint}?apiKey={self.apiKey}", json=data)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)

        # case: code is invalid
        data = {"code": "123", "cardType": self.card.cardType}
        response = self.client.post(f"{self.cardEndpoint}?apiKey={self.apiKey}", json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_controller_card_create_multiple_success(self) -> None:
        response = self.client.post(f"{self.cardEndpoint}/all?apiKey={self.apiKey}", json=self.cards)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_controller_card_create_multiple_fail(self) -> None:
        # case: invalid api key
        response = self.client.post(f"{self.cardEndpoint}/all?apiKey=invalid", json=self.cards)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no api key
        response = self.client.post(f"{self.cardEndpoint}/all", json=self.cards)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: card already exists
        self.cards["cards"][0]["code"] = self.card.code
        response = self.client.post(f"{self.cardEndpoint}/all?apiKey={self.apiKey}", json=self.cards)
        self.assertEqual(response.status_code, HTTPStatus.CONFLICT)

        # case: code is invalid
        data = {
            "cards": [
                {"code": "123", "cardType": self.card.cardType},
                {"code": "456", "cardType": self.card.cardType},
            ]
        }
        response = self.client.post(f"{self.cardEndpoint}/all?apiKey={self.apiKey}", json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_controller_card_get_success(self) -> None:
        response = self.client.get(f"{self.cardEndpoint}/{self.card.publicId}?apiKey={self.apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_controller_card_get_fail(self) -> None:
        # case: invalid api key
        response = self.client.get(f"{self.cardEndpoint}/{self.card.publicId}?apiKey=invalid")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no api key
        response = self.client.get(f"{self.cardEndpoint}/{self.card.publicId}")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: card does not exist
        response = self.client.get(f"{self.cardEndpoint}/{400}?apiKey={self.apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_controller_card_update_success(self) -> None:
        response = self.client.patch(f"{self.cardEndpoint}/{self.card.publicId}?apiKey={self.apiKey}", json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.card.cardType, self.data["cardType"])

    def test_controller_card_update_fail(self) -> None:
        # case: invalid api key
        response = self.client.patch(f"{self.cardEndpoint}/{self.card.publicId}?apiKey=invalid", json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no api key
        response = self.client.patch(f"{self.cardEndpoint}/{self.card.publicId}", json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: card does not exist
        response = self.client.patch(f"{self.cardEndpoint}/{400}?apiKey={self.apiKey}", json=self.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_controller_card_delete_success(self) -> None:
        response = self.client.delete(f"{self.cardEndpoint}/{self.card.publicId}?apiKey={self.apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_controller_card_delete_fail(self) -> None:
        # case: invalid api key
        response = self.client.delete(f"{self.cardEndpoint}/{self.card.publicId}?apiKey=invalid")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no api key
        response = self.client.delete(f"{self.cardEndpoint}/{self.card.publicId}")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: card does not exist
        response = self.client.delete(f"{self.cardEndpoint}/{400}?apiKey={self.apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_controller_card_extract_success(self) -> None:
        with open(self.file_path, "rb") as image:
            imageBytes = BytesIO(image.read())
        response = self.client.post(
            f"{self.cardExtractEndpoint}?apiKey={self.apiKey}",
            data={"image": (imageBytes, "test_image.jpg")},
            buffered=True,
            content_type="multipart/form-data",
            # data={"image": ("test_image.jpg", image, "image/jpeg")},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json["cardNumbers"]), 1)
        self.assertEqual(response.json["cardNumbers"][0], self.data["code"])

    def test_controller_card_extract_fail(self) -> None:
        # case: invalid api key
        response = self.client.post(f"{self.cardExtractEndpoint}?apiKey=invalid")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no api key
        response = self.client.post(f"{self.cardExtractEndpoint}")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        # case: no image
        response = self.client.post(f"{self.cardExtractEndpoint}?apiKey={self.apiKey}")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


if __name__ == "__main__":
    unittest.main()
