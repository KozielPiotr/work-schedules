from flask import Blueprint

bp = Blueprint("acc", __name__)

from app.acc_man import routes
