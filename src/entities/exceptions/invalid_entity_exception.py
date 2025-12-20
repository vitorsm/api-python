from typing import List


class InvalidEntityException(Exception):

    def __init__(self, entity_type: str, missing_fields: List[str]):
        super().__init__(f"Invalid {entity_type} entity. Missing or invalid fields: {', '.join(missing_fields)}")
        self.entity_type = entity_type
        self.invalid_fields = missing_fields
