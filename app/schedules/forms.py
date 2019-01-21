#-*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput

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
