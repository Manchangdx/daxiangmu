from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import configs
from .models import db, User, Course

def register_blueprints(app):
    from .handlers import front, admin, course
    for i in (admin, front, course):
        app.register_blueprint(i)

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    l = LoginManager()
    l.init_app(app)

    @l.user_loader
    def user_loader(id):
        return User.query.get(id)

    l.login_view = 'front.login'

def create_app(c):
    app = Flask(__name__)
    app.config.from_object(configs.get(c))
    register_blueprints(app)
    register_extensions(app)
    return app
