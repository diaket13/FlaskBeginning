import redis

PREFIX = 'flask_beginning:'


class MyRedis:

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if 'REDIS' in kwargs:
            self.client = redis.StrictRedis(connection_pool=redis.ConnectionPool(**kwargs['REDIS']))
        else:
            self.client = None

    def init_app(self, app):
        self.client = redis.StrictRedis(connection_pool=redis.ConnectionPool(**app.config['REDIS']))


Redis = MyRedis()
