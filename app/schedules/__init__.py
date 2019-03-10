from flask import Blueprint

bp = Blueprint("schedules", __name__)

from app.schedules import routes
