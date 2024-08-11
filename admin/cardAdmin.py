from flask_admin.contrib.sqla import ModelView


class CardAdmin(ModelView):
    column_list: list[str] = [
        "id",
        "publicId",
        "code",
        "cardType",
        "isValid",
        "createdAt",
        "updatedAt",
    ]
    column_hide_backrefs = False
    column_searchable_list: list[str] = ["code"]
    column_filters: list[str] = ["cardType", "isValid"]
    column_sortable_list: list[str] = ["id", "createdAt", "updatedAt"]
    column_editable_list: list[str] = [
        "code",
        "cardType",
        "isValid",
    ]
    form_create_rules: list[str] = [
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
