"""Prepares list of schedules aviable for current user to accept or modify."""

#-*- coding: utf-8 -*-
# pylint: disable=no-member

from flask_login import current_user
from app.models import Schedule

def list_of_schedules_acc_mod(mod_acc):
    """
    :param mod_acc: Defines if function looks for accepted or unaccepted schedules
    :return: list of schedules that match to 'mod_acc' criteria
    """
    schedules = []
    for schedule in Schedule.query.filter_by(accepted=mod_acc).order_by(Schedule.workplace, Schedule.year,
                                                                        Schedule.month, Schedule.version).all():
        for assigned_workplaces in current_user.workers_shop:
            if str(schedule.workplace) == str(assigned_workplaces):
                schedules.append(schedule)

    number_of_schedules = len(schedules)
    schedules_list = {"schedules": schedules, "nos": number_of_schedules}

    return schedules_list
