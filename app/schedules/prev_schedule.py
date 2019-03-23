"""Makes dictionary with all data needed to create template that shows existing schedule"""

#-*- coding: utf-8 -*-
# pylint: disable=no-member

from datetime import datetime
from calendar import Calendar

from app.models import Schedule, Personal_schedule
from app import MONTH_NAMES


def prev_schedule(month, year, workplace):
    """
    :param month: month of schedule
    :param year: year of schedule
    :param workplace: workplace for which schedule has to be create
    :return: dictionary with all needed data
    """
    cal = Calendar()
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    prev_month_name = MONTH_NAMES[prev_month - 1]

    try:
        prev_month_last_version = Schedule.query.filter_by(year=prev_year, month=prev_month, workplace=workplace,
                                                           accepted=True).order_by(Schedule.version.desc()).first().\
                                                                                   version
        prev_month_shd = Schedule.query.filter_by(year=prev_year, month=prev_month, workplace=workplace,
                                                  version=prev_month_last_version).first()
    except AttributeError:
        prev_month_shd = None

    if prev_month_shd is not None:
        prev_schd_id = prev_month_shd.id
        prev_workers = []
        for pers_schedule in prev_month_shd.ind:
            if str(pers_schedule.worker).replace(" ", "_") not in prev_workers:
                prev_workers.append(str(pers_schedule.worker).replace(" ", "_"))

        prev_hours = prev_month_shd.hrs_to_work
        prev_shdict = {}
        workers_hours = {}
        for worker in prev_workers:
            worker_hours = 0
            for p_schedule in prev_month_shd.ind:
                if p_schedule.worker == str(worker).replace("_", " "):
                    worker_hours += p_schedule.hours_sum
                workers_hours[worker] = worker_hours

        for worker in prev_workers:
            for day in cal.itermonthdays(prev_year, prev_month):
                if day > 0:
                    begin = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                              includes_id=prev_schd_id,
                                                              worker=worker.replace("_", " ")).first().begin_hour
                    end = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                            includes_id=prev_schd_id,
                                                            worker=worker.replace("_", " ")).first().end_hour
                    event = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                              includes_id=prev_schd_id,
                                                              worker=worker.replace("_", " ")).first().event
                    h_sum = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                              includes_id=prev_schd_id,
                                                              worker=worker.replace("_", " ")).first().hours_sum
                    billing_week = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                                     includes_id=prev_schd_id,
                                                                     worker=worker.replace("_",
                                                                                           " ")).first().billing_week

                    prev_shdict["begin-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = begin
                    prev_shdict["end-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = end
                    prev_shdict["event-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = event
                    prev_shdict["sum-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = h_sum
                    prev_shdict["billing-week-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = billing_week
    else:
        prev_shdict = None
        prev_hours = None
        prev_workers = None
        workers_hours = None
    prev = {"prev_shdict": prev_shdict, "hours": prev_hours, "workers": prev_workers, "workers_hours": workers_hours,
            "year": prev_year, "month": prev_month, "month_name": prev_month_name}
    return prev
