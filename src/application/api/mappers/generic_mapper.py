from dataclasses import fields, Field, is_dataclass
from datetime import datetime
from enum import Enum, StrEnum
from typing import Generic, TypeVar, Optional, Type, get_args, List, Any, get_origin, Union, Callable, Dict
from uuid import UUID

from src.application.api.mappers import uuid_mapper
from src.utils import date_utils, enum_utils


PRIMITIVE_TYPES = (int, float, bool, str, bytes)


Entity = TypeVar("Entity")

TO_ENTITY_CONVERTERS = {
    UUID: lambda str_uuid: uuid_mapper.to_uuid(str_uuid),
    datetime: lambda str_datetime: date_utils.iso_to_datetime(str_datetime)
}

TO_DTO_CONVERTERS = {
    UUID: lambda entity_uuid: str(entity_uuid),
    datetime: lambda entity_datetime: date_utils.datetime_to_iso(entity_datetime)
}


def register_new_mapper(mapper: Type['GenericMapper']):
    TO_ENTITY_CONVERTERS[mapper._get_entity_type()] = lambda dto: mapper.to_entity(dto)
    TO_DTO_CONVERTERS[mapper._get_entity_type()] = lambda entity: mapper.to_dto(entity)


class GenericMapper(Generic[Entity]):

    @classmethod
    def get_dto_converters(cls) -> Dict[Type, Callable]:
        return {}

    @classmethod
    def to_entity(cls, dto: dict) -> Optional[Entity]:
        entity_type = cls._get_entity_type()
        result = cls.__to_entity(dto, entity_type)

        if result:
            result.__post_init__()

        return result

    @classmethod
    def to_dto(cls, entity: Entity) -> Union[Optional[dict], List[dict]]:
        if isinstance(entity, (list, set, tuple)):
            return [cls.to_dto(single_entity) for single_entity in entity]

        if not entity:
            return None

        attributes = GenericMapper.__get_entity_attributes(entity)

        result = {}
        for key, value in attributes.items():
            result[key] = cls.__convert_to_dict_attribute(value)

        return result

    @classmethod
    def __convert_to_dict_attribute(cls, attribute_value: Any) -> Optional[Any]:
        if not attribute_value:
            return attribute_value

        attribute_type = type(attribute_value)

        if attribute_type in PRIMITIVE_TYPES:
            return attribute_value

        if attribute_type is list or attribute_type is tuple or attribute_type is set:
            result = []
            for list_item in attribute_value:
                result.append(cls.__convert_to_dict_attribute(list_item))
            return result

        if attribute_type in TO_DTO_CONVERTERS:
            return TO_DTO_CONVERTERS[attribute_type](attribute_value)

        if attribute_type in cls.get_dto_converters():
            return cls.get_dto_converters()[attribute_type](attribute_value)

        if is_dataclass(attribute_type):
            return cls.to_dto(attribute_value)

        if GenericMapper.__is_enum_type(attribute_type):
            return attribute_value.name

        return None

    @staticmethod
    def __get_entity_attributes(entity: Entity) -> dict:
        return entity.__dict__

    @classmethod
    def __to_entity(cls, dto: dict, entity_type: Type):
        if not dto:
            return None

        attributes = GenericMapper.__get_class_attributes(entity_type)

        result = object.__new__(entity_type)

        for attribute in attributes:
            attribute_type = GenericMapper.__get_field_type(attribute)
            setattr(result, attribute.name, cls.__convert_to_entity_attribute(attribute_type, dto.get(attribute.name)))

        return result

    @classmethod
    def __convert_to_entity_attribute(cls, attribute_type: Type, original_value: Optional[Any]) -> Optional[Any]:
        if not original_value:
            return original_value

        if GenericMapper.__is_primitive_type(attribute_type):
            return original_value

        list_item_type = GenericMapper.__get_list_type(attribute_type)

        if list_item_type:
            return [cls.__convert_to_entity_attribute(list_item_type, original_item_value)
                    for original_item_value in original_value]

        if attribute_type in TO_ENTITY_CONVERTERS:
            return TO_ENTITY_CONVERTERS[attribute_type](original_value)

        if is_dataclass(attribute_type):
            return cls.__to_entity(original_value, attribute_type)

        if GenericMapper.__is_enum_type(attribute_type):
            return enum_utils.instantiate_enum_from_str_name(attribute_type, original_value)

        return None

    @staticmethod
    def __get_field_type(attribute: Field) -> Type:
        field_type = attribute.type
        origin = get_origin(field_type)

        if origin is Union:
            args = [t for t in get_args(field_type) if t is not type(None)]
            field_type = args[0]

        return field_type

    @staticmethod
    def __get_list_type(attribute_type: Type) -> Type:
        origin = get_origin(attribute_type)
        list_item_type = None

        if origin is list:
            args = [t for t in get_args(attribute_type) if t is not type(None)]
            list_item_type = args[0]

        return list_item_type

    @staticmethod
    def __is_enum_type(attribute_type: Type) -> bool:
        if attribute_type is Enum or attribute_type is StrEnum:
            return True

        parents = attribute_type.__bases__
        return GenericMapper.__is_enum_type(parents[0]) if parents else False

    @staticmethod
    def __is_primitive_type(field_type: Type) -> bool:
        return field_type in PRIMITIVE_TYPES

    @classmethod
    def __get_entity_class_attributes(cls) -> List[Field]:
        return GenericMapper.__get_class_attributes(cls._get_entity_type())

    @staticmethod
    def __get_class_attributes(class_type: Type) -> List[Field]:
        return fields(class_type)

    @classmethod
    def _get_entity_type(cls) -> Type:
        return get_args(cls.__orig_bases__[0])[0]
