from flask import Blueprint, request, current_app as app
from flask_restful import Api, Resource
from utils.http_util import args_dict


class GroupAlbum(Resource):
    # def get(self, pk=None):
    #     if pk:
    #         return group_view.retrieve_album(pk)
    #     else:
    #         args = args_dict(request)
    #         return group_view.list_album(args)
    #
    # def post(self, pk=None):
    #     return group_view.create(request)
    #
    # def put(self, pk=None):
    #     return group_view.partial_update(pk, request)
    #     # return group_view.update(pk, request)
    #
    # def delete(self, pk=None):
    #     return group_view.delete(pk, request)
    #
    # def patch(self, pk=None):
    #     return group_view.partial_update(pk, request)
    pass


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(GroupAlbum, '/group/album', '/group/album/<int:pk>')
