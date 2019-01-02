"""
Routes for logging user in and out
"""

#-*- coding: utf-8 -*-

from flask import url_for, redirect, flash, request, render_template
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm


# Login page. Checks if user is logged in and if not redirects to log in  page
@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs user in.
    """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Nieprawidłowa nazwa użytkownika lub hasło")
            return redirect(url_for("index"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("auth/login.html", title="Grafiki - logowanie", form=form)


#  Logging out user
@bp.route("/logout")
@login_required
def logout():
    """
    Logs out current user.
    """
    logout_user()
    return redirect(url_for("index"))
