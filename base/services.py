from abc import ABC
from typing import Any


class BaseService(ABC):
    """Base service class for models."""
    model: Any

    @classmethod
    def all(cls):
        return cls.model.query.filter()

    @classmethod
    def create(cls, **params):
        return cls.model(**params).create()

    @classmethod
    def filter(cls, **params):
        return cls.model.query.filter(**params)

    @classmethod
    def get_by_id(cls, _id: int):
        return cls.model.query.get_or_404(_id)
