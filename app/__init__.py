from app.celery import celery
from flask import Flask
from app.models import db
from app.blueprint import register
from config import AppConfig
from flask.logging import default_handler
import logging
import mutilog

'''
此工厂函数用于创建flask并做了一定的配置
'''


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    # log配置
    app.logger.removeHandler(default_handler)
    # 配置写入日志文件的handler
    # handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler = mutilog.MyLoggerHandler('flask', encoding='UTF-8', when='H')
    # handler = handlers.TimedRotatingFileHandler('log/flask.log', encoding='UTF-8', interval=1, when='M', atTime=datetime.time(16, 45))
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    # 这是显示在控制台的handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    app.logger.addHandler(ch)
    # 日志级别为INFO
    app.logger.setLevel(logging.INFO)
    # db配置
    db.init_app(app)
    # 蓝图配置
    register(app)
    # celery配置
    celery.conf.update(app.config['CELERY'])

    return app
