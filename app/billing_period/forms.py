#-*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class BillingPeriod(FlaskForm):
    begin_month = SelectField("Początek okresu rozliczeniowego", choices=(("1", "Styczeń"), ("2", "Luty"),
                                                                          ("3", "Marzec"), ("4", "Kwiecień"),
                                                                          ("5", "Maj"), ("6", "Czerweiec"),
                                                                          ("7", "Lipiec"), ("8", "Sierpień"),
                                                                          ("9", "Wrzesień"), ("10", "Październik"),
                                                                          ("11", "Listopad"), ("12", "Grudzień")))
    begin_year = IntegerField("Rok: ", [DataRequired(message="Wprowadź rok")])
    length_of_billing_period = IntegerField("Długość okresu rozliczeniowego (w miesiącach)")
    submit = SubmitField("Zatwierdź")