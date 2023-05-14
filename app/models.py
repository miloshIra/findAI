import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from .utils_db import ResourceMixin
from collections import OrderedDict

'use: flask db migrate -m ''comment'' to migrate model changes'
'use: flask db upgrade to apply migration'


@login.user_loader
def load_user(id):
    return User.query.get(id)


class Company(db.Model, ResourceMixin):

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(64), index=True, unique=True)
    contact = db.Column(db.String(65))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('User', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Company {}>'.format(self.name)


class User(UserMixin, ResourceMixin, db.Model):
    ROLE = OrderedDict([
        ('member', 'Member'),
        ('subscriber', 'Subscriber'),
        ('admin', 'Admin')
    ])

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False),
                     index=True, nullable=False, server_default='member')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, server_default='')
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'), index=True, nullable=True)
    services = db.Column(ARRAY(db.String(256)))

    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_ip = db.Column(db.String(45))

    def __repr__(self):
        return '<User {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def initialize_password_reset(cls, email):
        user = User.query.filter_by(email=email).first()
        return user


class ModelIdea(db.Model, ResourceMixin):

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    category = db.Column(db.String(32))
    description = db.Column(db.Text())
    name = db.Column(db.String(32))


class Entry(db.Model, ResourceMixin):

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    image = db.Column(db.LargeBinary)
    service = db.Column(db.String(32), index=True)
    image_result = db.Column(db.LargeBinary, nullable=True)






