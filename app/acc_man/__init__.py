from flask import Blueprint

bp = Blueprint("acc", __name__)

from app.acc_man import acc_man