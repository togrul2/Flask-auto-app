from flask_restful import Api

from auth.controllers import (
    RegisterController,
    LoginController,
    UserController
)

api = Api()

api.add_resource(LoginController, '/api/login')
api.add_resource(RegisterController, '/api/register')
api.add_resource(UserController, '/api/user')
