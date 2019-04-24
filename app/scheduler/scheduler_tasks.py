import logging
import os

import pytz
from sqlalchemy import text

from app.mail.message import daily_messenger
from app.models import db
from app.models.user import User
from app.scheduler import scheduler

logger = logging.getLogger("scheduler")
logger.setLevel(logging.DEBUG)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), "scheduler.log"),encoding='UTF-8')
fh.setLevel(logging.DEBUG)
# 设置日志格式
formatter = logging.Formatter('%(asctime)s - [pid]%(process)d [thread]%(thread)d|%(threadName)s - %(levelname)s - %(pathname)s :%(lineno)s|%(funcName)s - %(message)s')
fh.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(fh)


@scheduler.task('cron', id='xxx', day='*', hour='0', minute='0', timezone=pytz.timezone('Asia/Shanghai'))
def xxx():
    logger.info('xxx')


@scheduler.task('cron', id='send_mail', day='*', hour='0', minute='0', timezone=pytz.timezone('Asia/Shanghai'))
def send_mail():
    with db.app.app_context():
        users = User.query.filter(text("create_time>=CURRENT_DATE()")).all()
        info = [i.name for i in users]
        daily_messenger(info)

