from flask_restful import Api

from auth.controllers import (
    RegisterController,
    LoginController,
    UserController
)

api = Api()

api.add_resource(LoginController, '/login')
api.add_resource(RegisterController, '/register')
api.add_resource(UserController, '/user')
