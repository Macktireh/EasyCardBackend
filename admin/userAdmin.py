from typing import Dict, List

from flask_admin.contrib.sqla import ModelView
from flask_admin.helpers import get_form_data
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Regexp

from repositories.userRepository import userRepository
from validators.authValidator import MESSAGE_PASSWORD_INVALID, REGEX_PASSWORD_VALIDATION


class UserAdmin(ModelView):
    column_searchable_list: List[str] = ["name", "email"]
    column_filters: List[str] = ["isActive", "isAdmin"]
    column_editable_list: List[str] = [
        "name",
        "isActive",
        "isAdmin",
    ]
    column_sortable_list: List[str] = ["createdAt", "updatedAt"]
    column_exclude_list: List[str] = ["passwordHash"]
    column_details_exclude_list: List[str] = ["passwordHash"]
    column_export_exclude_list: List[str] = ["passwordHash"]

    form_create_rules: List[str] = [
        "name",
        "email",
        "password",
        "passwordConfirm",
        "isActive",
    ]
    form_edit_rules: List[str] = [
        "name",
        "isActive",
        "isAdmin",
    ]

    create_modal: bool = True
    edit_modal: bool = True
    can_export: bool = True
    can_view_details: bool = True
    page_size: int = 50

    form_extra_fields: Dict[str, PasswordField] = {
        "password": PasswordField(
            "Password",
            [
                DataRequired(),
                Regexp(REGEX_PASSWORD_VALIDATION, message=MESSAGE_PASSWORD_INVALID),
            ],
        ),
        "passwordConfirm": PasswordField(
            "Password Confirm",
            [
                DataRequired(),
                EqualTo("password", message="Passwords must match"),
            ],
        ),
    }

    def create_model(self, form):
        form_data = get_form_data()
        data = {
            "email": form_data.get("email"),
            "name": form_data.get("name"),
            "password": form_data.get("password"),
            "isActive": bool(form_data.get("isActive")),
        }
        return userRepository.create(**data)