"""Functions for admin_password_change route"""

#-*- coding: utf-8 -*-

from app.models import User

def users_for_admin():
    """changes chosen user's password. Admin only"""
    workers = []
    for user in User.query.all():
        workers.append((str(user), str(user)))
    return workers
