"""Creates schedule based on uploaded file"""

#-*- coding: utf-8 -*-

import os
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename


def upload_xlsx(year, month, workplace, hours):
    """
    Uploads file
    """
    if "file" not in request.files:
        flash("Nie wybrano pliku")
        return redirect(request.url)

    file = request.files["file"]

    if file.filename == "":
        flash("Nie wybrano pliku")
        return redirect(request.url)

    if file and file.filename.rsplit('.', 1)[1].lower() == "xlsx":
        filename = secure_filename(file.filename)
        path = "app/xlsx_files/upload/"
        if not os.path.exists(path):
            os.makedirs(path)
        file.save("%s%s" % (path, filename))
        return redirect(url_for("xlsx.create_dict_from_file", path=path, filename=filename, year=year, month=month,
                                workplace=workplace, hours=hours))
    flash("Nieprawidłowy rodzaj pliku. Plik musi być w formacie xlsx.")
    return redirect(request.url)
