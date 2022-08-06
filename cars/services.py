from base.services import BaseService
from models import Car, Category, Manufacturer


class CarService(BaseService):
    """Car service class."""
    model = Car


class CategoryService(BaseService):
    """Category service class."""
    model = Category


class ManufacturerService(BaseService):
    """Manufacturer service class."""
    model = Manufacturer
