from abc import ABCMeta

from src.services.ports.generic_repository import GenericRepository


class WorkspaceRepository(GenericRepository, metaclass=ABCMeta):
    pass
