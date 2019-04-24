from app.celery import celery_app
from flask import Flask

from app.mail import mail
from app.models import db
from app.blueprint import register
from app.scheduler import scheduler
from config import config
from flask.logging import default_handler
import logging
import mutilog
import os
from app.my_redis import Redis
from app.my_mongo import mongodb
'''
此工厂函数用于创建flask并做了一定的配置
'''


def create_app():
    app = Flask(__name__)

    app.config.from_object(config[os.getenv('flask-env', 'dev')])

    # log配置
    app.logger.removeHandler(default_handler)
    # 配置写入日志文件的handler
    # handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler = mutilog.MyLoggerHandler('flask', encoding='UTF-8', when='D', backupCount=30)
    # handler = handlers.TimedRotatingFileHandler('log/flask.log', encoding='UTF-8', interval=1, when='M', atTime=datetime.time(16, 45))
    logging_format = logging.Formatter(
        '%(asctime)s - [pid]%(process)d [thread]%(thread)d|%(threadName)s - %(levelname)s - %(pathname)s :%(lineno)s|%(funcName)s - %(message)s')
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
    db.app = app
    # 蓝图配置
    register(app)
    # 邮件配置
    mail.init_app(app)
    # 定时任务配置
    scheduler.init_app(app)
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # 如果开了debug 就要这样配置
    scheduler.start()
    # celery配置
    celery_app.conf.update(app.config['CELERY'])
    # redis配置
    Redis.init_app(app)
    # mongodb配置
    mongodb.init_app(app)
    return app
