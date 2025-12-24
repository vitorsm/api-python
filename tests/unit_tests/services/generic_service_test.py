import abc
from typing import Any
from unittest.mock import Mock

from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.permission_exception import PermissionException
from src.services.generic_service import GenericService
from tests.mocks import user_mock


class GenericServiceTest(metaclass=abc.ABCMeta):

    def setUp(self):
        self.default_user = user_mock.get_default_user()
        self.get_authentication_repository().get_current_user.return_value = self.default_user
        self.user_without_permission = user_mock.get_valid_user()
        self.get_repository().find_by_id.return_value = self.get_default_entity()

    @abc.abstractmethod
    def get_default_entity(self) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def get_service(self) -> GenericService:
        raise NotImplementedError

    @abc.abstractmethod
    def get_repository(self) -> Mock:
        raise NotImplementedError

    @abc.abstractmethod
    def get_authentication_repository(self) -> Mock:
        raise NotImplementedError

    def test_create_entity(self):
        # given
        entity = self.get_default_entity()
        original_entity_id = entity.id

        # when
        self.get_service().create(entity)

        # then
        self.assertNotEqual(original_entity_id, entity.id)
        self.assertIsNotNone(entity.id)
        self.get_repository().create.assert_called_once_with(entity)

    def test_update_entity(self):
        # given
        updated_entity = self.get_default_entity()
        updated_entity.name = "new name"

        # when
        self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_called_once_with(updated_entity)

    def test_update_entity_without_permission(self):
        # given
        updated_entity = self.get_default_entity()
        updated_entity.name = "new name"
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when
        with self.assertRaises(PermissionException) as ex:
            self.get_service().update(updated_entity)

        # then
        self.get_repository().update.assert_not_called()
        self.assertIn(self.user_without_permission.login, str(ex.exception))

    def test_update_entity_not_found(self):
        # given
        updated_entity = self.get_default_entity()
        updated_entity.name = "new name"

        self.get_repository().find_by_id.return_value = None

        # when
        with self.assertRaises(EntityNotFoundException) as ex:
            self.get_service().update(updated_entity)

        self.assertIn(str(updated_entity.id), str(ex.exception))

    def test_find_by_id(self):
        # given
        mock_entity = self.get_default_entity()
        entity_id = mock_entity.id
        self.get_repository().find_by_id.return_value = mock_entity

        # when
        entity = self.get_service().find_by_id(entity_id)

        # then
        self.assertEqual(mock_entity, entity)

    def test_find_by_id_without_permission(self):
        # given
        entity_id = self.get_default_entity().id
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.get_service().find_by_id(entity_id)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

    def test_find_by_id_not_found(self):
        # given
        mock_entity = self.get_default_entity()
        entity_id = mock_entity.id
        self.get_repository().find_by_id.return_value = None

        # when
        with self.assertRaises(EntityNotFoundException) as ex:
            self.get_service().find_by_id(entity_id)

        # then
        self.assertIn(str(entity_id), str(ex.exception))

    def test_delete_entity(self):
        # given
        entity = self.get_default_entity()
        original_updated_at = entity.updated_at


        # when
        self.get_service().delete(entity)

        # then
        self.get_repository().update.assert_called_with(entity)

        self.assertNotEqual(    original_updated_at, entity.updated_at)
        self.assertIsNotNone(entity.deleted_at)

    def test_hard_delete_entity(self):
        # given
        entity = self.get_default_entity()

        # when
        self.get_service().delete(entity, is_hard_delete=True)

        # then
        self.get_repository().delete.assert_called_with(entity)

    def test_delete_entity_not_found(self):
        # given
        entity = self.get_default_entity()
        self.get_repository().find_by_id.return_value = None

        # when/then
        with self.assertRaises(EntityNotFoundException) as ex:
            self.get_service().delete(entity)

        self.assertIn(str(entity.id), str(ex.exception))

    def test_delete_without_permission(self):
        # given
        entity = self.get_default_entity()
        self.get_authentication_repository().get_current_user.return_value = self.user_without_permission

        # when/then
        with self.assertRaises(PermissionException) as ex:
            self.get_service().delete(entity)

        self.assertIn(str(self.user_without_permission.id), str(ex.exception))

