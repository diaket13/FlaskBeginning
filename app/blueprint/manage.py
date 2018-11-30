from flask import Blueprint, request, g
from flask_restful import Api, Resource

from flask_cors import CORS
from app.auth import base_auth, multi_auth
from app.views.manage import manage
from utils.http_util import args_dict


class User(Resource):
    @base_auth.login_required
    def get(self):
        return manage.retrieve()

    def post(self):
        return manage.register(request.json)


class Album(Resource):
    decorators = [multi_auth.login_required]
    #
    # def get(self, pk=None):
    #     if pk:
    #         return album.retrieve(pk)
    #     else:
    #         args = args_dict(request)
    #         return album.list(args)
    #
    # def put(self, pk=None):
    #     return album.update(pk, request)
    #
    # def delete(self, pk=None):
    #     return album.delete(pk)
    #
    # def patch(self, pk=None):
    #     return album.partial_update(pk, request)
    #
    # def post(self, pk=None):
    #     return album.create(request)


manage_bp = Blueprint('manage', __name__)
CORS(manage_bp)
api = Api(manage_bp)
api.add_resource(User, '/user')
api.add_resource(Album, '/album', '/album/<int:pk>')
