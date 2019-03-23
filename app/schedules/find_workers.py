"""Makes dictionary with data for dynamically generated checkboxes in new_schedule route"""

#-*- coding: utf-8 -*-

from flask import flash, redirect, url_for
from flask_login import current_user

from app.models import Shop


def find_workers(workplace):
    """
    :param workplace: chosen workplace
    :return: dictionary with workers
    """
    if current_user.access_level != "0" and current_user.access_level != "1" and current_user.access_level != "2":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("main.index"))

    shop = Shop.query.filter_by(shopname=workplace).first()
    workers = shop.works.all()
    jsondict = []
    for worker in shop.works.all():
        workers_list = {}
        if worker.access_level == "0" or worker.access_level == "1":
            workers.remove(worker)
        else:
            workers_list["name"] = worker.username
            jsondict.append(workers_list)
    return jsondict
