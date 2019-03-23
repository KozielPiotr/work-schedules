"""sends guidelines to db"""

#-*- coding: utf-8 -*-

from calendar import Calendar
from flask import request

from app import db
from app.models import Shop, Guidelines


def add_guideline():
    """
    Adds records with guidelines to db
    """
    cal = Calendar()
    data = request.json
    year = int(data["year"])
    month = int(data["month"])
    workplace = Shop.query.filter_by(shopname=data["workplace"]).first()
    for day in cal.itermonthdays(year, month):
        if day > 0:
            guideline = Guidelines.query.filter_by(guide=workplace, year=year, month=month, day=day).first()
            if guideline:
                guideline.no_of_workers = data[str(day)]
                db.session.add(guideline)
            else:
                guideline = Guidelines(guide=workplace, year=year, month=month, day=day,
                                       no_of_workers=data[str(day)])
                db.session.add(guideline)
    db.session.commit()
