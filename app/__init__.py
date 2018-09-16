# import os
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment



db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    from app import models
    login_manager.login_message = "You must be logged in to access this page.  Please login."
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbitten'),403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500



    from app.error import error as error_blueprint
    app.register_blueprint(error_blueprint)
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
