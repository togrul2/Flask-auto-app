from flask_restful import Api

from cars.controllers import (
    CarsController,
    CarController,
    MyCarsController
)

api = Api()

api.add_resource(CarsController, '/api/cars')
api.add_resource(CarController, '/api/cars/<int:pk>')
api.add_resource(MyCarsController, '/api/user/cars')
