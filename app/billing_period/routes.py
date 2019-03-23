"""
Allows to set beginning of counting billing periods and length of it in months.
"""

#-*- coding: utf-8 -*-
# pylint: disable=no-member

from datetime import datetime
from flask import flash, redirect, url_for, render_template
from flask_login import login_required

from app import db
from app.access_test import acc_test
from app.billing_period.forms import BillingPeriod
from app.billing_period import bp
from app.models import Billing_period


# gets beginning and duration of billing period
@bp.route("/billing-period", methods=["GET", "POST"])
@login_required
def billing_period():
    """
    Allows to set beginning of counting billing periods and length of it in months.
    """
    if acc_test.check_access(0) is False:
        return redirect(url_for("main.index"))

    form = BillingPeriod()
    cur_begin = "{: %d - %m - %Y}".format(Billing_period.query.filter_by(id=1).first().begin)
    cur_duration = Billing_period.query.filter_by(id=1).first().duration

    if form.validate_on_submit():
        begin = datetime(int(form.begin_year.data), int(form.begin_month.data), 1)
        duration = form.length_of_billing_period.data

        b_p = Billing_period
        b_p.query.filter_by(id=1).all()[0].begin = begin
        b_p.query.filter_by(id=1).all()[0].duration = duration
        db.session.commit()
        flash("Zmieniono okres rozliczeniowy na: Początek: %s Długość: %s" % ("{:%d - %m - %Y}".format(begin),
                                                                              duration))
        return redirect(url_for("main.index"))
    return render_template("billing_period/billing_period.html", title="Grafiki - okres rozliczeniowy", form=form,
                           cur_begin=cur_begin, cur_duration=cur_duration)
