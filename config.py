class AppConfig:
    DEBUG = False
    MONGODB_URL = 'mongodb://user:password@127.0.0.1:27017,127.0.0.1:27018/?replicaSet=replicaName&authSource=admin'
    MONGODB_DB = 'database'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/database?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'iv!YyJ!tN1SPc$S0uGR1GS^5Fc%2Tk0'
    REFRESH_KEY = 'mBj%xhv0vjHn0j&vE2GE1nTNGItJ%*KT'
    CELERY = {
        'broker_url': 'redis://dev:password@127.0.0.1:6379/3',
        'result_backend': 'redis://dev:password@127.0.0.1:6379/3',
        'task_serializer': 'json',
        'timezone': 'Asia/Hong_Kong',
    }
    REDIS = {
        'host': '127.0.0.1',
        'port': 6379,
        'password': 'password',
        'db': 0,
        'max_connections': 32,
        'decode_responses': True
    }
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USERNAME = '123456@qq.com'
    MAIL_PASSWORD = 'password'
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = '123456@qq.com'


config = {
    'dev': AppConfig
}
