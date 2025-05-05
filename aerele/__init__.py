from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
import os

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    os.makedirs(os.path.join(app.instance_path), exist_ok=True) # create the inventory db in my computer
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'inventry.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_USE_SIGNER'] = True
    db.init_app(app)
    migrate.init_app(app, db)
    Session(app)

    from . import models  #imp the models before migration
    from .routes import main  # import the Blueprint
    app.register_blueprint(main) 
    return app
