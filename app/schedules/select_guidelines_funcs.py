"""Functions for select_guideline route"""

#-*- coding: utf-8 -*-

from flask import redirect, url_for
from flask_login import current_user


def select_guidelines_choices():
    """
    creates choices for workplace field in form
    :param form:
    :return: choices for workplace field in form
    """
    workplaces = []
    for workplace in current_user.workers_shop:
        workplaces.append((str(workplace), str(workplace)))

    return workplaces


def select_guideline_validate(form):
    """
    Allows to select for which schedule guidelines will be created
    :return: redirects to guideline creation page
    """
    year = form.year.data
    month = form.month.data
    workplace = form.workplace.data
    return redirect(url_for("schedules.create_guideline", y=year, m=month, w=workplace))
