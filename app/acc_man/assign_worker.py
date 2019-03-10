"""Functions for worker_to_workplace route"""

#-*- coding: utf-8 -*-

from app.models import Shop, User

def assign_worker(form):
    """Fills form's selectfield choices"""

    workplaces = Shop.query.order_by(Shop.shopname).all()
    workplaces_list = []
    for workplace in workplaces:
        workplaces_list.append((str(workplace), str(workplace)))
    form.workplace.choices = workplaces_list

    workers = User.query.order_by(User.username).all()
    workers_list = []
    for worker in workers:
        workers_list.append((str(worker), str(worker)))
    form.worker.choices = workers_list
