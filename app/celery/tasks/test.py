import requests
from app.celery import celery_app
from celery.utils.log import get_task_logger
from app.models import db
from app.models.user import User
logger = get_task_logger(__name__)


@celery_app.task
def log_test(a):
    logger.info('put file %s', a)


@celery_app.task
def net_test(a):
    logger.info('connect %s', a)
    requests.get('http://192.168.0.1/api/test')


@celery_app.task
def db_test():
    from app.celery.app import app
    with app.app_context():
        a = db.session.query(User).first()
        logger.info('album %s', a.serializer())
        a.final_votes += 1
        db.session.commit()


