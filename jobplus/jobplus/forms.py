from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
    ValidationError, IntegerField, TextAreaField)
from wtforms.validators import Length, Email, EqualTo, DataRequired
from .models import db, User, CompanyDetail, Resume, Job

class RegisterForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired(), Length(3, 32)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_name(self, f):
        if User.query.filter_by(name=f.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, f):
        if User.query.filter_by(email=f.data).first():
            raise ValidationError('邮箱已经被注册')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    name = StringField('用户名 / 邮箱', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_name(self, f):
        u1 = User.query.filter_by(name=f.data).first()
        u2 = User.query.filter_by(email=f.data).first()
        if not u1 and not u2:
            raise ValidationError('用户名或邮箱不存在')

    def validate_password(self, f):
        user = User.query.filter_by(name=self.name.data).first()
        if not user:
            user = User.query.filter_by(email=self.name.data).first()
        if user and not user.check_password(f.data):
            raise ValidationError('密码错误')


class ResumeForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(2, 24)])
    age = IntegerField('年龄', validators=[DataRequired()])
    work_age = IntegerField('工龄', validators=[DataRequired()])
    home_city = StringField('家乡城市', validators=[DataRequired()])
    job_experience = TextAreaField('工作经历')
    edu_experience = TextAreaField('教育经历')
    pro_experience = TextAreaField('项目经历')
    submit = SubmitField('提交')

    def get_resume(self, resume):
        self.populate_obj(resume)
        db.session.add(resume)
        db.session.commit()
        return resume
