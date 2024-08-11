from typing import Any, Generic, TypeVar

from werkzeug import exceptions

from config.app import db
from repositories import BaseRepository

T = TypeVar("T")


class BaseRepositorySQLAlchemy(BaseRepository, Generic[T]):
    def __init__(self, model: type[T]) -> None:
        self.model = model

    def save(self, _model: T) -> T:
        db.session.commit()
        return _model

    def create(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T:
        _model = self.model(*args, **kwargs)
        db.session.add(_model)
        return self.save(_model)

    def createAll(self, data: list[dict[str, Any]]) -> None:
        db.session.bulk_insert_mappings(self.model, data)
        db.session.commit()

    def filter(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T | None:
        return self.model.query.filter_by(*args, **kwargs).first()

    def filterAll(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> list[T]:
        return self.model.query.filter_by(*args, **kwargs).all()

    def filterAllByExpression(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> list[T]:
        return self.model.query.filter(*args, **kwargs).all()

    def getAll(self) -> list[T]:
        return self.model.query.all()

    def getById(self, id: int) -> T | None:
        return self.filter(id=id)

    def getByPublicId(self, publicId: str) -> T | None:
        return self.filter(publicId=publicId)

    def getOrCreate(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> tuple[T, bool]:
        if model := self.filter(*args, **kwargs):
            return model, False
        return self.create(*args, **kwargs), True

    def getOr404(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T:
        if not (model := self.filter(*args, **kwargs)):
            raise exceptions.NotFound(f"{self.model.__name__} not found")
        return model

    def exists(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> bool:
        return self.filter(*args, **kwargs) is not None

    def delete(self, _model: T) -> T:
        db.session.delete(_model)
        db.session.commit()
        return _model

    def deleteAll(self) -> None:
        try:
            db.session.query(self.model).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()
