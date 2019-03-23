"""Adds user to schedule"""

#-*- coding: utf-8 -*-

from calendar import Calendar
from datetime import date
from flask import flash

from app import db
from app.models import Shop, Personal_schedule


def add_user_to_sched(schedule, worker):
    """
    adds new user to schedule
    :param schedule: selected schedule
    :param worker: worker to add
    """
    worker = worker
    cal = Calendar()
    workplace = schedule.workplace

    schedule_workers = []
    for ind_schedule in schedule.ind:
        if ind_schedule.worker not in schedule_workers:
            schedule_workers.append(ind_schedule.worker)

    workers = []
    for employee in Shop.query.filter_by(shopname=workplace).first().works.all():
        workers.append(str(employee))

    if worker in workers and worker not in schedule_workers:
        for day in cal.itermonthdays(schedule.year, schedule.month):
            if day > 0:
                schedule_date = date(schedule.year, schedule.month, day)
                name = "%s-%s-%s" % (schedule_date, worker, schedule.workplace)
                pers_schedule = Personal_schedule(name=name, date=schedule_date, worker=worker, begin_hour=0,
                                                  end_hour=0, hours_sum=0, event="off", workplace=workplace,
                                                  includes_id=schedule.id)
                db.session.add(pers_schedule)
        db.session.commit()
    elif worker not in workers:
        flash("Taki pracownik nie jest przypisany do tego miejsa pracy")
    elif worker in schedule_workers:
        flash("Taki pracownik jest już w tym grafiku")
