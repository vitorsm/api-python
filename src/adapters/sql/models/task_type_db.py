from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.adapters.sql.models import Base
from src.adapters.sql.models.generic_entity_db import GenericEntityDB
from src.entities.task_type import TaskType


class TaskTypeDB(GenericEntityDB, Base[TaskType]):
    __tablename__ = "task_type"
    parent_type_id = Column(UUID, ForeignKey("task_type.id"), nullable=True)

    parent_type_db = relationship("TaskTypeDB", foreign_keys=[parent_type_id], remote_side="TaskTypeDB.id")

    def __init__(self, task_type: TaskType):
        super().__init__(task_type)
        self.update_attributes(task_type)

    def to_entity(self) -> TaskType:
        task_type = object.__new__(TaskType)
        task_type.parent_type = self.parent_type_db.to_entity() if self.parent_type_db else None

        self.fill_entity(task_type)
        return task_type

    def update_attributes(self, task_type: TaskType):
        super().update_attributes(task_type)
        self.parent_type_id = task_type.parent_type.id if task_type.parent_type else None
