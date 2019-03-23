from flask import Blueprint

bp = Blueprint("xlsx", __name__)

from app.xlsx import routes
