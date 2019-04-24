from flask import current_app
from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from sqlalchemy import text
roles = db.Table('roles',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                 db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                 )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    hash_password = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, nullable=False, server_default='0')
    roles = db.relationship('Role', secondary=roles, lazy='dynamic', backref=db.backref('users', lazy=True))
    create_time = db.Column(db.DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    def set_hash_password(self, password: str):
        self.hash_password = generate_password_hash(self.name + password)

    def verify_password(self, password: str):
        return check_password_hash(self.hash_password, self.name + password)

    def __repr__(self):
        return f'<User> [name]{self.name} [open_id]{self.user_open_id}'

    def generate_auth_token(self, expiration=60 * 60):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def generate_refresh_token(self, expiration=30 * 24 * 60 * 60):
        s = TimedJSONWebSignatureSerializer(current_app.config['REFRESH_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id, 'hash': self.hash_password})

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
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def verify_refresh_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['REFRESH_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            print('expired')
            return None  # valid token, but expired
        except BadSignature:
            print('invalid')
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def serializer(self):
        return {
            'name': self.name,
            'token': self.generate_auth_token().decode('ascii'),
            "is_admin": self.is_admin,
        }


menus = db.Table('menus',
                 db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
                 db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'), primary_key=True)
                 )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menus = db.relationship('Menu', secondary=menus, lazy='subquery', backref=db.backref('roles', lazy=True))
    name = db.Column(db.String(30))

    def __repr__(self):
        return f'[name]:{self.name}'

    def serializer(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('menu.id', ondelete='SET NULL', ))
    name = db.Column(db.String(30))
    url = db.Column(db.String(100))
    child = None

    def __repr__(self):
        return f'[name]:{self.name} [url]:{self.url}'

    def serializer(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }

    @staticmethod
    def make_tree(menu_list):
        data = {menu.id: menu for menu in menu_list}
        result = []
        for menu in menu_list:
            if menu.parent_id in data.keys():
                parent = data[menu.parent_id]
                if not parent.child:
                    parent.child = [menu]
                else:
                    parent.child.append(menu)
            else:
                result.append(menu)
        return [menu.generate_tree() for menu in result]

    def generate_tree(self):
        data = self.serializer()
        if self.child:
            data['child'] = [child.generate_tree() for child in self.child]
        else:
            data['child'] = None
        return data
