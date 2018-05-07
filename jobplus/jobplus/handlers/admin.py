from flask import (Blueprint, render_template, request, current_app,
     redirect, url_for, flash)
from jobplus.decorators import admin_required
from jobplus.models import User, db

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/user')
@admin_required
def user():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)


@admin.route('/users/<int:user_id>/disable')
@admin_required
def disable_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_disable:
        user.is_disable = False
        flash('该用户已启用', 'success')
    else:
        user.is_disable = True
        flash('该用户已禁用', 'info')
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('.user'))
