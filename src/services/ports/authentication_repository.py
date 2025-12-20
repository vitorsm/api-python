import abc

from src.entities.user import User


class AuthenticationRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_current_user(self) -> User:
        raise NotImplementedError
