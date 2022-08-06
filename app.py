import os
import click
from flask.cli import with_appcontext
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from auth.controllers import (
    LoginController,
    RegisterController,
    UserController,
    jwt
)
from cars.controllers import CarsController, CarController
from models import db


app = Flask(__name__)
api = Api(app)

# Loading env variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

# config
db_url = 'mysql://root:Apostol716@localhost/auto_net'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)
jwt.init_app(app)


@click.command(name='create')
@with_appcontext
def create():
    db.create_all()


api.add_resource(LoginController, '/login')
api.add_resource(RegisterController, '/register')
api.add_resource(UserController, '/user')

api.add_resource(CarsController, '/cars')
api.add_resource(CarController, '/cars/<int:car_id>')

app.cli.add_command(create)

if __name__ == '__main__':
    app.run(debug=True)
