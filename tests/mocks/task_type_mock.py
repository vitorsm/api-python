import random
from datetime import datetime
from uuid import UUID, uuid4

from src.entities.task_type import TaskType
from tests.mocks import workspace_mock, user_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT

now = datetime.now()


def get_valid_task_type(tid: UUID = None, name: str = None, workspace=workspace_mock.get_valid_workspace(),
                          created_by=user_mock.get_valid_user(), updated_by=user_mock.get_valid_user(),
                          created_at: datetime = now, updated_at: datetime = now, deleted_at: datetime = None,
                          parent_type: TaskType = None) -> TaskType:
    id = tid if tid else uuid4()
    if not name:
        name = f"Task type {int(random.random() * 1000)}"

    return TaskType(id=id, name=name, workspace=workspace, created_by=created_by, updated_by=updated_by,
                    created_at=created_at, updated_at=updated_at, deleted_at=deleted_at, parent_type=parent_type)


def get_default_task_type() -> TaskType:
    return get_valid_task_type(tid=FIRST_DEFAULT_ID, name="Type 1", workspace=workspace_mock.get_default_workspace(),
                               created_by=user_mock.get_default_user(), updated_by=user_mock.get_default_user(),
                               created_at=DEFAULT_CREATED_AT, updated_at=DEFAULT_UPDATED_AT)
