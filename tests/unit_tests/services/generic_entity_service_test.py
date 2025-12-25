import abc
from unittest.mock import Mock

from tests.mocks import workspace_mock
from tests.unit_tests.services.generic_service_test import GenericServiceTest


class GenericEntityServiceTest(GenericServiceTest, metaclass=abc.ABCMeta):

    def setUp(self):
        super().setUp()

        self.get_workspace_service().find_by_id.return_value = workspace_mock.get_default_workspace()

    @abc.abstractmethod
    def get_workspace_service(self) -> Mock:
        raise NotImplementedError
