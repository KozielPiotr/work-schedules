#-*- coding: utf-8 -*-

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "auth.login"
login.login_message = "Zaloguj się, aby wyświetlić zawartość"

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.acc_man import bp as acc_man_bp
app.register_blueprint(acc_man_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app import routes, models


db.create_all()

