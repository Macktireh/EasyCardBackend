from http import HTTPStatus
from typing import List

from cv2 import IMREAD_COLOR, imdecode
from cv2.typing import MatLike
from flask_injector import inject
from flask_restx import Resource, abort
from numpy import frombuffer, uint8

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
    @api.marshal_list_with(CardSchema.card, envelope="data")
    def get(self):
        """List all registered cards"""
        return self.cardService.getCards()

    @api.doc("Create new card")
    @api.expect(CardSchema.cardIn)
    @api.marshal_list_with(CardSchema.card)
    def post(self):
        """Create new card"""
        print(api.payload)
        return self.cardService.createCard(api.payload)


@api.route("/extract")
@inject
class ExtractCardNumberController(Resource):
    def __init__(self, cardNumberExtractorService: CardNumberExtractorService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cardNumberExtractorService = cardNumberExtractorService

    @api.doc("Extract card number")
    @api.expect(CardSchema.imageParser)
    def post(self) -> dict[str, str | List[str]]:
        """Extract card number"""
        image = self.getImage()
        try:
            cardNumbers = self.cardNumberExtractorService.getCardNumbers(image)
        except Exception:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="something went wrong")
        if not cardNumbers:
            abort(HTTPStatus.BAD_REQUEST, message="card number extraction failed")
        return {"cardNumbers": cardNumbers, "message": "card number extracted successfully"}

    def getImage(self) -> MatLike:
        args = CardSchema.imageParser.parse_args()
        image_file = args["image"]
        contents = image_file.read()
        nparr = frombuffer(contents, uint8)
        return imdecode(nparr, IMREAD_COLOR)
