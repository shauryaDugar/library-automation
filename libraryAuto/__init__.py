from flask import Flask
from flask_mail import Mail
from libraryAuto.config import Config

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)

    from libraryAuto.main.routes import main
    app.register_blueprint(main)
    
    return app


