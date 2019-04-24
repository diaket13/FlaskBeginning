from flask import current_app

from .http_util import request_error


def get_paginate(args: dict) -> (int, int):
    """
    从参数中提取出page和size两个用于分页的参数,如果没有的话就用默认值代替
    :param args: 入参,一般为request.args
    :return: 包含两个值的元组
    """
    page = int(args.get('page', 1))
    size = int(args.get('size', 10))
    return page, size


def get_filter(filter_fields: set, args: dict, partial=True) -> dict:
    """
    参数提取
    从请求的入参中提取想要的参数
    :param filter_fields: 想要的参数集合
    :param args: 请求入参 一般为request.args和request.json
    :param partial: 是否允许参数不全,默认为真,意味着允许入参中可以有某些参数不存在
    :return: 参数过滤后的集合
    """
    filter_args = {k: v for k, v in args if k in filter_fields}
    if not partial and len(filter_args.keys()) < len(filter_fields):
        k = filter_fields - filter_args.keys()
        current_app.logger.error(f'{k} not found')
        request_error(f'{k} not found', 400)
    return filter_args
