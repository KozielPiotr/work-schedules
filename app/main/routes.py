"""
Main functions of project
"""

#-*- coding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from app import app
from app.main import bp


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    """
    Main page.
    """
    return render_template("main/index.html", title="Grafiki")


@bp.route("/<path:path>")
def static_proxy(path):
    """
    Allows to send files between functions.
    """
    return app.send_static_file(path)
