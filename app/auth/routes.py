"""
Routes for logging user in and out
- login(): login page. Checks if user is logged in and if not redirects to log in  page
- logout(): logs out user
- password_change(): changes current user's password
- admin_password_change(): changes chosen user's password. Admin only
"""

#-*- coding: utf-8 -*-
# pylint: disable=no-member

from flask import url_for, redirect, flash, request, render_template
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm, PasswordChangeForm, AdminPasswordChangeForm
from app.auth.workers_for_admin_pswd_change import users_for_admin


# Login page. Checks if user is logged in and if not redirects to log in page
@bp.route("/login", methods=["GET", "POST"])
def login():
    """Logs user in."""

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Nieprawidłowa nazwa użytkownika lub hasło")
            return redirect(url_for("main.index"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title="Grafiki - logowanie", form=form)


#  Logs out user
@bp.route("/logout")
@login_required
def logout():
    """Logs out current user."""

    logout_user()
    return redirect(url_for("main.index"))


# changes current user's password
@bp.route("/password-change", methods=["GET", "POST"])
@login_required
def password_change():
    """
    :return: main page, password for current user changed
    """
    user = request.args.get("user")
    form = PasswordChangeForm()

    if form.validate_on_submit():
        worker = User.query.filter_by(username=user).first()
        if worker.check_password(form.old_password.data):
            worker.set_password(form.new_password1.data)
            db.session.commit()
            flash("Hasło zmienione")
            return redirect(url_for("main.index"))

        flash("Nieprawidłowe obecne hasło")
        return redirect(url_for("auth.password_change", user=current_user))

    return render_template("auth/password_change.html", title="Grafiki - zmiana hasła", user=user, form=form)


# changes chosen user's password. Admin only
@bp.route("/admin-password-change", methods=["GET", "POST"])
@login_required
def admin_password_change():
    """
    :return: main page, password for current user changed
    """
    form = AdminPasswordChangeForm()
    form.worker.choices = users_for_admin()

    if form.validate_on_submit():
        print("dupa")
        worker = User.query.filter_by(username=form.worker.data).first()
        print(worker)
        worker.set_password(form.new_password1.data)
        db.session.commit()
        flash("Hasło zmienione")
        return redirect(url_for("main.index"))

    return render_template("auth/admin_password_change.html", title="Grafiki - zmiana hasła", form=form)
