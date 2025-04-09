from http import HTTPStatus
from random import randint

from cv2 import IMREAD_COLOR, imdecode
from cv2.typing import MatLike
from flask import request
from flask_injector import inject
from flask_restx import Resource, abort
from numpy import frombuffer, uint8

from middlewares.authMiddleware import api_key_required
from schemas.cardSchema import CardSchema
from services.cardNumberExtractorService import CardNumberExtractorService
from services.cardService import CardService

api = CardSchema.api


@api.route("")
@inject
class ListOrCreateCardController(Resource):
    def __init__(self, cardService: CardService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cardService = cardService

    @api.doc("List all registered cards")
    @api.response(HTTPStatus.OK, "Cards successfully listed")
    @api.marshal_list_with(CardSchema.card)
    @api_key_required
    def get(self):
        """List all registered cards"""
        return self.cardService.getCards()

    @api.doc("Create new card")
    @api.response(HTTPStatus.CREATED, "Card successfully created")
    @api.expect(CardSchema.cardIn, validate=True)
    @api.marshal_list_with(CardSchema.card)
    @api_key_required
    def post(self):
        """Create new card"""
        return self.cardService.createCard(api.payload), HTTPStatus.CREATED


@api.route("/all")
@inject
class CreateAllCardController(Resource):
    def __init__(self, cardService: CardService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cardService = cardService

    @api.doc("Create all new card")
    @api.response(HTTPStatus.CREATED, "all card successfully created")
    @api.expect(CardSchema.allCards, validate=True)
    @api_key_required
    def post(self):
        """Create all new card"""
        return self.cardService.createAllCards(api.payload["cards"]), HTTPStatus.CREATED


@api.route("/extract")
@inject
class ExtractCardNumberController(Resource):
    def __init__(self, cardNumberExtractorService: CardNumberExtractorService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cardNumberExtractorService = cardNumberExtractorService

    @api.doc("Extract card number")
    @api.response(HTTPStatus.OK, "Card number successfully extracted")
    @api.expect(CardSchema.imageParser, validate=True)
    @api.marshal_with(CardSchema.codes)
    @api_key_required
    def post(self) -> dict[str, str | list[str]]:
        """Extract card number"""
        image = self.getImage()
        try:
            cardNumbers = self.cardNumberExtractorService.getCardNumbers(image)
        except Exception:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="something went wrong")
        if not cardNumbers:
            abort(HTTPStatus.BAD_REQUEST, message="Failed to extract cards")
        return {"cardNumbers": cardNumbers}

    def getImage(self) -> MatLike:
        args = CardSchema.imageParser.parse_args()
        image_file = args["image"]
        contents = image_file.read()
        nparr = frombuffer(contents, uint8)
        return imdecode(nparr, IMREAD_COLOR)


@api.route("/extract/fake")
class FakeExtractCardNumberController(Resource):
    @api.doc("Fake Extract card number")
    @api.response(HTTPStatus.OK, "Card number successfully extracted")
    @api.expect(CardSchema.imageParser, validate=True)
    @api.marshal_with(CardSchema.codes)
    @api_key_required
    def post(self) -> dict[str, str | list[str]]:
        """Fake Extract card number"""
        n = request.args.get("n", type=int, default=randint(1, 10))
        cardNumbers = [randint(100000000000, 999999999999) for _ in range(n)]
        return {"cardNumbers": list(set(cardNumbers))}


@api.route("/<string:publicId>")
@inject
class CardController(Resource):
    def __init__(self, cardService: CardService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cardService = cardService

    @api.doc("Get card by id")
    @api.response(HTTPStatus.OK, "Card successfully retrieved")
    @api.marshal_with(CardSchema.card)
    @api_key_required
    def get(self, publicId: str):
        """Get card by publicId"""
        return self.cardService.getCard(publicId)

    @api.doc("Update card")
    @api.response(HTTPStatus.OK, "Card successfully updated")
    @api.expect(CardSchema.cardIn)
    @api.marshal_with(CardSchema.card)
    @api_key_required
    def patch(self, publicId: str):
        """Update card"""
        return self.cardService.updateCard(publicId, api.payload)

    @api.doc("Delete card")
    @api.response(HTTPStatus.NO_CONTENT, "Card successfully deleted")
    @api_key_required
    def delete(self, publicId: str):
        """Delete card"""
        return self.cardService.deleteCard(publicId), HTTPStatus.NO_CONTENT
