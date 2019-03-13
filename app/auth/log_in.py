"""Logs user in"""

from flask import url_for, request, flash
from flask_login import login_user
from werkzeug.urls import url_parse
from app.models import User

#-*- coding: utf-8 -*-

def login_to_page(remember, user_name, user_password):
    user = User.query.filter_by(username=user_name).first()
    if user is None or not user.check_password(user_password):
        flash("Nieprawidłowa nazwa użytkownika lub hasło")
        return url_for("main.index")
    login_user(user, remember=remember)
    next_page = request.args.get("next")
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for("main.index")
    return next_page
