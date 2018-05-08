from flask import (Blueprint, render_template, url_for, redirect, 
    flash, request, current_app)
from flask_login import login_required, current_user
from jobplus.models import db, User, CompanyDetail

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.filter_by(role=22).paginate(
        page=page,
        per_page=current_app.config['COMPANY_PER_PAGE'],
        error_out=False
    )
    return render_template('company/index.html', pagination=pagination, active='job')

@company.route('/<int:company_id>')
@login_required
def profile(company_id):
    return render_template('company/profile.html')

@company.route('/<int:company_id>/detail')
def detail(company_id):
    company = User.query.get(company_id)
    return render_template('company/detail.html', company=company)
