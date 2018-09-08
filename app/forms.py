from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Shop
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class LoginForm(FlaskForm):
    username = StringField("Użytkownik", validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField("Zapamiętaj")
    submit = SubmitField("Zaloguj")

class NewUserForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[DataRequired(message="Pole wymagane")])
    email = StringField("E-mail", validators=[DataRequired(message="Pole wymagane"), Email("Nieprawidłowy adres e-mail")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    password2 = PasswordField("Powtórz hasło", validators=[DataRequired(message="Pole wymagane"), EqualTo("password")])
    access_level = SelectField("Poziom uprawnień", validators=[DataRequired(message="Pole wymagane")], choices=[("u","podstawowy"), ("m" ,"kierownik"), ("a", "admin")])
    submit = SubmitField("Załóż konto")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Nazwa użytkownika zajęta")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Adres e-mail zajęty")

class NewShopForm(FlaskForm):
    shopname = StringField("Kod sklepu", validators=[DataRequired(message="Pole wymagane")])
    submit = SubmitField("Stwórz sklep")

    def validate_shopname(self, shopname):
        shop = Shop.query.filter_by(shopname=shopname.data).first()
        if shop is not None:
            raise ValidationError("Kod sklepu zajęty")


class UserToShopForm(FlaskForm):
    def shops_list():
        return Shop.query.all()

    def users_list():
        return User.query.all()

    shop = QuerySelectField("Wybierz sklep", query_factory=shops_list)
    user = QuerySelectField("Wybierz użytkownika", query_factory=users_list)
    submit = SubmitField("Przydziel")
