from flask_injector import inject
from flask_restx import Resource

from schemas.cardSchema import CardSchema
from services.cardService import CardService

api = CardSchema.api


# @api.route("/me")
# class RetrieveUpdateCardController(Resource):

#     def __init__(self, cardService: CardService, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.cardService = cardService

#     # @api.doc("Get Current Card")
#     # @api.marshal_list_with(CardSchema.card, envelope="data")
#     # def get(self):
#     #     """Get Current Card"""
#     #     return self.cardService

#     # @api.doc("Update Current Card")
#     # @api.marshal_list_with(CardSchema.card, envelope="data")
#     # def patch(self):
#     #     """Update Current Card"""
#     #     return self.cardService


@api.route("")
@inject
class ListOrCreateCardController(Resource):

    def __init__(self, cardService: CardService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cardService = cardService

    @api.doc("List all registered cards")
    @api.marshal_list_with(CardSchema.card, envelope="data")
    def get(self):
        """List all registered cards"""
        return self.cardService.getCards()
    
    @api.doc("Create new card")
    @api.expect(CardSchema.createCard)
    @api.marshal_list_with(CardSchema.card)
    def post(self):
        """Create new card"""
        print(api.payload)
        # return self.cardService.createCard(api.payload)
