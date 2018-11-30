REDIS_INFO = ['127.0.0.1', 'password', 6379, 0]


class AppConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/album?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'iv!YyJ!tN1SPc$S0uGR1GS^5Fc%2Tk0'
    CELERY = {
        'broker_url': 'redis://dev:lk123456@192.168.18.107:6379/3',
        'result_backend': 'redis://dev:lk123456@192.168.18.107:6379/3',
        'task_serializer': 'json'
    }

