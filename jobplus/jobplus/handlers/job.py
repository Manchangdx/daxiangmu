from flask import (Blueprint, render_template, redirect, url_for, flash,
    abort, current_app, request)
from flask_login import current_user, login_required
from jobplus.models import db, User, Job, Delivery

job = Blueprint('job', __name__, url_prefix='/job')

@job.route('/')
def index():
    page  = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['JOB_PER_PAGE'],
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination)

@job.route('/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job)

@job.route('/<int:job_id>/apply')
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if job.current_user_is_applied:
        flash('已投递过该职位', 'info')
    else:
        d = Delivery(
            job_id=job_id,
            resume_id=current_user.id
        )
        db.session.add(d)
        db.session.commit()
        flash('投递成功~', 'success')
    return redirect(url_for('job.detail', job_id=job.id))

@job.route('/<int:job_id>/status')
@login_required
def status(job_id):
    job = Job.query.get_or_404(job_id)
    if not current_user.is_admin and current_user.id != job.user.id:
        abort(404)
    if job.is_disable:
        job.is_disable = False
        flash('职位上线成功', 'success')
    else:
        job.is_disable = True
        flash('职位下线成功', 'info')
    db.session.add(job)
    db.session.commit()
    return redirect(url_for('admin.job'))
