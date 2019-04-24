import sys

from flask import request, current_app, g
from sqlalchemy.exc import DatabaseError

from app import db
from app.models.user import Menu, Role
from utils.http_util import success_result, request_error
from utils.query_util import get_filter, get_paginate


def create():
    data = get_filter({'name', 'url'}, request.json, False)
    data.update(get_filter({'parent_id'}, request.json))
    menu = Menu(**data)
    try:
        db.session.add(menu)
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    current_app.logger.info('菜单创建 %r', menu)
    return success_result()


def retrieve(pk: int):
    menu = Menu.query.get_or_404(pk)
    response = menu.serializer()
    if request.args.get('roles', False):
        roles = [role.serializer() for role in menu.roles]
        response['roles'] = roles
    return success_result(menu=response)


def get_list():
    args = request.args.to_dict() or {}
    page, size = get_paginate(args)

    query = db.session.query(Menu)
    if 'role' in args:
        query = query.join(Menu.roles).filter(Role.name == args['role'])
    if 'name' in args:
        query = query.filter(Menu.name.like('%' + args['name'] + '%'))
    if 'parent' in args:
        query = query.filter(Menu.parent_id == args['parent'])
    menus = query.paginate(page, size, True)
    data = {
        'menus': Menu.make_tree(menus.items),
        'count': menus.total
    }

    return success_result(**data)


def update_basic(pk: int):
    data = get_filter({'name', 'url', 'parent_id'}, request.json)
    try:
        num = Menu.query.filter(Menu.id == pk).update(data)
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')

    current_app.logger.info('菜单[id]:%d 更新了 %d', pk, num)
    if num == 0:
        return success_result(msg='虽然成功了,但是什么事都没有发生')
    return success_result()


def delete(pk: int):
    menu = Menu.query.get_or_404(pk)
    try:
        db.session.delete(menu)
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')

    current_app.logger.info('菜单 %r 被删除了', menu)
    return success_result()


def bind_role(pk: int):
    menu = Menu.query.get_or_404(pk)
    roles = request.json.get('roles', [])
    if isinstance(roles, list):
        role = Role.query.filter(Role.id.in_(roles))
        menu.roles.extend(role)
    else:
        role = Role.query.get_or_404(roles)
        menu.roles.append(role)
    try:
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    return success_result()


def unbind_role(pk: int):
    menu = Menu.query.get_or_404(pk)
    roles = request.json.get('roles', [])
    if isinstance(roles, list):
        role = Role.query.filter(Role.id.in_(roles)).all()
        for ro in role:
            if ro in menu.roles:
                menu.roles.remove(ro)
    else:
        role = Role.query.get_or_404(roles)
        if role in menu.roles:
            menu.roles.remove(role)
    try:
        db.session.commit()
    except DatabaseError as e:
        current_app.logger.exception(e)
        request_error('database error')
    return success_result()


update_action = ('unbind_role', 'bind_role', 'update_basic')


def update(pk: int):
    action = request.args.get('action', None)
    if action and action in update_action:
        current_app.logger.info('%r 执行了 %s', g.user, action)
        # current_app.logger.info('<menu> %r 执行了 %s', g.user, action)
        return getattr(sys.modules[__name__], action)(pk)
    else:
        request_error('请选择有效的action')
