from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Użytkownik", validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField("Zapamiętaj")
    submit = SubmitField("Zaloguj")

class RegistrationForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[DataRequired(message="Pole wymagane")])
    email = StringField("E-mail", validators=[DataRequired(message="Pole wymagane"), Email("Nieprawidłowy adres e-mail")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    password2 = PasswordField("Powtórz hasło", validators=[DataRequired(message="Pole wymagane"), EqualTo("password")])
    submit = SubmitField("Załóż konto")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Nazwa użytkownika zajęta")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Adres e-mail zajęty")
