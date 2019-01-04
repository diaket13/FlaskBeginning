REDIS_INFO = ['127.0.0.1', 'password', 6379, 0]


class AppConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/album?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'iv!YyJ!tN1SPc$S0uGR1GS^5Fc%2Tk0'
    CELERY = {
        'broker_url': 'redis://dev:password@127.0.0.1:6379/3',
        'result_backend': 'redis://dev:password@127.0.0.1:6379/3',
        'task_serializer': 'json'
    }

