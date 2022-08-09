from base.services import BaseService
from models import Car


class CarService(BaseService):
    """Car service class."""
    model = Car
