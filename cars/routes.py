from flask_restful import Api

from cars.controllers import (
    CategoriesController,
    CategoryController,
    ManufacturersController,
    ManufacturerController,
    CarsController,
    CarController
)

api = Api()


api.add_resource(CategoriesController, '/categories')
api.add_resource(CategoryController, '/categories/<int:pk>')

api.add_resource(ManufacturersController, '/manufacturers')
api.add_resource(ManufacturerController, '/manufacturers/<int:pk>')

api.add_resource(CarsController, '/cars')
api.add_resource(CarController, '/cars/<int:pk>')
