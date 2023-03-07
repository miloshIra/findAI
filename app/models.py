import uuid

import flask_login
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

'use: flask db migrate -m ''comment'' to migrate model changes'
'use: flask db upgrade to apply migration'


@login.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    company = db.Column(db.String(128))
    services = db.Column(ARRAY(db.String(256)))

    def __repr__(self):
        return '<User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

