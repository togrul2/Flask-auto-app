from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class User(db.Model):
    """User model used for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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

    def __repr__(self):
        return f'<Student {self.firstname}>'


class Manufacturer(db.Model):
    """Manufacturer model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), primary_key=True)


class Car(db.Model):
    """Car model."""
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'))
    brand = db.relationship('Manufacturer', backref=db.backref('cars',
                                                               lazy=True))
    model = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
