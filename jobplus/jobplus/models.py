from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class User(Base, UserMixin):
    ROLE_USER = 11
    ROLE_COMPANY = 22
    ROLE_ADMIN = 33
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(128), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    resume = db.relationship('Resume', 
        uselist=False, 
        cascade='all, delete-orphan', 
        backref='user'
    )
    companydetail = db.relationship('CompanyDetail', 
        uselist=False,
        cascade='all, delete-orphan',
        backref='user'
    )
    jobs = db.relationship('Job', cascade='all, delete-orphan', backref='user')

    def __repr__(self):
        return '<User: {}>'.format(self.name)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, p):
        self._password = generate_password_hash(p)

    def check_password(self, p):
        return check_password_hash(self._password, p)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class Resume(Base):
    id = db.Column(db.Integer, 
        db.ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True
    )
    name = db.Column(db.String(32), nullable=False)
    age = db.Column(db.SmallInteger, nullable=False)
    work_age = db.Column(db.SmallInteger)
    home_city = db.Column(db.String(64))
    job_experience = db.Column(db.Text)
    edu_experience = db.Column(db.Text)
    pro_experience = db.Column(db.Text)


class CompanyDetail(Base):
    id = db.Column(db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        primary_key=True
    )
    image_url = db.Column(db.String(256))
    finance = db.Column(db.String(64))
    staff_num = db.Column(db.String(64))
    type = db.Column(db.String(64))
    about = db.Column(db.Text)

    def __repr__(self):
        return '<CompanyDetail: {}>'.format(self.about[:9])


class Job(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.String(64))
    location = db.Column(db.String(64))
    experience_requirement = db.Column(db.String(64))
    degree_requirement = db.Column(db.String(64))
    is_fulltime = db.Column(db.Boolean, default=True)
    release_time = db.Column(db.String(64))
    is_open = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Job: {}>'.format(self.name)


class Delivery(Base):
    STATUS_WAITING = 11
    STATUS_REJECT = 22
    STATUS_ACCEPT = 33
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=STATUS_WAITING)
    response = db.Column(db.String(256))
