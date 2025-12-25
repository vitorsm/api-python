from typing import Optional

from src.application.api.mappers.generic_mapper import GenericMapper, register_new_mapper
from src.entities.user import User


class UserMapper(GenericMapper[User]):

    @classmethod
    def to_dto(cls, user: Optional[User]) -> Optional[dict]:
        dto = super().to_dto(user)
        if dto:
            dto["password"] = None
        return dto


register_new_mapper(UserMapper)
