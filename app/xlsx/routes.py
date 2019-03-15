"""
Creates xlsx files based on accepted versions of schedule and loads xlsx files to create new schedules
- to_xlsx(): Creates xlsx file with schedule
- download_schedule(): Allows to download file with schedule
- upload_file(): Uploads chosen .xlsx file with schedule
"""

#-*- coding: utf-8 -*-

from flask import request, current_app, send_from_directory, render_template
from flask_login import login_required
from app.xlsx import bp
from app.xlsx.forms import UploadFile
from app.xlsx import create_xlsx, upload_from_file, create_from_file


@bp.route("/xlsx", methods=["GET", "POST"])
@login_required
def to_xlsx():
    """
    Creates xlsx file with schedule
    :return: redirects to template with generated link to created xlsx file with schedule
    """
    return create_xlsx.create_file()


@bp.route("/xlsx_download/<year>/<month>/<workplace>/<path:filename>", methods=["GET", "POST"])
@login_required
def download_schedule(year, month, workplace, filename):
    """
    Allows to download file with schedule. Params creates path to file.
    :param year: schedule's year
    :param month: schedule's month
    :param workplace: schedule's workplace
    :param filename: name of file with schedule
    :return: downloading file
    """
    path = "/xlsx_files/download/%s/%s/%s/" % (year, month, workplace.replace(" ", "_"))
    to_file = current_app.root_path+path

    return send_from_directory(directory=to_file, filename=filename)


@bp.route("/upload-file", methods=["GET", "POST"])
@login_required
def upload_file():
    """
    Uploads chosen .xlsx file with schedule
    :return: template with form to choose schedule file
    :form validate return: redirection to function that creates dictionary based on uploaded file with schedule
    """
    year = request.args.get("year")
    month = request.args.get("month")
    workplace = request.args.get("workplace")
    hours = request.args.get("hours")
    title = "Grafiki - wybór pliku z grafikiem"
    form = UploadFile()
    if form.validate_on_submit():
        return upload_from_file.upload_xlsx(year, month, workplace, hours)

    return render_template("xlsx/upload_from_file.html", title=title, form=form)


@bp.route("/create_from_file", methods=["GET", "POST"])
@login_required
def create_dict_from_file():
    """
    Loads file with schedule and makes dictionary with data required to fulfill template
    """
    return create_from_file.create_sched()
