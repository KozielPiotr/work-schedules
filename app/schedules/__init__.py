# pylint: disable=missing-docstring, wrong-import-position

from flask import Blueprint

bp = Blueprint("schedules", __name__)

from app.schedules import routes
