"""
Creates xlsx files based on accepted versions of schedule and loads xlsx files to create new schedules
- to_xlsx(): Creates xlsx file with schedule
"""

import os
import calendar
from openpyxl import Workbook
from openpyxl.utils import column_index_from_string as cifs
from flask import request, render_template
from app.xlsx import bp
from app import schedules


@bp.route("/xlsx", methods=["GET", "POST"])
def to_xlsx():
    """
    Creates xlsx file with schedule
    :return: redirects to template with generated link to created xlsx file with schedule
    """
    cal = calendar.Calendar()

    # getting dict with schedule data
    sched = request.args.get("schd")
    sched_v = request.args.get("v")
    sched_dict = schedules.routes.show_schedule_helper(sched, sched_v)

    # preparing data for xlsx file
    workplace = sched_dict["workplace"]
    year = sched_dict["year"]
    month = sched_dict["month"]
    version = sched_dict["version"]

    month_names = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień",
                   "Wrzesień", "Październik", "Listopad", "Grudzień"]
    weekday_names = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
    month_name = month_names[month-1]

    # starting work with file
    wb = Workbook()
    ws = wb.active
    ws.title = "grafik_na_%s" % (month_name)

    start_cell = ws.cell(row=1, column=1)

    # workplace, year and name of the month
    i = 1
    while i <= 3:
        for val in [workplace, year, month_name]:
            a = ws.cell(row=start_cell.row+i, column=2)
            a.value = val
            i += 1

    ws.merge_cells(start_row=2, start_column=3, end_row=4, end_column=3)
    cel = ws.cell(row=start_cell.row+1, column=cifs(start_cell.column)+2)
    cel.value = "D"
    print(cel.fill)

    # workers names and headers
    start = 0
    for worker in sched_dict["workers"]:
        ws.merge_cells(start_row=2, start_column=start+4, end_row=3, end_column=start+7)
        ws.cell(row=2, column=start+4).value = worker
        ws.cell(row=4, column=start+4).value = "Od"
        ws.cell(row=4, column=start+5).value = "Do"
        ws.cell(row=4, column=start+6).value = "H"
        ws.cell(row=4, column=start+7).value = "Podpis"
        start += 4

    # days and data for each worker
    start = ws.cell(row=5, column=2)
    c_r = 0
    for day in cal.itermonthdays2(sched_dict["year"], sched_dict["month"]):
        c_c = 0
        if day[0] > 0:
            day_name_cel = ws.cell(row=start.row+c_r, column=cifs(start.column)+c_c)
            day_name_cel.value = weekday_names[day[1]]

            day_number_cell = ws.cell(row=day_name_cel.row, column=cifs(day_name_cel.column)+1)
            day_number_cell.value = day[0]

            # hours and events
            for worker in sched_dict["workers"]:
                cel = ws.cell(row=start.row+c_r, column=c_c+4)
                cel.value = sched_dict["begin-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                                  day[0])]
                cel = ws.cell(row=start.row + c_r, column=c_c + 5)
                cel.value = sched_dict["end-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                                  day[0])]
                cel = ws.cell(row=start.row + c_r, column=c_c + 6)
                cel.value = sched_dict["sum-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                                  day[0])]
                cel = ws.cell(row=start.row + c_r, column=c_c + 6)
                event = sched_dict["event-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                                  day[0])]
                if event == "off":
                    cel.value = "X"
                elif event == "in_work":
                    cel.value = "........"
                else:
                    cel.value = event
                c_c += 4

            c_r += 1




    filename = "%s_grafik_na_%02d_%s_v_%s.xlsx" % (workplace.replace(" ", "_"), month, year, version)
    print(filename)
    path = "xlsx_schedules/%s/%s/%s" % (year, month, workplace.replace(" ", "_"))
    if not os.path.exists(path):
        os.makedirs(path)
    wb.save("%s/%s" % (path, filename))

    return render_template("xlsx/download_xlsx.html", path=path, filename=filename, weekday_names=weekday_names)
