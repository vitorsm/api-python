from datetime import datetime

from sqlalchemy import Column, UUID, String, ForeignKey, DateTime
from sqlalchemy.orm import declared_attr, relationship

from src.entities.generic_entity import GenericEntity


class GenericEntityDB:
    @declared_attr
    def id(cls):
        return Column(UUID, primary_key=True)

    @declared_attr
    def name(cls):
        return Column(String(255), nullable=True)

    @declared_attr
    def workspace_id(cls):
        return Column(UUID, ForeignKey("workspace.id"))

    @declared_attr
    def created_at(cls):
        return Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True, default=None)

    @declared_attr
    def created_by(cls):
        return Column(UUID, ForeignKey("user.id"), nullable=False)

    @declared_attr
    def updated_by(cls):
        return Column(UUID, ForeignKey("user.id"), nullable=False)

    @declared_attr
    def workspace_db(cls):
        return relationship("WorkspaceDB", foreign_keys=[cls.workspace_id])

    @declared_attr
    def created_by_db(cls):
        return relationship("UserDB", foreign_keys=[cls.created_by], lazy="joined")

    @declared_attr
    def updated_by_db(cls):
        return relationship("UserDB", foreign_keys=[cls.updated_by], lazy="joined")

    def __init__(self, generic_entity: GenericEntity):
        self.__update_attributes(generic_entity)

    def update_attributes(self, generic_entity: GenericEntity):
        self.__update_attributes(generic_entity)

    def __update_attributes(self, generic_entity: GenericEntity):
        self.id = generic_entity.id
        self.name = generic_entity.name
        self.workspace_id = generic_entity.workspace.id
        self.created_at = generic_entity.created_at
        self.updated_at = generic_entity.updated_at
        self.deleted_at = generic_entity.deleted_at
        self.created_by = generic_entity.created_by.id
        self.updated_by = generic_entity.updated_by.id

    def fill_entity(self, entity: GenericEntity):
        entity.id = self.id
        entity.name = self.name
        entity.workspace = self.workspace_db.to_entity()
        entity.created_at = self.created_at
        entity.updated_at = self.updated_at
        entity.deleted_at = self.deleted_at
        entity.created_by = self.created_by_db.to_entity()
        entity.updated_by = self.updated_by_db.to_entity()