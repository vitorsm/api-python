from src.adapters.sql.db_instance import DBInstance
from src.adapters.sql.models.workspace_db import WorkspaceDB
from src.adapters.sql.sql_repository import SQLRepository
from src.entities.workspace import Workspace
from src.services.ports.workspace_repository import WorkspaceRepository


class SQLWorkspaceRepository(SQLRepository[Workspace, WorkspaceDB], WorkspaceRepository):

    def __init__(self, db_instance: DBInstance):
        self.__db_instance = db_instance

    def get_db_instance(self) -> DBInstance:
        return self.__db_instance
