from sqlalchemy.exc import IntegrityError

from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.user_db import UserDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.exceptions.duplicate_entity_exception import DuplicateEntityException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.user import User
from src.services.ports.user_repository import UserRepository


class SQLUserRepository(SQLRepository[User, UserDB], UserRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def create(self, user: User):
        try:
            super().create(user)
        except IntegrityError as ex:
            raise DuplicateEntityException("User", "login")

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance

    def find_by_login(self, login: str) -> User:
        session = self.get_session()
        user_db = session.query(UserDB).filter(UserDB.login == login).first()
        return user_db.to_entity() if user_db else None
