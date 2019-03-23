"""Functions for new_schedule route"""

#-*- coding: utf-8 -*-

from calendar import Calendar
from flask import flash, redirect, url_for, render_template
from flask_login import current_user

from app import MONTH_NAMES, WEEKDAY_NAMES
from app.models import User, Shop, Schedule, Billing_period, Guidelines
from app.schedules.prev_schedule import prev_schedule


def ns_choices(form):
    """
    Fills forms selectfield choices
    :param form: form
    """
    workplaces = []
    workers_list = []
    c_user = User.query.filter_by(username=str(current_user)).first()
    for workplace in c_user.workers_shop:
        workplaces.append((str(workplace), str(workplace)))
    form.workplace.choices = workplaces

    for worker in User.query.order_by(User.access_level).all():
        workers_list.append((str(worker), str(worker)))
    form.workers.choices = workers_list


def ns_form_validate(form):
    """
    :param form: form
    :return: template with all necessary data for new schedule or error message
    """
    workplace = form.workplace.data
    year = int(form.year.data)
    month = int(form.month.data)
    hours = form.hours.data
    month_name = MONTH_NAMES[month - 1]

    schedule_name = "%s-%s-%s" % (year, month, workplace)
    check_schedule = Schedule.query.filter_by(name=schedule_name).first()
    if check_schedule is not None:
        flash("Taki grafik już istnieje")
        return redirect(url_for("schedules.new_schedule"))

    workers_to_schd = []
    for worker in form.workers.data:
        workers_to_schd.append(str(worker).replace(" ", "_"))

    prev = prev_schedule(month, year, workplace)

    cal = Calendar()
    return render_template("schedules/empty_schedule.html", title="Grafiki - nowy grafik",
                           workers=workers_to_schd, shop=workplace, year=year, month=month, mn=month_name,
                           cal=cal, wdn=WEEKDAY_NAMES, hours=hours, Billing_period=Billing_period,
                           prev_shdict=prev["prev_shdict"], prev_month=prev["month"],
                           prev_month_name=prev["month_name"], prev_year=prev["year"],
                           prev_hours=prev["hours"], prev_workers=prev["workers"],
                           workers_hours=prev["workers_hours"], Shop=Shop, Guidelines=Guidelines)
