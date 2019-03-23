# pylint: disable=missing-docstring, wrong-import-position

from flask import Blueprint

bp = Blueprint("acc", __name__)

from app.acc_man import routes
