from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<int:user_id>')
@login_required
def index(user_id):
    return render_template('user/index.html', user=current_user)
