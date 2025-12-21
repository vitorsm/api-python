import abc
from typing import Any

from src.services.ports.generic_repository import GenericRepository
from tests.mocks import FIRST_DEFAULT_ID, SECOND_DEFAULT_ID


class GenericRepositoryTest(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_valid_entity(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_default_entity(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_updated_entity(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_repository(self) -> GenericRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def compare_entities(self, entity1: Any, entity2: Any):
        raise NotImplementedError

    def test_create_entity(self):
        # given
        entity = self.get_valid_entity()

        # when
        self.get_repository().create(entity)

        # then
        persisted_entity = self.get_repository().find_by_id(entity.id)
        self.compare_entities(entity, persisted_entity)

    def test_update_entity(self):
        # given
        entity = self.get_updated_entity()

        # when
        self.get_repository().update(entity)

        # then
        persisted_entity = self.get_repository().find_by_id(entity.id)
        self.compare_entities(entity, persisted_entity)

    def test_find_by_id(self):
        # given
        entity_id = FIRST_DEFAULT_ID

        # when
        entity = self.get_repository().find_by_id(entity_id)

        # then
        self.assertIsNotNone(entity)
        self.compare_entities(self.get_default_entity(), entity)

    def test_delete_user(self):
        # given
        entity_id = SECOND_DEFAULT_ID
        entity = self.get_valid_entity()
        entity.id = entity_id

        # when
        self.get_repository().delete(entity)

        # then
        persisted_entity = self.get_repository().find_by_id(entity_id)
        self.assertIsNone(persisted_entity)
