from http import HTTPStatus
from typing import List

from flask import Blueprint

from src.application.api.errors.api_error import APIError
from src.application.api.errors.error_code import ErrorCode
from src.entities.exceptions.authentication_exception import AuthenticationException
from src.entities.exceptions.duplicate_entity_exception import DuplicateEntityException
from src.entities.exceptions.entity_not_found_exception import EntityNotFoundException
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.exceptions.permission_exception import PermissionException


def error_handlers(controllers: List[Blueprint]):
    for controller in controllers:
        @controller.errorhandler(AuthenticationException)
        def handle_authentication_exception(error: AuthenticationException):
            error = APIError(ErrorCode.CREDENTIALS_ERROR, "Invalid credentials", None,
                             HTTPStatus.UNAUTHORIZED)
            return error.to_api()

        @controller.errorhandler(DuplicateEntityException)
        def handle_duplicate_data_exception(error: DuplicateEntityException):
            invalid_fields = ", ".join(error.invalid_fields)
            details = f"{error.entity_type} - {invalid_fields}"
            error = APIError(ErrorCode.DUPLICATE_ENTITY, "Duplicate data", details,
                             HTTPStatus.BAD_REQUEST)
            return error.to_api()

        @controller.errorhandler(InvalidEntityException)
        def handle_data_validation_exception(error: InvalidEntityException):
            invalid_fields = ", ".join(error.invalid_fields)
            details = f"{error.entity_type} - {invalid_fields}"
            error = APIError(ErrorCode.VALIDATION_ERROR, "Invalid input", details,
                             HTTPStatus.BAD_REQUEST)
            return error.to_api()

        @controller.errorhandler(PermissionException)
        def handle_data_validation_exception(error: PermissionException):
            details = str(error)
            error = APIError(ErrorCode.PERMISSION_ERROR, "Permission error", details,
                             HTTPStatus.FORBIDDEN)
            return error.to_api()

        @controller.errorhandler(EntityNotFoundException)
        def handle_not_found_exception(error: EntityNotFoundException):
            details = str(error)
            error = APIError(ErrorCode.ENTITY_NOT_FOUND, "Entity not found", details,
                             HTTPStatus.NOT_FOUND)
            return error.to_api()
