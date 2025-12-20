from src.entities.exceptions.invalid_entity_exception import InvalidEntityException


class DuplicateEntityException(InvalidEntityException):

    def __init__(self, entity_type: str, duplicate_field: str):
        super().__init__(entity_type, [duplicate_field])
