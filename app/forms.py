#-*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Shop
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput



class LoginForm(FlaskForm):
    username = StringField("Użytkownik", validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    remember_me = BooleanField("Zapamiętaj")
    submit = SubmitField("Zaloguj")


class NewUserForm(FlaskForm):
    username = StringField("Nazwa użytkownika", validators=[DataRequired(message="Pole wymagane")])
    password = PasswordField("Hasło", validators=[DataRequired(message="Pole wymagane")])
    password2 = PasswordField("Powtórz hasło", validators=[DataRequired(message="Pole wymagane"), EqualTo("password")])
    access_level = SelectField("Poziom uprawnień", validators=[DataRequired(message="Pole wymagane")],
                               choices=[("3","podstawowy"), ("2" ,"kierownik"), ("1", "kierownik działu"),
                                        ("0", "admin")])
    submit = SubmitField("Załóż konto")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Nazwa użytkownika zajęta")


class NewShopForm(FlaskForm):
    shopname = StringField("Kod sklepu", validators=[DataRequired(message="Pole wymagane")])
    submit = SubmitField("Stwórz sklep")

    def validate_shopname(self, shopname):
        shop = Shop.query.filter_by(shopname=shopname.data).first()
        if shop is not None:
            raise ValidationError("Kod sklepu zajęty")


class UserToShopForm(FlaskForm):
    workplace = SelectField("Wybierz sklep")
    worker = SelectField("Wybierz użytkownika")
    submit = SubmitField("Przydziel")


class BooleanSubField(BooleanField):
    def process_data(self, value):
        if isinstance(value, BooleanField):
            self.data = value.data
        else:
            self.data = bool(value)


class BillingPeriod(FlaskForm):
    begin_month = SelectField("Początek okresu rozliczeniowego", choices=(("1", "Styczeń"), ("2", "Luty"),("3", "Marzec"), ("4", "Kwiecień"),
                                            ("5", "Maj"), ("6", "Czerweiec"), ("7", "Lipiec"), ("8", "Sierpień"),
                                            ("9", "Wrzesień"), ("10", "Październik"), ("11", "Listopad"),
                                            ("12", "Grudzień")))
    begin_year = IntegerField("Rok: ", [DataRequired(message="Wprowadź rok")])
    length_of_billing_period = IntegerField("Długość okresu rozliczeniowego (w miesiącach)")
    submit = SubmitField("Zatwierdź")


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class NewScheduleForm(FlaskForm):
    workplace = SelectField("Sklep: ")
    year = IntegerField("Rok: ", [DataRequired(message="Wprowadź rok")])
    month = SelectField("Miesiąc: ", choices=(("1", "Styczeń"), ("2", "Luty"), ("3", "Marzec"), ("4", "Kwiecień"),
                                            ("5", "Maj"), ("6", "Czerweiec"), ("7", "Lipiec"), ("8", "Sierpień"),
                                            ("9", "Wrzesień"), ("10", "Październik"), ("11", "Listopad"),
                                            ("12", "Grudzień")))
    workers = MultiCheckboxField("Pracownicy: ")
    hours = IntegerField("Ilość roboczogodzin")
    submit = SubmitField("Nowy grafik", [DataRequired(message="Wprowadź ilość godzin")])