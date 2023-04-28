from flask import Flask
from flask_mail import Mail
from libraryAuto.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)

    from libraryAuto.main.routes import main
    app.register_blueprint(main)
    
    return app


