from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse

from auth.services import UserService
from base.controllers import (
    BaseListCreateController,
    BaseRetrieveUpdateDestroyController
)
from cars.services import CarService


class CarsController(BaseListCreateController):
    """Cars controller, provides list and create methods."""
    body_parser = reqparse.RequestParser()
    body_parser.add_argument('brand', type=str, required=True)
    body_parser.add_argument('category', type=str, required=True)
    body_parser.add_argument('model', type=str, required=True)
    body_parser.add_argument('image', type=str)
    body_parser.add_argument('price', type=int, required=True)
    body_parser.add_argument('year', type=int, required=True)
    body_parser.add_argument('description', type=str)

    args_parser = reqparse.RequestParser()
    args_parser.add_argument('sort', type=str, location='args')

    service = CarService

    @jwt_required()
    def post(self):
        """Create car method."""
        username = get_jwt_identity()
        user = UserService.get_by_username(username)
        data = self.body_parser.parse_args()
        data["user_id"] = user.id
        car = self.service.create(**data)
        return car.serialize, 201


class CarController(BaseRetrieveUpdateDestroyController):
    """Car controller, provides retrieve, update and delete methods."""
    parser = reqparse.RequestParser()
    parser.add_argument('brand', type=int, required=True)
    parser.add_argument('category', type=int, required=True)
    parser.add_argument('model', type=str, required=True)
    parser.add_argument('image', type=str)
    parser.add_argument('price', type=int, required=True)
    parser.add_argument('year', type=int, required=True)
    parser.add_argument('description', type=str)

    service = CarService

    @jwt_required()
    def patch(self, pk):
        username = get_jwt_identity()
        user = UserService.get_by_username(username)
        car = CarService.get_by_id(pk)

        # Only owner can update car data.
        if car.user_id != user.id:
            return {'error': 'You can\'t update others\' car.'}

        data = self.parser.parse_args()
        data.pop('user_id')
        car.update(data)
        return car.serialize, 200

    @jwt_required()
    def delete(self, pk):
        username = get_jwt_identity()
        user = UserService.get_by_username(username)
        car = CarService.get_by_id(pk)

        # Only owner can update car data.
        if car.user_id != user.id:
            return {'error': 'You can\'t delete others\' car.'}

        return super(CarController, self).delete(pk)
