"""
Managing users accounts, workplaces and connections between them
"""

#-*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from app import db
from app.acc_man import bp
from app.acc_man.forms import NewUserForm, NewShopForm, UserToShopForm
from app.models import User, Shop


#  New user
@bp.route("/new-user", methods=["GET", "POST"])
@login_required
def new_user():
    """
    Adds new user to database.
    """
    if current_user.access_level != "0" and current_user.access_level != "1":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    form = NewUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, access_level=form.access_level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Nowy użytkownik zarejestrowany")
        return redirect(url_for("acc.new_user"))
    return render_template("new_user.html", title="Grafiki - nowy użytkownik", form=form)


# New workplace
@bp.route("/new-shop", methods=["GET", "POST"])
@login_required
def new_shop():
    """
    Adds new workplace to database.
    """
    if current_user.access_level != "0" and current_user.access_level != "1":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    form = NewShopForm()
    if form.validate_on_submit():
        shop = Shop(shopname=form.shopname.data)
        db.session.add(shop)
        db.session.commit()
        flash("Stworzono nowy sklep")
        return redirect(url_for("index"))
    return render_template("new_shop.html", title="Grafiki - nowy sklep", form=form)


# Assigns user to the shop
@bp.route("/workplace-worker-connect", methods=["GET", "POST"])
@login_required
def worker_to_workplace():
    """
    Allows to manage connections between workers and workplaces.
    """
    if current_user.access_level != "0" and current_user.access_level != "1":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    form = UserToShopForm()
    workplaces = Shop.query.order_by(Shop.shopname).all()
    workplaces_list = []
    for workplace in workplaces:
        workplaces_list.append((str(workplace), str(workplace)))
    form.workplace.choices = workplaces_list

    workers = User.query.order_by(User.username).all()
    workers_list = []
    for worker in workers:
        workers_list.append((str(worker), str(worker)))
    form.worker.choices = workers_list

    users_number = len(workers_list)
    if form.validate_on_submit():
        worker = User.query.filter_by(username=form.worker.data).first()
        workplace = Shop.query.filter_by(shopname=form.workplace.data).first()
        already_assigned = workplace.works
        if worker not in already_assigned:
            workplace.works.append(worker)
            db.session.commit()
            flash("Przypisano %s do %s" % (worker, workplace))
        else:
            flash("%s był już przypisany do %s" % (worker, workplace))
        return redirect(url_for("acc.worker_to_workplace"))
    return render_template("worker_to_workplace.html", title="Grafiki - przydzielanie użytkownika do sklepu",
                           form=form, workplaces=workplaces, users_number=users_number)
