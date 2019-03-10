"""creates dictionary with data to make modifiable template with schedule"""

#-*- coding: utf-8 -*-

from calendar import Calendar
from datetime import datetime
from flask import redirect, url_for, flash, request
from flask_login import current_user
from app import MONTH_NAMES
from app.models import Schedule, Personal_schedule
from app.schedules import prev_schedule


def acc_mod_schd(action):
    """
    :param action: action
    :return: dictionary with data to render template in route
    """
    title = "Grafiki"
    schedule = None
    if action == "to_accept":
        if (current_user.access_level != "0") and (current_user.access_level != "1"):
            flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
            return redirect(url_for("main.index"))
        schedule = Schedule.query.filter_by(name=request.args.get("schd"), version=int(request.args.get("v")),
                                            accepted=False).first()
        title = "Grafiki - akceptacja grafiku"
    elif action == "to_modify":
        if (current_user.access_level != "0") and (current_user.access_level != "1") and \
                (current_user.access_level != "2"):
            flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
            return redirect(url_for("main.index"))
        schedule = Schedule.query.filter_by(name=request.args.get("schd"), version=int(request.args.get("v")),
                                            accepted=True).first()
        title = "Grafiki - modyfikacja grafiku"
    if not schedule:
        flash("Nie ma takiego grafiku")
        return redirect(url_for("schedules.accept_modify_schedule"))

    schedule_id = schedule.id
    workplace = schedule.workplace
    year = schedule.year
    month = schedule.month
    hours = schedule.hrs_to_work
    version = schedule.version
    workers = []
    for pers_schedule in schedule.ind:
        if str(pers_schedule.worker).replace(" ", "_") not in workers:
            workers.append(str(pers_schedule.worker).replace(" ", "_"))

    month_name = MONTH_NAMES[month - 1]

    prev = prev_schedule.prev_schedule(month, year, workplace)

    shdict = {}
    for worker in workers:
        for day in Calendar().itermonthdays(year, month):
            if day > 0:
                begin = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schedule_id,
                                                          worker=worker.replace("_", " ")).first().begin_hour
                end = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schedule_id,
                                                        worker=worker.replace("_", " ")).first().end_hour
                event = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schedule_id,
                                                          worker=worker.replace("_", " ")).first().event
                if begin == 0:
                    begin = ""
                shdict["begin-%s-%d-%02d-%02d" % (worker, year, month, day)] = begin
                if end == 0:
                    end = ""
                shdict["end-%s-%d-%02d-%02d" % (worker, year, month, day)] = end
                shdict["event-%s-%d-%02d-%02d" % (worker, year, month, day)] = event

    schedules = {"prev": prev, "shdict": shdict, "schedule_id": schedule.id, "workplace": workplace, "year": year,
                 "month": month, "month_name": month_name, "workers": workers, "hours": hours, "version": version,
                 "title": title}
    return schedules
