from abc import ABC
from typing import Any
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import RequestParser


class BaseListCreateController(ABC, Resource):
    """Base class for create and list operations."""
    body_parser: RequestParser
    args_parser: RequestParser
    service: Any

    def get(self):
        # Here we fetch all records from db.
        result = self.service.all()
        data = self.args_parser.parse_args()
        sort_desc = False  # Sort ascending by default

        # If sort keyword presents in request args, then sort.
        if sort_by := data.get("sort"):
            if sort_by.startswith('-'):  # `-` at the beginning indicates desc.
                sort_by = sort_by[1:]
                sort_desc = True

            if attr := getattr(self.service.model, sort_by, None):
                if sort_desc:
                    result = result.order_by(attr.desc())
                else:
                    result = result.order_by(attr)
            else:
                return {'error': 'wrong sorting attribute given.'}, 400

        return [obj.serialize for obj in result], 200

    @jwt_required()
    def post(self):
        data = self.body_parser.parse_args()
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
