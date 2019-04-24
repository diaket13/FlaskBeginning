from flask_apscheduler import APScheduler

scheduler = APScheduler()
# scheduler.add_job(id='1', func=days_rebate, trigger='cron', day='*', hour=0, minute=0, second=0)
# scheduler.add_job(id='1', func=days_rebate, trigger='cron', second='*/5')
from app.scheduler import scheduler_tasks