from flask import Blueprint

bp = Blueprint("access_test", __name__)

from app.auth import routes
