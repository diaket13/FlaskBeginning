from bson import ObjectId, Decimal128

from app.my_mongo import mongodb


class Users:
    collection = mongodb.database['users']

    def __init__(self, openid, session_key):
        self.openid = openid
        self.session_key = session_key

    def generalize(self):
        return self.collection.insert_one({
            'openid': self.openid,
            'session_key': self.session_key,
            'times': {
                'total': 0,
                'remain': 0,
                'today': 0,
                'timestamp': 0
            },
            'amount': Decimal128('0')
        })


class Product:
    collection = mongodb.database['product']
