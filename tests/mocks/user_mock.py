import random
from datetime import datetime
from uuid import uuid4

from src.entities.user import User
from tests.mocks import FIRST_DEFAULT_ID


def get_valid_user() -> User:
    return User(id=uuid4(), name="User1", login=f"user{int(random.random() * 1000)}", password="pass",
                updated_at=datetime.now())


def get_default_user() -> User:
    return User(id=FIRST_DEFAULT_ID, name="User 1", login="user1", password="12345", updated_at=datetime.now())
