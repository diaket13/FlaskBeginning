import sys

from flask import request, current_app, g
from sqlalchemy.exc import DatabaseError

from app import db
from app.models.user import Menu, Role, User
from utils.http_util import success_result, request_error
from utils.query_util import get_filter, get_paginate


def create():
    data = get_filter({'name'}, request.json, False)
    role = Role(**data)
    try:
        db.session.add(role)
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    current_app.logger.info('角色创建 %r', role)
    return success_result()


def retrieve(pk: int):
    role = Role.query.get_or_404(pk)
    response = role.serializer()
    if 'menu' in request.args:
        response['menus'] = Menu.make_tree(role.menus)
    if 'user' in request.args:
        users = [user.info() for user in role.users]
        response['users'] = users
    return success_result(role=response)


def get_list():
    args = request.args.to_dict() or {}
    page, size = get_paginate(args)

    query = db.session.query(Role)
    if 'user' in args:
        query = query.join(Role.users).filter(User.id == args['user'])
    if 'name' in args:
        query = query.filter(Role.name.like('%' + args['name'] + '%'))
    roles = query.paginate(page, size, True)
    data = {
        'roles': [role.serializer() for role in roles.items],
        'count': roles.total
    }

    return success_result(**data)


def update_basic(pk: int):
    data = get_filter({'name'}, request.json)
    try:
        num = Role.query.filter(Role.id == pk).update(data)
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        return request_error('database error')

    current_app.logger.info('角色[id]:%d 更新了 %d', pk, num)
    if num == 0:
        return success_result(msg='虽然成功了,但是什么事都没有发生')
    return success_result()


def delete(pk: int):
    role = Role.query.get_or_404(pk)
    try:
        db.session.delete(role)
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')

    current_app.logger.info('角色 %r 被删除了', role)
    return success_result()


def bind_user(pk: int):
    role = Role.query.get_or_404(pk)
    users = request.json.get('users', [])
    if isinstance(users, list):
        user = User.query.filter(User.id.in_(users))
        role.users.extend(user)
    else:
        user = User.query.get_or_404(users)
        role.users.append(user)
    try:
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    return success_result()


def unbind_user(pk: int):
    role = Role.query.get_or_404(pk)
    users = request.json.get('users', [])
    if isinstance(users, list):
        user = User.query.filter(User.id.in_(users)).all()
        for usr in user:
            if usr in role.users:
                role.users.remove(usr)
    else:
        user = User.query.get_or_404(users)
        if user in role.users:
            role.users.remove(user)
    try:
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    return success_result()


def bind_menu(pk: int):
    role = Role.query.get_or_404(pk)
    menus = request.json.get('menus', [])
    if isinstance(menus, list):
        menu = Menu.query.filter(Menu.id.in_(menus))
        role.menus.extend(menu)
    else:
        menu = Menu.query.get_or_404(menus)
        role.menus.append(menu)
    try:
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    return success_result()


def unbind_menu(pk: int):
    role = Role.query.get_or_404(pk)
    menus = request.json.get('menus', [])
    if isinstance(menus, list):
        menu = Menu.query.filter(Menu.id.in_(menus)).all()
        for me in menu:
            if me in role.menus:
                role.menus.remove(me)
    else:
        menu = Menu.query.get_or_404(menus)
        if menu in role.menus:
            role.menus.remove(menu)
    try:
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    return success_result()


update_action = ('unbind_menu', 'bind_menu', 'unbind_user', 'bind_user', 'update_basic')


def update(pk: int):
    action = request.args.get('action', None)
    if action and action in update_action:
        current_app.logger.info('%r 执行了 %s', g.user, action)
        # current_app.logger.info('<role> %r 执行了 %s', g.user, action)
        return getattr(sys.modules[__name__], action)(pk)
    else:
        request_error('请选择有效的action')
