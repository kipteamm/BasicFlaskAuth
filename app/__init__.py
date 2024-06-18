from flask_login import LoginManager

from flask_migrate import Migrate

from flask import Flask, flash, redirect, url_for

from app.auth.models import User
from app.auth.views import auth_blueprint
from app.main.views import main_blueprint
from app.extensions import db


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisisasecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager(app)

    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))

    return app
