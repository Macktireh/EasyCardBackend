from flask_restx import Namespace, fields


class CardSchema:
    api = Namespace("Card", description="card related operations")

    createCard = api.model(
        name="createCard",
        model={
            "code": fields.String(
                required=True, description="secret code", max_length=12, min_length=12, example="123456789123"
            ),
            "type": fields.String(
                required=True, description="type of card", enum=["500", "1000", "2000", "5000", "10000"], example="1000"
            ),
        },
        strict=False,
    )

    card = api.model(
        name="card",
        model={
            "id": fields.Integer(description="id of the card", readonly=True, example=1),
            "code": fields.String(
                required=True, description="secret code", max_length=12, min_length=12, example="123456789123"
            ),
            "type": fields.String(
                required=True, description="type of card", enum=["500", "1000", "2000", "5000", "10000"], example="1000"
            ),
            "isValid": fields.Boolean(description="if the card is valid", example=True),
            "createdAt": fields.DateTime(description="date of the card creation", readonly=True),
            "updatedAt": fields.DateTime(description="date of the card update", readonly=True),
        },
    )
