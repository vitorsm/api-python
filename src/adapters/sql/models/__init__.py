import abc
from typing import TypeVar, Generic

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

SQLBase = declarative_base()


Entity = TypeVar("Entity")


class BaseMeta(abc.ABCMeta, DeclarativeMeta):
    pass


class Base(SQLBase, Generic[Entity], metaclass=BaseMeta):
    __abstract__ = True

    @abc.abstractmethod
    def to_entity(self) -> Entity:
        raise NotImplementedError

    @abc.abstractmethod
    def update_attributes(self, entity: Entity):
        raise NotImplementedError
