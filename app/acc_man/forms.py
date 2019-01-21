#-*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import User, Shop


class NewUserForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    password2 = PasswordField("Powtórz hasło", validators=[DataRequired(message="Pole wymagane"), EqualTo("password")])
    access_level = SelectField("Poziom uprawnień", validators=[DataRequired(message="Pole wymagane")],
                               choices=[("3", "podstawowy"), ("2", "kierownik"), ("1", "kierownik działu"),
                                        ("0", "admin")])
    submit = SubmitField("Załóż konto")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Nazwa użytkownika zajęta")


class NewWorkplaceForm(FlaskForm):
    workplace_name = StringField("Kod sklepu", validators=[DataRequired(message="Pole wymagane")])
    submit = SubmitField("Stwórz sklep")

    def validate_shopname(self, shopname):
        shop = Shop.query.filter_by(shopname=shopname.data).first()
        if shop is not None:
            raise ValidationError("Kod sklepu zajęty")


class UserToShopForm(FlaskForm):
    workplace = SelectField("Wybierz sklep")
    worker = SelectField("Wybierz użytkownika")
    submit = SubmitField("Przydziel")

