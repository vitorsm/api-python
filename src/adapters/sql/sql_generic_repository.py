import abc
from src.adapters.sql.sql_repository import SQLRepository
from src.services.ports.generic_repository import GenericRepository


class SQLGenericRepository(SQLRepository, metaclass=abc.ABCMeta):
    pass