#-*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class UploadFile(FlaskForm):
    file = FileField("Wczytaj plik")
    submit = SubmitField("Zatwierdź")
