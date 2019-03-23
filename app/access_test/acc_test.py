"""Checks user's access level"""

#-*- coding: utf-8 -*-

from flask import flash
from flask_login import current_user


def check_access(level):

    if int(current_user.access_level) > level:
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
    return False
