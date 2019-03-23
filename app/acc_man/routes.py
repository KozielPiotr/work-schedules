"""
Managing users accounts, workplaces and connections between them
- new_user: creates new user
- new_workplace: creates new workplace
- worker_to_workplace: assigns user to the workplace
- worker_to_workplace_workers: jsonifies data for dynamically generated checkboxes in worker_to_workplace()
"""

#-*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template, jsonify, request
from flask_login import login_required

from app import db
from app.models import User, Shop
from app.access_test import acc_test
from app.acc_man import bp
from app.acc_man.forms import NewUserForm, NewWorkplaceForm, UserToShopForm
from app.acc_man.assign_worker import assign_worker


# New user
@bp.route("/new-user", methods=["GET", "POST"])
@login_required
def new_user():
    """
    Adds new user to database.
    """
    if acc_test.check_access(0) is False:
        return redirect(url_for("main.index"))

    form = NewUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, access_level=form.access_level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Nowy użytkownik zarejestrowany")
        return redirect(url_for("acc.new_user"))
    return render_template("acc_man/new_user.html", title="Grafiki - nowy użytkownik", form=form)


# New workplace
@bp.route("/new-workplace", methods=["GET", "POST"])
@login_required
def new_workplace():
    """
    Adds new workplace to database.
    """
    if acc_test.check_access(0) is False:
        return redirect(url_for("main.index"))

    form = NewWorkplaceForm()
    if form.validate_on_submit():
        workplace = Shop(shopname=form.workplace_name.data)
        db.session.add(workplace)
        db.session.commit()
        flash("Stworzono nowy sklep")
        return redirect(url_for("main.index"))
    return render_template("acc_man/new_workplace.html", title="Grafiki - nowy sklep", form=form)


# Assigns user to the workplace
@bp.route("/workplace-worker-connect", methods=["GET", "POST"])
@login_required
def worker_to_workplace():
    """
    Allows to manage connections between workers and workplaces.
    """
    if acc_test.check_access(0) is False:
        return redirect(url_for("main.index"))

    form = UserToShopForm()
    assign_worker(form)
    workplaces = Shop.query.order_by(Shop.shopname).all()

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
    return render_template("acc_man/worker_to_workplace.html", title="Grafiki - przydzielanie użytkownika do sklepu",
                           form=form, workplaces=workplaces)


# Jsonifies data for dynamically generated checkboxes in worker_to_workplace()
@bp.route("/workplace-worker-connect/<workplace>")
@login_required
def worker_to_workplace_workers(workplace):
    """
    Makes list of workers unassigned to chosen workplace
    :param workplace: chosen workplace
    :return: list of workers
    """
    if acc_test.check_access(0) is False:
        return redirect(url_for("main.index"))

    shop = Shop.query.filter_by(shopname=workplace).first()
    workers_appended = shop.works.all()
    workers_all = User.query.order_by(User.username).all()
    workers = []
    for worker in workers_all:
        if worker not in workers_appended:
            workers.append(worker)
    jsondict = []
    for worker in workers:
        workers_list = {"name": worker.username}
        jsondict.append(workers_list)
    return jsonify({"workers": jsondict})


# removes connection between worker and workplace
@bp.route("/remove-user-from-shop", methods=["GET", "POST"])
@login_required
def remove_from_shop():
    """
    Removes link between worker and workplace.
    """
    if acc_test.check_access(0) is False:
        return redirect(url_for("main.index"))

    user = request.args.get("user")
    workplace = request.args.get("workplace")
    found_user = User.query.filter_by(username=user).first()
    found_workplace = Shop.query.filter_by(shopname=workplace).first()
    found_workplace.works.remove(found_user)
    db.session.commit()
    flash("Usunięto %s z %s" % (user, workplace))
    return redirect(url_for("acc.worker_to_workplace"))
