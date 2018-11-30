from flask import current_app
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    hash_password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, nullable=False, server_default='0')

    def set_hash_password(self, password: str):
        self.hash_password = generate_password_hash(self.name + password)

    def verify_password(self, password: str):
        return check_password_hash(self.hash_password, self.name + password)

    def __repr__(self):
        return f'<Manager> [name]{self.name} [open_id]{self.user_open_id}'

    def generate_auth_token(self, expiration=60*60):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            print('expired')
            data = e.payload
            return None  # valid token, but expired
        except BadSignature:
            print('invalid')
            return None  # invalid token
        user = Manager.query.get(data['id'])
        return user

    def serializer(self):
        from utils.qiniu_util import get_upload_token
        upload_token = get_upload_token()
        return {
            "user_open_id":self.user_open_id,
            'name': self.name,
            'token': self.generate_auth_token().decode('ascii'),
            'image_upload_token': upload_token[1],
            'audio_upload_token': upload_token[0]
        }