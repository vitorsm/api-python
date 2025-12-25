import abc
from typing import Any, List

from src.entities.generic_entity import GenericEntity
from src.services.ports.generic_entity_repository import GenericEntityRepository
from tests.integration_tests.adapters.sql.generic_repository_test import GenericRepositoryTest
from tests.mocks import FIRST_DEFAULT_ID


class GenericEntityRepositoryTest(GenericRepositoryTest, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def compare_entities_custom(self, entity1: GenericEntity, entity2: GenericEntity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_repository(self) -> GenericEntityRepository:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_entities(self) -> List[GenericEntity]:
        raise NotImplementedError

    def compare_entities(self, entity1: GenericEntity, entity2: GenericEntity):
        self.assertEqual(entity1.id, entity2.id)
        self.assertEqual(entity1.name, entity2.name)
        self.assertEqual(entity1.workspace, entity2.workspace)
        self.assertEqual(entity1.created_at, entity2.created_at)
        self.assertEqual(entity1.updated_at, entity2.updated_at)
        self.assertEqual(entity1.deleted_at, entity2.deleted_at)
        self.assertEqual(entity1.created_by, entity2.created_by)
        self.assertEqual(entity1.updated_by, entity2.updated_by)

        self.compare_entities_custom(entity1, entity2)

    def test_find_all(self):
        # given
        workspace_id = FIRST_DEFAULT_ID

        # when
        persisted_entities = self.get_repository().find_all(workspace_id)

        # then

        all_entities = self.get_all_entities()
        for entity, persisted_entity in zip(all_entities, persisted_entities):
            self.compare_entities(entity, persisted_entity)
