from flask import g, make_response, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from app.models.user import Manager
from utils.http_util import error_result

base_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(base_auth, token_auth)


@base_auth.verify_password
def verify_password(username, password):
    manager = Manager.query.filter_by(name=username).first()
    if not manager or not manager.verify_password(password):
        return False
    g.manager = manager
    return True


@base_auth.error_handler
def unauthorized():
    return make_response(jsonify(error_result('未登录!!', 401)))


@token_auth.verify_token
def verify_token(token):
    manager = Manager.verify_auth_token(token)
    if not manager:
        return False
    g.manager = manager
    return True