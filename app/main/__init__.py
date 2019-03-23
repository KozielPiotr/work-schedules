# pylint: disable=missing-docstring, wrong-import-position

from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main import routes
