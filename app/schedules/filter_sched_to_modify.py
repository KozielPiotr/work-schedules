"""Finds schedule that matches filter criteria and gets data from it"""

#-*- coding: utf-8 -*-

from flask import url_for
from flask_login import current_user

from app.models import Schedule
from app.schedules import latest_version


def one_workplace(action, year, month, workplace, schedules):
    """
    When one workplace is selected
    :param action: action to take
    :param year: year of schedule
    :param month: month of schedule
    :param workplace: workplace of schedule
    :param schedules: chosen schedule
    :return: dictionary with data to create json
    """
    if not schedules:
        to_front = {"option": 0}
        return to_front
    filtered = latest_version.find_latest_version_schd(schedules, workplace, year, month)
    uri = "#"
    if action == "modify":
        uri = url_for("schedules.accept_modify_schedule", schd=filtered.name, v=filtered.version,
                      action="to_modify")
    elif action == "show":
        uri = url_for("schedules.show_schedule", schd=filtered.name, version=filtered.version, action=action)
    elif action == "xlsx":
        uri = url_for("xlsx.to_xlsx", schd=filtered.name, v=filtered.version, action=action)
    to_front = {"option": 1, "schedules": [{"url": uri, "name": filtered.name, "year": filtered.year,
                                            "month": filtered.month, "workplace": filtered.workplace,
                                            "version": filtered.version}]}
    return to_front


def all_workplaces(action, year, month):
    """
    When all aviable schedules are selected
    :param action: action to take
    :param year: year of schedule
    :param month: month of schedule
    :return: dictionary with data to create json
    """
    workplaces = current_user.workers_shop
    json_schedules = []
    for users_workplace in workplaces:
        schedules = Schedule.query.filter_by(year=int(year), month=int(month), workplace=users_workplace.shopname,
                                             accepted=True).all()
        if schedules:
            filtered = latest_version.find_latest_version_schd(schedules, users_workplace.shopname, year, month)
            if filtered is not None:
                uri = "#"
                if action == "modify":
                    uri = url_for("schedules.accept_modify_schedule", schd=filtered.name, v=filtered.version,
                                  action="to_modify")
                elif action == "show":
                    uri = url_for("schedules.show_schedule", schd=filtered.name, version=filtered.version,
                                  action=action)
                elif action == "xlsx":
                    uri = url_for("xlsx.to_xlsx", schd=filtered.name, v=filtered.version, action=action)
                json_schedules.append({"url": uri, "name": filtered.name, "year": filtered.year,
                                       "month": filtered.month, "workplace": filtered.workplace,
                                       "version": filtered.version})
    if not json_schedules:
        to_front = {"option": 0}
        return to_front

    to_front = {"option": 1, "schedules":json_schedules}
    return to_front


def find_schedule(year, month, workplace, action):
    """

    :param year: year of schedule
    :param month: month of schedule
    :param workplace: workplace of schedule
    :param action: action to take
    :return:
    """
    schedules = Schedule.query.filter_by(year=int(year), month=int(month), workplace=workplace, accepted=True).all()
    if workplace != "0":
        return one_workplace(action, year, month, workplace, schedules)
    return all_workplaces(action, year, month)
