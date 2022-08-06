from werkzeug.security import generate_password_hash

from models import User, db


class BaseService:
    """Base service class for create, update, delete actions."""
    model = None

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.model.query.filter(*args, **kwargs)

    @classmethod
    def create(cls, **params):
        obj = cls.model(**params)
        db.session.add(obj)
        db.session.commit()
        return obj


class UserService(BaseService):
    """User model services: create, update, delete."""
    model = User

    @classmethod
    def get_by_username(cls, username):
        return cls.model.query.filter_by(username=username).first()

    @classmethod
    def get_by_username_or_email(cls, username, email):
        return cls.model.query.filter(
            (cls.model.username == username) |
            (cls.model.email == email)).first()

    @classmethod
    def create(cls, **params):
        params["password"] = generate_password_hash(params["password"])
        user = cls.model(**params)
        return user.create()
