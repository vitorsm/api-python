import abc
from uuid import UUID


class AuthStateRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_user_state(self) -> UUID:
        raise NotImplementedError

    @abc.abstractmethod
    def check_user_state(self, user_state: UUID):
        raise NotImplementedError
