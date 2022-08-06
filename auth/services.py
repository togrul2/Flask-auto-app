from base.services import BaseService
from werkzeug.security import generate_password_hash

from models import User


class UserService(BaseService):
    """User model services."""
    model = User

    @classmethod
    def get_by_username(cls, username: str):
        return cls.model.query.filter_by(username=username).first()

    @classmethod
    def get_by_username_or_email(cls, username: str, email: str):
        """Get user by username or email."""
        return cls.model.query.filter(
            (cls.model.username == username) |
            (cls.model.email == email)).first()

    @classmethod
    def create(cls, **params):
        """User creation method."""

        if "password" in params:
            password = generate_password_hash(params["password"])
            params["password"] = password

        user = super().create(**params)
        return user.create()
