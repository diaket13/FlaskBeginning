from app.celery import celery_app
from celery.utils.log import get_task_logger
from app.models import db
from app.models.user import User
logger = get_task_logger(__name__)


@celery_app.task
def db_timer():
    from app.celery.app import app
    with app.app_context():
        a = db.session.query(User).first()
        logger.info('album %s', a.serializer())
        a.final_votes += 1
        db.session.commit()
