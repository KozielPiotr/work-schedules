"""Functions for new_schedule_to_db route"""

#-*- coding: utf-8 -*-

from datetime import date
from flask import redirect, url_for
from app import db
from app.models import Personal_schedule, Schedule
from app.access_test import acc_test


def ind_schedules_to_db(data, schedule, billing_period):
    """
    Adds individual schedule to database.
    :param data: json with all information for every individual schedule
    :param schedule: schedule in db that this personal schedule will be connected
    :param billing_period: billing period to which this personal schedule will belong
    """
    for element in data["ind_schedules"]:
        schd_date = date(int(element["year"]), int(element["month"]), int(element["day"]))
        worker = element["worker"].replace("_", " ")
        b_hour = element["from"]
        e_hour = element["to"]
        h_sum = element["sum"]
        event = element["event"]
        workplace = element["workplace"]
        ps_name = "%s-%s-%s" % (schd_date, worker, workplace)
        billing_week = element["billing_week"]
        ps_schedule = Personal_schedule(name=ps_name, date=schd_date, worker=worker, begin_hour=b_hour,
                                        end_hour=e_hour, hours_sum=h_sum, event=event, workplace=workplace,
                                        includes=schedule, billing_period=billing_period, billing_week=billing_week)
        db.session.add(ps_schedule)


def create_unaccepted_version(data):
    """
    Creates new unaccepted schedule
    :param data: json with all information for every individual schedule
    """
    name = "%s-%s-%s" % (data["main_data"]["year"], data["main_data"]["month"], data["main_data"]["workplace"])
    year = int(data["main_data"]["year"])
    month = int(data["main_data"]["month"])
    workplace = data["main_data"]["workplace"]
    hours = data["main_data"]["hours"]
    billing_period = int(data["main_data"]["billing_period"])
    version = int(data["main_data"]["version"])
    schedule = Schedule(name=name, year=year, month=month, workplace=workplace, hrs_to_work=hours,
                        accepted=False, version=version, billing_period=billing_period)
    db.session.add(schedule)

    ind_schedules_to_db(data, schedule, billing_period)
    db.session.commit()


def create_new_unaccepted_version(data):
    """
    Creates unaccepted version of existing schedule
    :param data: json with all information for every individual schedule
    """
    if acc_test.check_access(1) is False:
        return redirect(url_for("main.index"))

    unaccepted_schedule = Schedule.query.filter_by(
        name="%s-%s-%s" % (data["main_data"]["year"], data["main_data"]["month"],
                           data["main_data"]["workplace"]), accepted=False).first()

    name = unaccepted_schedule.name
    year = unaccepted_schedule.year
    month = unaccepted_schedule.month
    workplace = unaccepted_schedule.workplace
    hours = unaccepted_schedule.hrs_to_work
    accepted = True
    version = unaccepted_schedule.version + 1
    billing_period = unaccepted_schedule.billing_period
    schedule = Schedule(name=name, year=year, month=month, workplace=workplace, hrs_to_work=hours,
                        accepted=accepted, version=version, billing_period=billing_period)
    db.session.add(schedule)

    ind_schedules_to_db(data, schedule, billing_period)
    db.session.commit()

    for ind_schedule in unaccepted_schedule.ind:
        db.session.delete(ind_schedule)
    db.session.delete(unaccepted_schedule)
    db.session.commit()


def add_schedule_to_db(action, data):
    """
    dds schedule to database
    """
    if action in ("send_v_0", "modify_existing"):
        create_unaccepted_version(data)
    elif action == "accept_new_v":
        create_new_unaccepted_version(data)
