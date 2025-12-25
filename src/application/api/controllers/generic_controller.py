import abc
from typing import TypeVar, Generic, Type, get_args

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_mapper import GenericMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.services.generic_service import GenericService

EntityService = TypeVar("EntityService", bound=GenericService)
EntityMapper = TypeVar("EntityMapper", bound=GenericMapper)


class GenericController(Generic[EntityService, EntityMapper], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_app_injector(self) -> Injector:
        raise NotImplementedError

    @abc.abstractmethod
    def get_controller(self) -> Blueprint:
        raise NotImplementedError

    @abc.abstractmethod
    def create_endpoints(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_controller_name(self) -> str:
        """This name will be used on the endpoint path. Prefer to use plural"""
        raise NotImplementedError

    def has_create_endpoint(self) -> bool:
        return True

    def instantiate_controller(self) -> Blueprint:
        controller_name = self.get_controller_name()
        return Blueprint(f"{controller_name}_controller", __name__, url_prefix=f"/api/{controller_name}")

    def start_controller(self):
        self.__register_endpoints()
        self.create_endpoints()

    def __register_endpoints(self):
        if self.has_create_endpoint():
            @self.get_controller().route("", methods=["POST"])
            @jwt_required()
            def create_entity():
                entity_dto = request.get_json()
                mapper = self._get_mapper_type()
                entity = mapper.to_entity(entity_dto)

                if not entity:
                    raise InvalidEntityException("", ["invalid entity"])

                entity_service = self._get_entity_service()
                entity_service.create(entity)

                return jsonify(mapper.to_dto(entity)), 201

        @self.get_controller().route("<string:entity_id>", methods=["PUT"])
        @jwt_required()
        def update_entity(entity_id: str):
            entity_dto = request.get_json()

            if entity_id != entity_dto.get("id"):
                raise InvalidEntityException("UUID", ["id"])

            mapper = self._get_mapper_type()
            entity = mapper.to_entity(entity_dto)

            if not entity:
                raise InvalidEntityException("", ["invalid entity"])

            entity_service = self._get_entity_service()
            entity_service.update(entity)

            return jsonify(mapper.to_dto(entity))

        @self.get_controller().route("<string:entity_id>")
        @jwt_required()
        def get_entity(entity_id: str):
            uuid_entity_id = uuid_mapper.to_uuid(entity_id)

            if not uuid_entity_id:
                raise InvalidEntityException("UUID", ["uuid"])

            entity_service = self._get_entity_service()
            entity = entity_service.find_by_id(uuid_entity_id)

            mapper = self._get_mapper_type()

            return jsonify(mapper.to_dto(entity))

        @self.get_controller().route("<string:entity_id>", methods=["DELETE"])
        @jwt_required()
        def delete_entity(entity_id: str):
            uuid_entity_id = uuid_mapper.to_uuid(entity_id)

            if not uuid_entity_id:
                raise InvalidEntityException("UUID", ["uuid"])

            entity_service = self._get_entity_service()
            # todo - change it to delete by id
            entity = entity_service.find_by_id(uuid_entity_id)

            entity_service.delete(entity)

            return '', 204

    def _get_entity_service(self) -> GenericService:
        entity_service_type = self.__get_service_type()
        return self.get_app_injector().get(entity_service_type)

    def __get_service_type(self) -> Type[EntityService]:
        return get_args(self.__orig_bases__[0])[0]

    def _get_mapper_type(self) -> Type[EntityMapper]:
        return get_args(self.__orig_bases__[0])[1]

