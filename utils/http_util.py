import functools

from flask import current_app
from flask_restful import abort


def args_log():
    """
    装饰器
    打印函数入参
    :return: 返回原函数
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            current_app.logger.info('[%s] %r %r', func.__name__, args, kw)
            return func(*args, **kw)

        return wrapper

    return decorator


def request_error(error_msg: str, code: int = 500):
    """
    错误结果的统一返回格式,为了随时随地地返回错误,用了异常的方式直接中断
    :param error_msg: 错误信息
    :param code: http_code
    :return:
    """
    abort(code, result='error', error_msg=error_msg)


def success_result(code=200, **kwargs):
    result = {'result': 'success'}
    if kwargs:
        result = kwargs
    return result, code
