import uuid
from datetime import datetime
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


class Company(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), index=True, unique=True)
    contact = db.Column(db.String(65))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Company {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'), index=True, nullable=True)
    services = db.Column(ARRAY(db.String(256)))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class AIService(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    counter = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

