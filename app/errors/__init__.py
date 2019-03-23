# pylint: disable=missing-docstring, wrong-import-position

from flask import Blueprint

bp = Blueprint("errors", __name__)

from app.errors import handlers
