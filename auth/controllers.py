"""Controllers module"""
import datetime

from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from auth.services import UserService
from models import db


class LoginController(Resource):
    """Login controller."""
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', required=True)

    def post(self):
        data = self.parser.parse_args()

        # Search user by username
        if user := UserService.get_by_username(data["username"]):
            if check_password_hash(user.password, data["password"]):
                # Found username password is correct, generate tokens
                access_token = create_access_token(
                    identity=data['username'],
                    expires_delta=datetime.timedelta(
                        days=365))  # Expiry is 365 for test purposes
                refresh_token = create_refresh_token(identity=data['username'])
                return {"access": access_token,
                        "refresh": refresh_token}, 201

        return {"error": "Invalid login or password"}, 400


class RegisterController(Resource):
    """Register controller."""

    parser = reqparse.RequestParser()
    parser.add_argument('first_name', required=True)
    parser.add_argument('last_name', required=True)
    parser.add_argument('username', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        data = self.parser.parse_args()
        if UserService.get_by_username_or_email(data['username'],
                                                data['email']):
            return {"error": ("User with this username"
                              "or email already exists")}, 400

        user = UserService.create(**data)
        return user.serialize, 201


class UserController(Resource):
    """Controller for user based on access token."""
    parser = reqparse.RequestParser()
    parser.add_argument('first_name')
    parser.add_argument('last_name')
    parser.add_argument('username')
    parser.add_argument('email')
    parser.add_argument('password')

    @jwt_required()
    def get(self):
        """Retrieve user info."""
        username = get_jwt_identity()
        user = UserService.get_by_username(username)
        return user.serialize, 200

    @jwt_required()
    def patch(self):
        """Partial edit of user."""
        username = get_jwt_identity()
        user = UserService.get_by_username(username)
        data = self.parser.parse_args()
        user.update(**data)
        return user.serialize, 200

    @jwt_required()
    def delete(self):
        """Deletion of user."""
        username = get_jwt_identity()
        admin = UserService.get_by_username(username)
        admin.delete()
        db.session.commit()
        return {}, 204
