import random
from datetime import datetime
from typing import List
from uuid import uuid4, UUID

from src.entities.user import User
from src.entities.workspace import Workspace
from tests.mocks import user_mock, FIRST_DEFAULT_ID, DEFAULT_CREATED_AT, DEFAULT_UPDATED_AT

now = datetime.now()


def get_valid_workspace(wid: UUID = None, name: str = None, created_at: datetime = DEFAULT_CREATED_AT,
                        updated_at: datetime = DEFAULT_UPDATED_AT, created_by: User = user_mock.get_valid_user(),
                        updated_by: User = user_mock.get_valid_user(), user_ids: List[UUID] = None,
                        deleted_at: datetime = None) -> Workspace:
    if not name:
        name = f"workspace {int(random.random() * 1000)}"

    wid = wid if wid is not None else uuid4()
    user_ids = user_ids if user_ids is not None else []

    return Workspace(id=wid, name=name, created_at=created_at, updated_at=updated_at,
                     created_by=created_by, updated_by=updated_by,
                     users_ids=user_ids, deleted_at=deleted_at)


def get_default_workspace() -> Workspace:
    return get_valid_workspace(wid=FIRST_DEFAULT_ID, name="Workspace 1",
                               created_by=user_mock.get_default_user(), updated_by=user_mock.get_default_user(),
                               created_at=DEFAULT_CREATED_AT, updated_at=DEFAULT_UPDATED_AT,
                               user_ids=[FIRST_DEFAULT_ID])