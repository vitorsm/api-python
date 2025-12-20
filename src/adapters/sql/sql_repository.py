import abc
from typing import TypeVar, Generic, Optional, Type, get_args
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.adapters.sql.db_instance import DBInstance

Entity = TypeVar("Entity")
DBModel = TypeVar("DBModel")


class SQLRepository(Generic[Entity, DBModel], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_db_instance(self) -> DBInstance:
        raise NotImplementedError

    def get_session(self) -> Session:
        return self.get_db_instance().get_session()

    def create(self, entity: Entity):
        model_db_type = self.__get_db_model_type()
        entity_db = model_db_type(entity)
        session = self.get_session()
        session.add(entity_db)
        session.commit()

    def update(self, entity: Entity):
        session = self.get_session()
        entity_db = session.get_one(self.__get_db_model_type(), entity.id)
        entity_db.update_attributes(entity)
        session.commit()

    def delete(self, entity: Entity):
        session = self.get_session()
        entity_db = session.get_one(self.__get_db_model_type(), entity.id)
        session.delete(entity_db)
        session.commit()

    def find_by_id(self, entity_id: UUID) -> Optional[Entity]:
        session = self.get_session()
        model_type = self.__get_db_model_type()

        try:
            entity_db = session.get_one(model_type, entity_id)
        except NoResultFound:
            return None

        # put it in the query
        if hasattr(entity_db, "deleted_at") and entity_db.deleted_at is not None:
            return None

        return entity_db.to_entity()

    def __get_entity_type(self) -> Type[Entity]:
        return get_args(self.__orig_bases__[0])[0]

    def __get_db_model_type(self) -> Type[DBModel]:
        return get_args(self.__orig_bases__[0])[1]
