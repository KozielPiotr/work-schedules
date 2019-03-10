"""Prepares data for showing schedule"""

#-*- coding: utf-8 -*-

from calendar import Calendar
from datetime import datetime
from app.models import Schedule, Personal_schedule


def show_schedule_helper(schd, version):
    """
    Creates dictionary with data for chosen schedule
    :param schd: name of schedule
    :param version: version of schedule
    :return: dict with schedule data
    """
    cal = Calendar()
    schedule = Schedule.query.filter_by(name=schd, version=version, accepted=True).first()

    schd_id = schedule.id
    year = schedule.year
    month = schedule.month
    workplace = schedule.workplace
    hours = schedule.hrs_to_work
    version = schedule.version
    schd_dict = {"year": year, "month": month, "workplace": workplace, "hours": hours, "version": version}

    workers = []
    for ind_sched in schedule.ind:
        if str(ind_sched.worker) not in workers:
            workers.append(str(ind_sched.worker))
    schd_dict["workers"] = workers

    workers_hours = {}
    for worker in workers:
        worker_hours = 0
        for ind_sched in schedule.ind:
            if ind_sched.worker == str(worker).replace("_", " "):
                worker_hours += ind_sched.hours_sum
            workers_hours[worker] = worker_hours
        for day in cal.itermonthdays(year, month):
            if day > 0:
                begin = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schd_id,
                                                          worker=worker.replace("_", " ")).first().begin_hour
                end = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schd_id,
                                                        worker=worker.replace("_", " ")).first().end_hour
                event = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schd_id,
                                                          worker=worker.replace("_", " ")).first().event
                h_sum = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schd_id,
                                                          worker=worker.replace("_", " ")).first().hours_sum
                billing_week = Personal_schedule.query.filter_by(date=datetime(year, month, day), includes_id=schd_id,
                                                                 worker=worker.replace("_", " ")).first().billing_week

                schd_dict["begin-%s-%d-%02d-%02d" % (worker, year, month, day)] = begin
                schd_dict["end-%s-%d-%02d-%02d" % (worker, year, month, day)] = end
                schd_dict["event-%s-%d-%02d-%02d" % (worker, year, month, day)] = event
                schd_dict["sum-%s-%d-%02d-%02d" % (worker, year, month, day)] = h_sum
                schd_dict["billing-week-%s-%d-%02d-%02d" % (worker, year, month, day)] = billing_week
    schd_dict["workers_hours"] = workers_hours
    return schd_dict
