import abc
from typing import Optional

from src.entities.user import User


class OpenIdRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_user_from_code_open_id(self, code: str, client_id: str) -> Optional[User]:
        raise NotImplementedError
