from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")


class BaseRepository(ABC):
    """A base repository class for handling database operations."""

    @abstractmethod
    def save(self, _model: T, update: bool = True) -> T:
        """
        Saves the given model to the database.

        Parameters:
            _model (Model): The model to be saved.

        Returns:
            Model: The saved model.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T:
        """
        Creates a new instance of the model with the specified arguments and saves it to the database.

        Args:
            *args (Tuple[Any, ...]): The positional arguments to pass to the model constructor.
            **kwargs (Dict[str, Any]): The keyword arguments to pass to the model constructor.

        Returns:
            Model: The newly created model instance.
        """
        raise NotImplementedError

    @abstractmethod
    def createAll(self, data: list[dict[str, Any]]) -> None:
        """
        Create multiple instances of the model with the specified arguments and saves them to the database.

        Args:
            data (List[Dict[str, Any]]): The list of dictionaries containing the arguments to pass to the model constructor.

        Returns:
            None
        """  # noqa: E501
        raise NotImplementedError

    @abstractmethod
    def filter(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T | None:
        """
        Find a record in the database based on the provided arguments.

        Args:
            *args (Tuple[Any, ...]): Positional arguments to filter the query.
            **kwargs (Dict[str, Any]): Keyword arguments to filter the query.

        Returns:
            Model | None: The first record that matches the filter, or None if no record is found.
        """
        raise NotImplementedError

    @abstractmethod
    def filterAll(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> list[T]:
        """
        Filter all instances of Model by the given arguments.

        Args:
            *args: Positional arguments passed to the filter method.
            **kwargs: Keyword arguments passed to the filter method.

        Returns:
            List of instances of Model that match the given arguments.
        """
        raise NotImplementedError

    @abstractmethod
    def filterAllByExpression(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> list[T]:
        """
        Filter all instances of Model by the given expression.

        Args:
            *args: Positional arguments passed to the filter method.
            **kwargs: Keyword arguments passed to the filter method.

        Returns:
            List of instances of Model that match the given expression.
        """
        raise NotImplementedError

    @abstractmethod
    def getAll(self) -> list[T]:
        """
        Returns all the elements in the model.
        :return: List of elements in the model.
        """
        raise NotImplementedError

    @abstractmethod
    def getById(self, id: int) -> T | None:
        """
        Retrieves an entity from the database by its ID.

        Parameters:
            id (int): The ID of the entity to retrieve.

        Returns:
            Model | None: The retrieved entity if found, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def getByPublicId(self, publicId: str) -> T | None:
        """
        Retrieves an entity from the database by its public ID.

        Parameters:
            publicId (str): The public ID of the entity to retrieve.

        Returns:
            Model | None: The retrieved entity if found, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def getOrCreate(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> tuple[T, bool]:
        """
        Get or create a new instance of the model.

        Args:
            *args (Tuple[Any, ...]): Variable length argument list for filtering the model.
            **kwargs (Dict[str, Any]): Keyword arguments for filtering the model.

        Returns:
            Tuple[Model, bool]: A tuple containing the model instance and a boolean indicating if it was created or not.
        """
        raise NotImplementedError

    @abstractmethod
    def getOr404(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T:
        """
        Get a model instance or raise a 404 error if not found.

        Args:
            *args: Positional arguments for filtering the query.
            **kwargs: Keyword arguments for filtering the query.

        Returns:
            Model: The retrieved model instance.

        Raises:
            NotFound: If the model instance is not found.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> bool:
        """
        Check if a model instance exists in the database.

        Args:
            *args: Positional arguments for filtering the query.
            **kwargs: Keyword arguments for filtering the query.

        Returns:
            bool: True if the model instance exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, _model: T) -> T:
        """
        Delete a model object from the database.

        Args:
            _model (Model): The model object to be deleted.

        Returns:
            Model: The deleted model object.
        """
        raise NotImplementedError

    @abstractmethod
    def deleteAll(self) -> None:
        """
        Delete all model objects from the database.

        Returns:
            None
        """
        raise NotImplementedError
