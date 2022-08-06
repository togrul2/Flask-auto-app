from typing import Any, Dict
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy import func

db = SQLAlchemy()


class BaseModel:
    """Base class for model functionality."""
    def create(self):
        """Create method."""
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **params: Dict[str, Any]):
        """Update method."""
        for k, v in params.items():
            if v:
                setattr(self, k, v)

        db.session.commit()

    def delete(self):
        """Delete method."""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Base serializer for model."""
        raise NotImplementedError


class User(db.Model, BaseModel):
    """User model used for authentication"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': str(self.created_at)
        }

    def update(self, params: Dict[str, Any]):
        """User update method."""
        password = generate_password_hash(params["password"])
        params["password"] = password
        return super().update(**params)

    def __repr__(self):
        return f'<User {self.firstname}>'


class Manufacturer(BaseModel, db.Model):
    """Manufacturer model."""
    __tablename__ = 'manufacturer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Manufacturer {self.name}>'


class Category(BaseModel, db.Model):
    """Category model."""
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Car(BaseModel, db.Model):
    """Car model."""
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    model = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    owner = db.relationship('User', backref=db.backref('cars', lazy=True))
    category = db.relationship('Category',
                               backref=db.backref('cars', lazy=True))
    manufacturer = db.relationship('Manufacturer',
                                   backref=db.backref('cars', lazy=True))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'manufacturer_id': self.manufacturer_id,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'model': self.model,
            'image': self.image,
            'price': self.price,
            'year': self.year,
            'description': self.description,
            'created_at': str(self.created_at)
        }
