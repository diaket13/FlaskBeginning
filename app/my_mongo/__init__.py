import pymongo


class MyMongodb:

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        self.client = pymongo.MongoClient(kwargs['MONGODB_URL']) if 'MONGODB_URL' in kwargs else None
        self.database = kwargs.get('MONGODB_DB', None)

    def init_app(self, app):
        self.client = pymongo.MongoClient(app.config['MONGODB_URL'])
        self.database = app.config['MONGODB_DB']


mongodb = MyMongodb()
