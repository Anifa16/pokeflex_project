from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

# Initializing Packages
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app():
    # Init app
    app = Flask(__name__)

    # Link the config
    app.config.from_object(Config)

    # Register Packages
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # Configure Login Settings
    login.login_view = 'auth.login'
    login.login_message = 'You must log in to access this page.'
    login.login_message_category = 'warning'

    # Importing Blueprints
    from .blueprints.main import main
    from .blueprints.auth import auth
    from .blueprints.post import post

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(post)

    return app