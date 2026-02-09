from typing import TypeVar
from pydantic import BaseModel
from src.database import BaseModel as DBBaseModel


DBModelType = TypeVar("DBModelType", bound=DBBaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data, **extra):
        result = cls.schema.model_validate(data, from_attributes=True)
        if extra:
            return result.model_copy(update=extra)
        return result

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
