from flask_restful import Resource


class CarsController(Resource):
    """Cars controller, provides list and create methods."""

    def get(self):
        ...

    def post(self):
        ...


class CarController:
    """Car controller, provides retrieve, update and delete methods."""

    def get(self, car_id):
        pass

    def patch(self, car_id):
        pass

    def delete(self, car_id):
        pass
