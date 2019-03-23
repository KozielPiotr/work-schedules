from flask import Blueprint

bp = Blueprint("b_per", __name__)

from app.billing_period import routes
