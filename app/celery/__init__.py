from celery import Celery
from celery.schedules import crontab

celery_app = Celery('flask-beginning')


celery_app.conf.update(beat_schedule={
    'do_email': {
        'task': 'app.celery.tasks.timer.db_timer',
        "schedule": crontab(minute="*/1"),
        "args": ()
    },
})

from .tasks import test,timer