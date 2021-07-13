from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

# Create app
app = Flask(__name__, instance_relative_config=False)
app.config.from_object("config.DevelopmentConfig")
# Database
db = SQLAlchemy(app)
# Login
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    # Import Blueprints
    from .login.routes import login
    from .shorter.routes import shorter

    # Register Blueprints
    app.register_blueprint(login)
    app.register_blueprint(shorter)
