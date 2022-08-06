from abc import ABC
from typing import Any
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import RequestParser


class BaseListCreateController(ABC, Resource):
    """Base class for create and update operations."""
    parser: RequestParser
    service: Any

    def get(self):
        result = self.service.all()
        sort_by = request.args.get("sort", type=str)
        desc = False

        if sort_by is not None:
            if sort_by.startswith('-'):
                sort_by = sort_by[1:]
                desc = True

            if (attr := getattr(self.service.model, sort_by, None)) is not None:
                if desc:
                    result = result.order_by(attr.desc())
                else:
                    result = result.order_by(attr)

        return [obj.serialize for obj in result], 200

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        obj = self.service.create(**data)
        return obj.serialize, 201


class BaseRetrieveUpdateDestroyController(ABC, Resource):
    """Base class for retrieve, update and destroy operations."""

    model: Any
    parser: RequestParser
    service: Any

    def get(self, pk):
        return self.service.get_by_id(pk).serialize, 200

    @jwt_required()
    def patch(self, pk):
        obj = self.service.get_by_id(pk)
        result = obj.update(**self.parser.parse_args())
        return result.serialize, 200

    @jwt_required()
    def delete(self, pk):
        obj = self.service.get_by_id(pk)
        obj.delete()
        return None, 204
