"""When user is going to accept schedule, he or she should see all changes between old and new version of the schedule."""

#-*- coding: utf-8 -*-

from calendar import Calendar
from datetime import datetime

from app.models import Schedule, Personal_schedule


def create_change_messages(unaccepted_ind, last_accepted_ind, basic):
    """
    Creates string with changes in personal schedule
    :param unaccepted_ind: unaccepted personal schedule
    :param last_accepted_ind: last accepted personal schedule
    :param basic: dict with day, month, year and hours for schedules
    :return: string with changes in personal schedule
    """
    l_a_event = last_accepted_ind.event

    if last_accepted_ind.event == "off":
        l_a_event = "wolne"
    elif last_accepted_ind.event == "in_work":
        l_a_event = "praca"
    un_event = unaccepted_ind.event
    if unaccepted_ind.event == "off":
        un_event = "wolne"
    elif unaccepted_ind.event == "in_work":
        un_event = "praca"
    un_begin = basic["un_begin"]
    if un_begin == 0:
        un_begin = "--"
    un_end = basic["un_end"]
    if un_end == 0:
        un_end = "--"
    l_a_begin = basic["l_a_begin"]
    if l_a_begin == 0:
        l_a_begin = "--"
    l_a_end = basic["l_a_end"]
    if l_a_end == 0:
        l_a_end = "--"

    change = "W dniu %s.%s.%s:\n\tbyło: " % (basic["day"], basic["month"], basic["year"])
    if l_a_event == "wolne\n\tjest: ":
        change += l_a_event
    else:
        change += "%s od %s do %s\n\tjest: " % (l_a_event, l_a_begin, l_a_end)

    if un_event == "wolne":
        change += un_event
    else:
        change += "%s od %s do %s" % (un_event, un_begin, un_end)

    return change


def find_workers(ind):
    """
    Finds workers in individual schedules
    :param ind:
    :return: list of unique workers in given schedules
    """
    workers = []
    for ind_sched in ind:
        if ind_sched.worker not in workers:
            workers.append(ind_sched.worker)
    return workers


def compare_inds(schedule_id, last_accepted_id, unaccepted_ind, year, month):
    """
    Compares individual schedules from unaccepted schedule with those from last accepted version of the schedule.
    :param schedule_id: id of unaccepted schedule
    :param last_accepted_id: id of he last accepted schedule
    :param unaccepted_ind: list of unaccepted schedule's individual schedules
    :param year: year of schedule
    :param month: month of schedule
    :return: list of differences
    """
    changes = {}
    workers = find_workers(unaccepted_ind)
    cal = Calendar()
    for worker in workers:
        msg = []
        for day in cal.itermonthdays(year, month):
            if day > 0:
                unaccepted_ind = Personal_schedule.query.filter_by(date=datetime(year, month, day),
                                                                   worker=worker,
                                                                   includes_id=schedule_id).first()
                last_accepted_ind = Personal_schedule.query.filter_by(date=datetime(year, month, day),
                                                                      worker=worker,
                                                                      includes_id=last_accepted_id).first()
                if unaccepted_ind and last_accepted_ind:
                    if unaccepted_ind.begin_hour != last_accepted_ind.begin_hour or \
                       unaccepted_ind.end_hour != last_accepted_ind.end_hour or \
                       unaccepted_ind.event != last_accepted_ind.event:
                        basic = {
                            "year": year, "month": month, "day": day,
                            "l_a_begin": last_accepted_ind.begin_hour, "l_a_end": last_accepted_ind.end_hour,
                            "un_begin": unaccepted_ind.begin_hour, "un_end": unaccepted_ind.end_hour
                        }
                        msg.append(create_change_messages(unaccepted_ind, last_accepted_ind, basic))
        changes[worker] = msg

    return changes


def get_diff(schedule_id):
    """
    Gets differences between unaccepted schedule and it's last accepted version.
    :param schedule_id: id of unaccepted schedule
    :return:
    """
    unaccepted = Schedule.query.filter_by(id=schedule_id).first()
    unaccepted_ind = unaccepted.ind
    year = unaccepted.year
    month = unaccepted.month
    last_accepted = Schedule.query.filter_by(name=unaccepted.name, version=unaccepted.version,
                                             accepted=True).first()
    last_accepted_id = last_accepted.id

    found_diffs = compare_inds(schedule_id, last_accepted_id, unaccepted_ind, year, month)

    return found_diffs
