from src.adapters.sql import TaskTypeDB
from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.task_type import TaskType
from src.services.ports.task_type_repository import TaskTypeRepository


class SQLTaskTypeRepository(SQLRepository[TaskType, TaskTypeDB], TaskTypeRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
