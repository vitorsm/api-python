import abc

from flask import request, jsonify
from flask_jwt_extended import jwt_required

from src.application.api.controllers.generic_controller import GenericController, EntityService, EntityMapper
from src.application.api.mappers import uuid_mapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException


class GenericEntityController(GenericController[EntityService, EntityMapper], metaclass=abc.ABCMeta):

    def create_endpoints(self):
        @self.get_controller().route("", methods=["GET"])
        @jwt_required()
        def find_all():
            workspace_id = uuid_mapper.to_uuid(request.args.get("workspace_id"))

            if not workspace_id:
                raise InvalidEntityException("UUID", ["workspace_id"])

            entity_service = self._get_entity_service()
            entities = entity_service.find_all(workspace_id)

            mapper = self._get_mapper_type()

            return jsonify(mapper.to_dto(entities))

        self.create_custom_endpoints()

    @abc.abstractmethod
    def create_custom_endpoints(self):
        raise NotImplementedError
