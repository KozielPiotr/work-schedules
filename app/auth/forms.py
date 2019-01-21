#-*- coding: utf-8 -*-

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Użytkownik", validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField("Zapamiętaj")
    submit = SubmitField("Zaloguj")


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField("Obecne hasło", validators=[DataRequired(message="Pole wymagane")])
    new_password1 = PasswordField("Nowe hasło", validators=[DataRequired(message="Pole wymagane")])
    new_password2 = PasswordField("Powtórz hasło", validators=[DataRequired(message="Pole wymagane"),
                                                               EqualTo("new_password1",
                                                                       message="wprowadzono różne hasła")])
    submit = SubmitField("Zmień hasło")


class AdminPasswordChangeForm(FlaskForm):
    worker = SelectField("Użytkownik")
    new_password1 = PasswordField("Nowe hasło", validators=[DataRequired(message="Pole wymagane")])
    new_password2 = PasswordField("Powtórz hasło", validators=[DataRequired(message="Pole wymagane"),
                                                               EqualTo("new_password1",
                                                                       message="wprowadzono różne hasła")])
    submit = SubmitField("Zmień hasło")
