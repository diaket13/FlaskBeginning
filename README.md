# FlaskBeginning
小型的flask服务 功能包括
- jwt  用flask_httpauth + itsdangerous来实现的
- restful blueprint+flask_restful实现
- 数据存储 redis + mysql + mongodb 3个数据库都有集成 其中mysql使用了orm flask_sqlalchemy 
- 邮件 flask_mail
- 异步任务 celery
- flask自身的管理 flask_migrate flask_script
- 定时任务 celery 和 apscheduler
- log 按时间划分的多进程可用的日志