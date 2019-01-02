#-*- coding: utf-8 -*-

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Użytkownik", validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField("Zapamiętaj")
    submit = SubmitField("Zaloguj")