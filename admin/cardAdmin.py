from typing import List

from flask_admin.contrib.sqla import ModelView


class CardAdmin(ModelView):
    column_list: List[str] = [
        "id",
        "publicId",
        "code",
        "cardType",
        "isValid",
        "createdAt",
        "updatedAt",
    ]
    column_hide_backrefs = False
    column_searchable_list: List[str] = ["code"]
    column_filters: List[str] = ["cardType", "isValid"]
    column_sortable_list: List[str] = ["id", "createdAt", "updatedAt"]
    column_editable_list: List[str] = [
        "code",
        "cardType",
        "isValid",
    ]
    form_create_rules: List[str] = [
        "code",
        "cardType",
        "isValid",
    ]

    form_excluded_columns = ["id", "publicId", "createdAt", "updatedAt"]

    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 15
