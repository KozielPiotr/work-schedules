"""
Creates xlsx files based on accepted versions of schedule and loads xlsx files to create new schedules
- to_xlsx(): Creates xlsx file with schedule
"""

import os
import calendar
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment
from openpyxl.styles.borders import Border, Side
from openpyxl.utils import column_index_from_string as cifs
from flask import request, redirect, url_for, current_app, send_from_directory
from flask_login import login_required
from app.xlsx import bp
from app import schedules


@bp.route("/xlsx", methods=["GET", "POST"])
@login_required
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
    ws.title = "grafik_na_%s" % month_name

    # style patterns for file
    header_style = PatternFill(fgColor="b4bbc1", fill_type="solid")
    names_style = PatternFill(fgColor="c9ccce", fill_type="solid")
    footer_style = PatternFill(fgColor="55bbff", fill_type="solid")
    l4_style = PatternFill(fgColor="80D332", fill_type="solid")
    u_style = PatternFill(fgColor="FC33FF", fill_type="solid")
    thin_border_style = Border(left=Side(style="thin"),
                               right=Side(style="thin"),
                               top=Side(style="thin"),
                               bottom=Side(style="thin"))
    right_med_border_style = Border(left=Side(style="thin"),
                                    right=Side(style="medium"),
                                    top=Side(style="thin"),
                                    bottom=Side(style="thin"))
    right_bot_med_border_style = Border(left=Side(style="thin"),
                                        right=Side(style="medium"),
                                        top=Side(style="thin"),
                                        bottom=Side(style="medium"))
    bottom_med_border_style = Border(left=Side(style="thin"),
                                     right=Side(style="thin"),
                                     top=Side(style="thin"),
                                     bottom=Side(style="medium"))

    alignment_style = Alignment(horizontal="center",
                                vertical="center",
                                wrapText=True)

    start_cell = ws.cell(row=1, column=1)

    # workplace, year and name of the month
    i = 1
    while i <= 3:
        for val in [workplace, year, month_name]:
            cel = ws.cell(row=start_cell.row+i, column=2)
            cel.value = val
            cel.fill = header_style
            if i == 3:
                cel.border = bottom_med_border_style
            else:
                cel.border = thin_border_style
            i += 1

    ws.merge_cells(start_row=2, start_column=3, end_row=4, end_column=3)
    cel = ws.cell(row=start_cell.row+1, column=cifs(start_cell.column)+2)
    cel.value = "D"
    cel.fill = header_style
    cel.border = right_bot_med_border_style
    ws.cell(row=4, column=3).border = right_bot_med_border_style

    # workers names and headers
    start = 0
    for worker in sched_dict["workers"]:
        ws.merge_cells(start_row=2, start_column=start+4, end_row=3, end_column=start+7)
        ws.cell(row=2, column=start+4).value = worker
        ws.cell(row=2, column=start+4).fill = names_style
        ws.cell(row=2, column=start+4).border = right_med_border_style
        ws.cell(row=2, column=start+7).border = right_med_border_style
        ws.cell(row=4, column=start+4).value = "Od"
        ws.cell(row=4, column=start+4).fill = header_style
        ws.cell(row=4, column=start+4).border = bottom_med_border_style
        ws.cell(row=4, column=start+5).value = "Do"
        ws.cell(row=4, column=start+5).fill = header_style
        ws.cell(row=4, column=start+5).border = bottom_med_border_style
        ws.cell(row=4, column=start+6).value = "H"
        ws.cell(row=4, column=start+6).fill = header_style
        ws.cell(row=4, column=start+6).border = bottom_med_border_style
        ws.cell(row=4, column=start+7).value = "Podpis"
        ws.cell(row=4, column=start+7).fill = header_style
        ws.cell(row=4, column=start+7).border = right_bot_med_border_style
        start += 4

    # days and data for each worker
    start = ws.cell(row=5, column=2)
    c_r = 0
    for day in cal.itermonthdays2(sched_dict["year"], sched_dict["month"]):
        c_c = 0
        if day[0] > 0:
            day_name_cel = ws.cell(row=start.row+c_r, column=cifs(start.column)+c_c)
            day_name_cel.value = weekday_names[day[1]]
            day_name_cel.fill = header_style
            day_name_cel.border = thin_border_style

            day_number_cell = ws.cell(row=day_name_cel.row, column=cifs(day_name_cel.column)+1)
            day_number_cell.value = day[0]
            day_number_cell.fill = header_style
            day_number_cell.border = right_med_border_style

            # hours and events
            for worker in sched_dict["workers"]:
                if weekday_names[day[1]] not in ["Sobota", "Niedziela"]:
                    color = PatternFill(fgColor="ffffff", fill_type="solid")
                else:
                    color = PatternFill(fgColor="b4bbc1", fill_type="solid")
                event = sched_dict["event-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                              day[0])]
                sum_val = sched_dict["sum-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                              day[0])]
                if event in ["UW", "UNŻ", "UO", "UOJ", "UR"]:
                    color = u_style
                elif event == "L4":
                    color = l4_style

                cel = ws.cell(row=start.row+c_r, column=c_c+4)
                if sum_val == 0:
                    cel.value = "--"
                else:
                    cel.value = sched_dict["begin-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                                      day[0])]
                cel.fill = color
                cel.border = thin_border_style
                cel = ws.cell(row=start.row + c_r, column=c_c + 5)
                if sum_val == 0:
                    cel.value = "--"
                else:
                    cel.value = sched_dict["end-%s-%d-%02d-%02d" % (worker, sched_dict["year"], sched_dict["month"],
                                                                    day[0])]
                cel.border = thin_border_style
                cel.fill = color
                cel = ws.cell(row=start.row + c_r, column=c_c + 6)
                cel.value = sum_val
                cel.border = thin_border_style
                cel.fill = color
                cel = ws.cell(row=start.row + c_r, column=c_c + 7)

                if event == "off":
                    cel.value = "X"
                elif event == "in_work":
                    cel.value = "........"
                else:
                    cel.value = event

                cel.border = right_med_border_style
                cel.fill = color
                c_c += 4
            c_r += 1

    # footer with hours
    start = ws.cell(row=ws.max_row+1, column=2)
    ws.merge_cells(start_row=start.row, start_column=2, end_row=start.row, end_column=cifs(start.column)+1)
    start.value = "H/mc:"
    start.fill = footer_style
    start.border = right_med_border_style
    ws.cell(row=start.row, column=cifs(start.column)+1).border = right_med_border_style
    start_col = 0
    for worker in sched_dict["workers"]:
        ws.merge_cells(start_row=start.row, start_column=start_col+4, end_row=start.row,
                       end_column=start_col+7)
        cel = ws.cell(row=start.row, column=start_col+4)
        cel.value = "Suma H:"
        cel.fill = footer_style
        cel.border = right_med_border_style
        ws.cell(row=start.row, column=start_col+7).border = right_med_border_style
        start_col += 4

    start = ws.cell(row=ws.max_row + 1, column=2)
    ws.merge_cells(start_row=start.row, start_column=2, end_row=start.row, end_column=cifs(start.column)+1)
    start.value = sched_dict["hours"]
    start.fill = footer_style
    start.border = right_med_border_style
    ws.cell(row=start.row, column=cifs(start.column)+1).border = right_med_border_style
    start_col = 0
    for worker in sched_dict["workers"]:
        ws.merge_cells(start_row=start.row, start_column=start_col+4, end_row=start.row,
                       end_column=start_col+7)
        cel = ws.cell(row=start.row, column=start_col+4)
        cel.value = sched_dict["workers_hours"][worker]
        cel.border = right_med_border_style
        ws.cell(row=start.row, column=start_col+7).border = right_med_border_style
        if cel.value > sched_dict["hours"]:
            cel.fill = PatternFill(fgColor="ff7878", fill_type="solid")
        elif cel.value < sched_dict["hours"]:
            cel.fill = PatternFill(fgColor="faaa01", fill_type="solid")
        start_col += 4

    start = ws.cell(row=ws.max_row+1, column=2)
    ws.merge_cells(start_row=start.row, start_column=2, end_row=start.row, end_column=cifs(start.column)+1)
    start.value = "Pozostało:"
    start.fill = footer_style
    start.border = right_med_border_style
    ws.cell(row=start.row, column=cifs(start.column)+1).border = right_med_border_style
    start_col = 0
    for worker in sched_dict["workers"]:
        ws.merge_cells(start_row=start.row, start_column=start_col+4, end_row=start.row,
                       end_column=start_col+7)
        cel = ws.cell(row=start.row, column=start_col+4)
        cel.value = sched_dict["hours"] - sched_dict["workers_hours"][worker]
        cel.border = right_med_border_style
        ws.cell(row=start.row, column=start_col+7).border = right_med_border_style
        if cel.value < 0:
            cel.fill = PatternFill(fgColor="ff7878", fill_type="solid")
        elif cel.value > 1:
            cel.fill = PatternFill(fgColor="faaa01", fill_type="solid")
        start_col += 4

    for row in range(1, ws.max_row+1):
        for col in range(1, ws.max_column+1):
            ws.cell(row=row, column=col).alignment = alignment_style

    # saving file
    filename = "%s_grafik_na_%02d_%s_v_%s.xlsx" % (workplace.replace(" ", "_"), month, year, version)
    path = "app/xlsx_schedules/%s/%s/%s" % (year, month, workplace.replace(" ", "_"))
    if not os.path.exists(path):
        os.makedirs(path)
    wb.save("%s/%s" % (path, filename))
    return redirect(url_for("xlsx.download_schedule", year=year, month=month, workplace=workplace, filename=filename))


@bp.route("/xlsx_download/<year>/<month>/<workplace>/<path:filename>", methods=["GET", "POST"])
@login_required
def download_schedule(year, month, workplace, filename):
    path = "/xlsx_schedules/%s/%s/%s/" % (year, month, workplace.replace(" ", "_"))
    to_file = current_app.root_path+path

    return send_from_directory(directory=to_file, filename=filename)
