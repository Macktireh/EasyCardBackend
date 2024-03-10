from models.user import User
from repositories.baseRepositorySQLalchemy import BaseRepositorySQLalchemy


class UserRepository(BaseRepositorySQLalchemy):
    def __init__(self, model: User) -> None:
        super().__init__(model)

    def createSuperUser(self, *args, **kwargs) -> User:
        """
        Creates a super user with the given arguments.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The created super user.
        """
        return self.create(*args, **kwargs, isActive=True, isAdmin=True)


userRepository = UserRepository(model=User)
