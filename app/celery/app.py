from manage import app
from app.celery import celery_app

# 在windows上 用 celery worker -A celery_worker.celery -l INFO -P eventlet 运行celery
# python3.7 的celery的版本跟requirement上的有出入 百度解决

