import abc

from sqlalchemy.orm import Session


class DBInstance(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_session(self) -> Session:
        raise NotImplementedError
