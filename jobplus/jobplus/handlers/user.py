from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from jobplus.models import User, Resume, db, CompanyDetail
from jobplus.forms import ResumeForm

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<int:user_id>')
@login_required
def profile(user_id):
    resume = current_user.resume
    return render_template('user/profile.html', resume=resume)

@user.route('/<int:user_id>/edit_resume', methods=['GET', 'POST'])
@login_required
def edit_resume(user_id):
    resume = Resume.query.join(User).filter(User.id==user_id).first()
    if not resume:
        resume = Resume(
            user=User.query.filter_by(id=user_id).first(),
            name='周杰伦',
            age=22,
            work_age=1,
            home_city='布拉格'
        )
    form = ResumeForm(obj=resume)
    if form.validate_on_submit():
        print('------------------------------ok')
        form.get_resume(resume)
        flash('简历已更新~', 'warning')
        return redirect(url_for('.profile', user_id=current_user.id))
    return render_template('user/edit_resume.html', form=form)
