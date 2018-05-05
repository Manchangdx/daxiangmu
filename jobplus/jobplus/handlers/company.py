from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/<int:company_id>')
@login_required
def index(company_id):
    return render_template('company/index.html', company=current_user)
