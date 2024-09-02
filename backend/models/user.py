from uuid import uuid4
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True, default=uuid4)

    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(192))

    confirmed_at = db.Column(db.DateTime())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    last_updated = db.Column(db.DateTime(), default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'

    def gen_user_id(self):
        if not self.id or not self.id.__len__():
            self.id = str(uuid4())

    def make_identity(self):
        return urlsafe_b64encode(self.id.encode('utf-8')).decode('utf-8')

    @staticmethod
    def get_id_from_identity(identity):
        return urlsafe_b64decode(identity.encode('utf-8')).decode('utf-8')

    def check_login(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'confirmed_at': self.confirmed_at,
            'last_seen': self.last_seen,
            'last_updated': self.last_updated,
            'last_login_at': self.last_login_at,
            'created_at': self.created_at
        }
