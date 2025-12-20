import abc
from typing import Optional

from src.entities.user import User
from src.services.ports.generic_repository import GenericRepository


class UserRepository(GenericRepository[User], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_by_login(self, login: str) -> Optional[User]:
        raise NotImplementedError
