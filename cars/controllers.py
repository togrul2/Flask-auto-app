from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse

from auth.services import UserService
from base.controllers import BaseListCreateController, \
    BaseRetrieveUpdateDestroyController
from cars.services import CarService, ManufacturerService, CategoryService


class CarsController(BaseListCreateController):
    """Cars controller, provides list and create methods."""
    parser = reqparse.RequestParser()
    parser.add_argument('manufacturer_id', type=int, required=True)
    parser.add_argument('category_id', type=int, required=True)
    parser.add_argument('model', type=str, required=True)
    parser.add_argument('image', type=str)
    parser.add_argument('price', type=int, required=True)
    parser.add_argument('year', type=int, required=True)
    parser.add_argument('description', type=str)

    service = CarService

    @jwt_required()
    def post(self):
        """Create car method."""
        username = get_jwt_identity()
        user = UserService.get_by_username(username)
        data = self.parser.parse_args()
        data["user_id"] = user.id
        car = self.service.create(**data)
        return car.serialize, 201


class CarController(BaseRetrieveUpdateDestroyController):
    """Car controller, provides retrieve, update and delete methods."""
    parser = reqparse.RequestParser()
    parser.add_argument('manufacturer_id', type=int, required=True)
    parser.add_argument('category_id', type=int, required=True)
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

        super(CarController, self).delete(pk)


class CategoryController(BaseRetrieveUpdateDestroyController):
    """Category controller, provides retrieve, update and delete methods."""
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    service = CategoryService


class CategoriesController(BaseListCreateController):
    """Categories controller, provides list and create methods."""
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    service = CategoryService


class ManufacturerController(BaseRetrieveUpdateDestroyController):
    """Manufacturer controller, provides retrieve,
    update and delete methods."""
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    service = ManufacturerService


class ManufacturersController(BaseListCreateController):
    """Manufacturers controller, provides list and create methods."""
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True)
    service = ManufacturerService
