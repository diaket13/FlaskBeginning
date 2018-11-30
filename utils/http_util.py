import json
import functools
from flask import current_app


def args_log(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            current_app.logger.info('[%s] %r %r', func.__name__, args, kw)
            return func(*args, **kw)
        return wrapper
    return decorator


def data_dict(request) -> dict:
    return json.loads(request.data.decode('utf-8'))


def args_dict(request) -> dict:
    return request.args.to_dict()


def error_result(error_msg: str, code=500):
    return {'result': 'error', 'error_msg': error_msg}, code


def success_result(code=200, **kwargs):
    result = {'result': 'success'}
    if kwargs:
        result.update(kwargs)
    return result, code
