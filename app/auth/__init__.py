from functools import wraps

from flask import g, make_response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_restful import abort

from app.models.user import User

base_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
multi_auth = MultiAuth(base_auth, token_auth)
refresh_auth = HTTPTokenAuth()


@base_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(name=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@base_auth.error_handler
def unauthorized():
    return make_response({'error_msg': '未登录!!'}, 401)


@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


@refresh_auth.verify_token
def verify_refresh_token(token):
    user = User.verify_refresh_token(token)
    if not user:
        return False
    g.user = user
    return True


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = g.user
        if not user.is_admin:
            abort(403, error_msg='你不是管理员')
        return f(*args, **kwargs)

    return decorated
