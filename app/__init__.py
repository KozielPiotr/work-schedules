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
MONTH_NAMES = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień",
               "Wrzesień", "Październik", "Listopad", "Grudzień"]
WEEKDAY_NAMES = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.acc_man import bp as acc_man_bp
app.register_blueprint(acc_man_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app.billing_period import bp as b_per_bp
app.register_blueprint(b_per_bp)

from app.schedules import bp as schedules_bp
app.register_blueprint(schedules_bp)

from app.xlsx import bp as xlsx_bp
app.register_blueprint(xlsx_bp)

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app import models
