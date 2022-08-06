import os
import click
from flask.cli import with_appcontext
from flask import Flask
from dotenv import load_dotenv

from auth.jwt import jwt
from auth.routes import api as auth_api
from cars.routes import api as cars_api

from models import db


app = Flask(__name__)

# Loading env variables
load_dotenv()

# base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# mysql config
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASSWORD')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DB = os.environ.get('MYSQL_DATABASE')

# database connection url
db_url = f'mysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)
jwt.init_app(app)
auth_api.init_app(app)
cars_api.init_app(app)


@click.command(name='create_db_schema')
@with_appcontext
def create_db_schema():
    """Custom command for db schema creation."""
    db.drop_all()
    db.create_all()


app.cli.add_command(create_db_schema)

if __name__ == '__main__':
    app.run(debug=bool(int(os.environ.get('FLASK_DEBUG', '1'))))
