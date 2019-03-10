"""Removes schedule from db"""

#-*- coding: utf-8 -*-

from flask import redirect, url_for, flash
from app import db
from app.models import Schedule


def remove_sched(schedule):
    """
    Removes schedule with passed id from db
    :param schedule: schedule's id
    :return: redirects to main page
    """
    schedule_to_remove = Schedule.query.filter_by(id=schedule).first()

    if schedule_to_remove is not None:
        for pers_schedule in schedule_to_remove.ind:
            db.session.delete(pers_schedule)
        db.session.delete(schedule_to_remove)
        db.session.commit()
        flash("Usunięto niezaakceptowaną propozycję grafiku %s na %s.%s v_%s" % (schedule_to_remove.workplace,
                                                                                 schedule_to_remove.month,
                                                                                 schedule_to_remove.year,
                                                                                 schedule_to_remove.version))
        return redirect(url_for("main.index"))

    flash("Nie ma takiego grafiku")
    return redirect(url_for("main.index"))
