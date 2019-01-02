"""
Main functions of project
"""

#-*- coding: utf-8 -*-
# pylint: disable=no-member

from flask import render_template
from flask_login import login_required
from app import app
from app.models import Schedule
from app.main import bp


# main page
@bp.route("/")
@bp.route("/index")
@login_required
def index():
    """
    Main page.
    """
    return render_template("main/index.html", title="Grafiki")


@bp.route("/test", methods=["GET", "POST"])
def test():
    """
    Test route. Needs to be removed in final version.
    """
    queries = []
    months = Schedule.query.filter_by(month=11)
    places = Schedule.query.filter_by(workplace="Sklep 1")
    for month in months:
        if month in places:
            queries.append(month.name)
    print(queries)
    return "%s"


@bp.route("/<path:path>")
def static_proxy(path):
    """
    Allows to send files between functions.
    """
    return app.send_static_file(path)