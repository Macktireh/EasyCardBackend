from typing import Any, Dict, List, Tuple, TypeVar

from werkzeug import exceptions

from config.app import db
from repositories import BaseRepository

Model = TypeVar("Model")


class BaseRepositorySQLalchemy(BaseRepository):
    def __init__(self, model: Model) -> None:
        self.model = model

    def save(self, _model: Model, update: bool = True) -> Model:
        db.session.commit()
        return _model

    def create(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Model:
        _model = self.model(*args, **kwargs)
        db.session.add(_model)
        return self.save(_model, False)

    def filter(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Model | None:
        return self.model.query.filter_by(*args, **kwargs).first()

    def filterAll(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> List[Model]:
        return self.model.query.filter_by(*args, **kwargs).all()

    def filterAllByExpression(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> List[Model]:
        return self.model.query.filter(*args, **kwargs).all()

    def getAll(self) -> List[Model]:
        return self.model.query.all()

    def getById(self, id: int) -> Model | None:
        return self.filter(id=id)

    def getByPublicId(self, publicId: str) -> Model | None:
        return self.filter(publicId=publicId)

    def getOrCreate(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Tuple[Model, bool]:
        if model := self.filter(*args, **kwargs):
            return model, False
        return self.create(*args, **kwargs), True

    def getOr404(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Model:
        if not (model := self.filter(*args, **kwargs)):
            raise exceptions.NotFound(f"{self.model.__name__} not found")
        return model

    def exists(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> bool:
        return self.filter(*args, **kwargs) is not None

    def delete(self, _model: Model) -> Model:
        db.session.delete(_model)
        db.session.commit()
        return _model
