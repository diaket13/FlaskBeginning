from flask import current_app, g
from sqlalchemy.exc import DatabaseError, IntegrityError

from app.models.user import Manager
from utils.http_util import error_result, success_result
from app.models import db
from utils.query_util import get_filter


def register(info: dict):
    try:
        needed_args = get_filter(('user_open_id', 'username', 'password', 'confirm_password',), info, False)
    except KeyError as e:
        return error_result(f'Parameters {str(e)} are missing', 400)
    password = needed_args['password']
    if len(password) < 8:
        return error_result(f'密码长度不够{8}位', 400)
    if password != needed_args.get('confirm_password'):
        return error_result('两次密码输入不一样', 400)
    if Manager.query.filter_by(name=needed_args['username']).first():
        return error_result('用户名已存在', 400)
    manager = Manager(user_open_id=needed_args['user_open_id'], name=needed_args['username'])
    manager.set_hash_password(password)
    try:
        db.session.add(manager)
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.error("%s,%r", repr(manager), e.orig)
        return error_result(str(e.orig), 400)
    except DatabaseError as e:
        current_app.logger.exception(manager)
        return error_result(str(e.orig), 500)
    else:
        current_app.logger.info(repr(manager) + '注册')
        return success_result()


def retrieve():
    return g.manager.serializer(), 200
