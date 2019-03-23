"""Finds the latest version of schedule"""

#-*- coding: utf-8 -*-

from app.models import Schedule


def find_latest_version_schd(schedules, workplace, year, month):
    """
    Only latest version can be modified.
    :param schedules: all schedules for chosen workplace
    :param workplace: chosen workplace
    :param year: schedule's year
    :param month: schedules month
    """
    versions = []
    for schedule in schedules:
        versions.append(schedule.version)

    highest_version = max(versions)
    filtered = Schedule.query.filter_by(year=int(year), month=int(month), workplace=workplace,
                                        version=highest_version, accepted=True).first()
    return filtered
