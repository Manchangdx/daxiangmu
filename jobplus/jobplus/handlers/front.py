from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from jobplus.forms import RegisterForm, LoginForm
from jobplus.models import db, User, User, Job

front = Blueprint('front', __name__)

@front.route('/')
def index():
    companies = [User.query.all()[i] for i in [1, 3, 4]]
    jobs = [Job.query.all()[i] for i in [32, 11, 22]]
    return render_template('index.html', companies=companies, jobs=jobs)

@front.route('/userregister', methods=['GET', 'POST'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('用户注册成功，请登录。', 'success')
        return redirect(url_for('.login'))
    return render_template('userregister.html', form=form)

@front.route('/companyregister', methods=['GET', 'POST'])
def companyregister():
    form = RegisterForm()
    form.name.label = u'企业名称'
    if form.validate_on_submit():
        user = form.create_user()
        user.role = User.ROLE_COMPANY
        db.session.add(user)
        db.session.commit()
        flash('公司注册成功，请登录。', 'success')
        return redirect(url_for('.login'))
    return render_template('companyregister.html', form=form)

@front.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user
        if user.is_disable:
            flash('用户已经被禁用', 'info')
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        flash('您已登录成功～', 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)



@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录。', 'info')
    return redirect(url_for('.index'))
