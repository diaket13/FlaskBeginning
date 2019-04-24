from flask import Blueprint
from flask_cors import CORS
from flask_restful import Api, Resource

from app.auth import token_auth, refresh_auth
from app.views.manage import user


class User(Resource):
    decorators = [token_auth.login_required]

    def get(self):
        return user.retrieve()

    def post(self):
        return user.change_password()


class Register(Resource):
    def post(self):
        return user.register()


class Login(Resource):
    def post(self):
        return user.login()


class TokenRefresh(Resource):

    @refresh_auth.login_required
    def get(self):
        return user.token_refresh()


user_bp = Blueprint('user', __name__)
CORS(user_bp)
api = Api(user_bp)
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(User, '')
api.add_resource(TokenRefresh, '/token')
