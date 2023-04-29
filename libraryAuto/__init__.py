from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from libraryAuto.config import Config
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
db = SQLAlchemy()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from libraryAuto.main.routes import main
    app.register_blueprint(main)
    
    return app


