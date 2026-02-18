from datetime import datetime

from sqlalchemy import Column, UUID, String, DateTime, Text

from src.adapters.sql.models import Base
from src.entities.user import User


class UserDB(Base[User]):
    __tablename__ = "user"
    id = Column(UUID, primary_key=True)
    name = Column(Text, nullable=False)
    login = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    photo = Column(String(255), nullable=True, unique=False)
    password = Column(Text, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, default=None)

    def __init__(self, user: User):
        self.update_attributes(user)

    def update_attributes(self, user: User):
        self.id = user.id
        self.name = user.name
        self.login = user.login
        self.password = user.password
        self.updated_at = user.updated_at
        self.deleted_at = user.deleted_at
        self.photo = user.photo
        self.email = user.email

    def to_entity(self) -> User:
        return User(id=self.id, name=self.name, login=self.login, password=self.password, updated_at=self.updated_at,
                    deleted_at=self.deleted_at, email=self.email, photo=self.photo)
