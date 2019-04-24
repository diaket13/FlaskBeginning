from flask import current_app, g, request
from sqlalchemy.exc import DatabaseError, IntegrityError

from app.models import db
from app.models.user import User
from utils.http_util import request_error, success_result
from utils.query_util import get_filter


def register():
    needed_args = get_filter({'user_open_id', 'username', 'password', 'confirm_password'}, request.get_json(force=True), False)
    password = needed_args['password']
    if len(password) < 8:
        request_error(f'密码长度不够{8}位', 400)
    if password != needed_args.get('confirm_password'):
        request_error('两次密码输入不一样', 400)
    if User.query.filter_by(name=needed_args['username']).first():
        request_error('用户名已存在', 400)
    manager = User(user_open_id=needed_args['user_open_id'], name=needed_args['username'])
    manager.set_hash_password(password)
    try:
        db.session.add(manager)
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.error("%s,%r", repr(manager), e.orig)
        request_error(str(e.orig), 400)
    except DatabaseError as e:
        current_app.logger.exception(manager)
        request_error(str(e.orig), 500)
    else:
        current_app.logger.info(repr(manager) + '注册')
        return success_result()


def retrieve():
    return success_result(user=g.user.serializer())


def token_refresh():
    return success_result(token=g.user.generate_auth_token().decode('ascii'))


def login():
    json = request.json or {}
    data = get_filter({'username', 'password'}, json, False)
    user = User.query.filter_by(name=data['username']).first()
    if not user or not user.verify_password(data['password']):
        request_error('用户或密码不对', 404)
    return success_result(user=user.serializer())


def change_password():
    needed_args = get_filter({'old_password', 'password', 'confirm_password', }, request.get_json(force=True), False)
    user = g.user
    if not user.verify_password(needed_args['old_password']):
        request_error(f'旧密码不正确', 400)
    if needed_args.get('password') != needed_args.get('confirm_password'):
        request_error('两次密码输入不一样', 400)
    user.set_hash_password(needed_args.get('password'))
    try:
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.error("%s,%r", repr(user), e.orig)
        request_error(str(e.orig), 400)
    except DatabaseError as e:
        current_app.logger.exception(user)
        request_error(str(e.orig), 500)
    else:
        current_app.logger.info(repr(user) + '更改密码')
        return success_result(user=user.login())
