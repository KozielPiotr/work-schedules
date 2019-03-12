"""
Routes for whole schedules part of project.
- new_schedule_find_workers(): jsonifies data for dynamicly generated checkboxes in new_schedule()
- new_schedule_to_db(): adds schedule to database
- unaccepted_schedules(): makes list of unaccepted schedule for current user
- accept_modify_schedule(): creates modifiable template with schedule
- modifiable_schedules(): makes list of schedules modifiable by current user
- filter_schedules_to_modify(): jsonifies data for dynamically generated filtered list of schedules in
  modifiable_schedules()
- remove_schedule(): removes schedule from db
- add_user_to_schedule(): adds user to existing schedule
- choose_show_schedule(): generates form to choose schedule to show
- show_schedule_helper(): creates dictionary with all data from chosen schedule
- show_schedule() : generates uneditable template with chosen schedule
- select_guideline(): form to select for which year, month and workplace guideline would be created
- create_guideline(): creates guideline
- guidelines_to_db(): sends guidelines to db
"""

#-*- coding: utf-8 -*-

from calendar import Calendar
from flask import redirect, url_for, render_template, jsonify, request
from flask_login import login_required
from app import MONTH_NAMES, WEEKDAY_NAMES
from app.access_test import acc_test
from app.schedules import bp
from app.models import Shop, Billing_period, Schedule, Guidelines
from app.schedules.forms import NewScheduleForm, SelectGuideline
from app.schedules import list_of_schedules, new_schedule_funcs, find_workers, new_schd_to_db, filter_sched_to_modify,\
    accept_or_modify_schedule, remove_sched, add_user_to_sched, show_schedule_helper, select_guidelines_funcs,\
    guideline_to_database


@bp.route("/new-schedule", methods=["GET", "POST"])
@login_required
def new_schedule():
    """
    Creates template with empty, modifiable schedule for chosen year, month and workplace and with unmodifiable
    schedule for previous month.
    :return: template with all necessary data for new schedule
    """
    if acc_test.check_access(2) is False:
        return redirect(url_for("main.index"))

    form = NewScheduleForm()
    new_schedule_funcs.ns_choices(form)

    if form.validate_on_submit():
        return new_schedule_funcs.ns_form_validate(form)

    return render_template("schedules/new_schedule.html", title="Grafiki - nowy grafik", form=form)


@bp.route("/new-schedule/<workplace>")
@login_required
def new_schedule_find_workers(workplace):
    """
    Finds workers assigned to chosen workplace and sends back list with them to template that allow to choose workers
    that will be in schedule.
    :param workplace: chosen workplace
    :return: jsonified list of workers assigned to chosen workplace
    """
    if acc_test.check_access(2) is False:
        return redirect(url_for("main.index"))

    jsondict = find_workers.find_workers(workplace)
    return jsonify({"workers": jsondict})


@bp.route('/schedule-to-db/<action>', methods=['POST'])
@login_required
def new_schedule_to_db(action):
    """
    Adds new (unaccepted) schedule do database or replaces unaccepted version with accepted one.
    :param action: tells function if it has to add new version to db or replace existing one with it's accepted version.
    """
    if acc_test.check_access(2) is False:
        return redirect(url_for("main.index"))

    data = request.json

    new_schd_to_db.add_schedule_to_db(action, data)

    return url_for("main.index")
    # except AttributeError:
    # return "1"
    # except:
    # return "2"


@bp.route("/unaccepted_schedules", methods=["GET", "POST"])
@login_required
def unaccepted_schedules():
    """
    :return: shows list of every unaccepted schedules which current user can accept.
    """
    if acc_test.check_access(1) is False:
        return redirect(url_for("main.index"))

    los = list_of_schedules.list_of_schedules_acc_mod(mod_acc=False)

    return render_template("schedules/schedules-to-accept.html", title="Grafiki - niezaakceptowane grafiki",
                           ua=los["schedules"], sn=los["nos"], Schedule=Schedule)


@bp.route("/accept-schedule", methods=["GET", "POST"])
@login_required
def accept_modify_schedule():
    """
    :return: creates template with modifiable version of chosen unaccepted schedule and unmodifiable view.
    at previous month schedule
    """
    if acc_test.check_access(1) is False:
        return redirect(url_for("main.index"))

    action = request.args.get("action")
    schedule = None
    cal = Calendar()
    to_render = accept_or_modify_schedule.acc_mod_schd(action)
    prev = to_render["prev"]

    return render_template("schedules/accept-schedule.html", action=action, title=to_render["title"], schedule=schedule,
                           workplace=to_render["workplace"], year=to_render["year"], month=to_render["month"],
                           workers=to_render["workers"], month_name=to_render["month_name"], wdn=WEEKDAY_NAMES,
                           Billing_period=Billing_period, version=to_render["version"], shdict=to_render["shdict"],
                           hours=to_render["hours"], prev_shdict=prev["prev_shdict"], prev_month=prev["month"],
                           prev_hours=prev["hours"], prev_month_name=prev["month_name"], prev_year=prev["year"],
                           prev_workers=prev["workers"], workers_hours=prev["workers_hours"], cal=cal,
                           id=to_render["schedule_id"], Guidelines=Guidelines, Shop=Shop)


@bp.route("/modifiable-schedules", methods=["GET", "POST"])
@login_required
def modifiable_schedules():
    """
    Makes list of schedules modifiable by current user.
    :return: renders template with form that allows to filter all accepted schedules and chose one to modify
    """
    if acc_test.check_access(2) is False:
        return redirect(url_for("main.index"))

    return render_template("schedules/schedules-to-modify.html", title="Grafiki - modyfikowalne grafiki",
                           mn=MONTH_NAMES, Schedule=Schedule)


@bp.route("/filter-schedules/<year>/<month>/<workplace>/<action>")
@login_required
def filter_schedules_to_modify(year, month, workplace, action):
    """
    Finds schedule that matches filter criteria.
    :param year: year of schedule
    :param month: month of schedule
    :param workplace: workplace of schedule
    :param action: action to take
    :return: matching schedule
    """
    if acc_test.check_access(2) is False:
        return redirect(url_for("main.index"))

    return jsonify(filter_sched_to_modify.find_schedule(year, month, workplace, action))


@bp.route('/remove-schedule/<schedule>', methods=["GET", "POST"])
@login_required
def remove_schedule(schedule):
    """
    Removes schedule with passed id from db.
    :param schedule: schedule's id
    """
    if acc_test.check_access(2) is False:
        return redirect(url_for("main.index"))

    return remove_sched.remove_sched(schedule)


@bp.route('/add-user-to-schedule/<schedule_id>/<worker>/<action>', methods=["GET", "POST"])
@login_required
def add_user_to_schedule(schedule_id, worker, action):
    """
    Adds user to schedule.
    :param schedule_id: schedule, to which worker should be appended
    :param worker: worker that will be added to schedule
    :param action: determines if modifying or accepting schedule
    :return: redirects to template with new worker added
    """

    schedule = Schedule.query.filter_by(id=schedule_id).first()
    add_user_to_sched.add_user_to_sched(schedule, worker)

    return redirect(url_for("schedules.accept_modify_schedule", action=action, schd=schedule.name,
                            v=schedule.version))


@bp.route('/choose_show_schedule', methods=["GET", "POST"])
@login_required
def choose_show_schedule():
    """
    :return: generates form to choose schedule to show.
    """
    action = request.args.get("action")
    title = "Grafiki - podgląd grafiku"

    return render_template("schedules/choose_show_schedule.html", title=title, mn=MONTH_NAMES, action=action)


@bp.route('/show_schedule/<schd>/<version>', methods=["GET", "POST"])
@login_required
def show_schedule(schd, version):
    """
    Generates uneditable template with chosen schedule.
    :return: template with view of chosen schedule
    """
    schd_dict = show_schedule_helper.show_schedule_helper(schd, version)

    return render_template("schedules/show_schedule.html", schd_dict=schd_dict, mn=MONTH_NAMES, cal=Calendar(),
                           wdn=WEEKDAY_NAMES)


@bp.route('/select-guideline', methods=["GET", "POST"])
@login_required
def select_guideline():
    """
    Allows to select for which schedule guidelines will be created.
    :return: template for choose year, month and workplace
    """
    if acc_test.check_access(1) is False:
        return redirect(url_for("main.index"))

    title = "Grafiki - wytyczne"
    form = SelectGuideline()

    form.workplace.choices = select_guidelines_funcs.select_guidelines_choices()
    if form.validate_on_submit():
        return select_guidelines_funcs.select_guideline_validate(form)

    return render_template("schedules/select-guideline.html", title=title, mn=MONTH_NAMES, form=form)


@bp.route('/create-guideline', methods=["GET", "POST"])
@login_required
def create_guideline():
    """
    Template with calendar where user can input guidelines.
    :return: template for guidelines
    """
    if acc_test.check_access(1) is False:
        return redirect(url_for("main.index"))

    year = int(request.args.get("y"))
    month = int(request.args.get("m"))
    workplace = Shop.query.filter_by(shopname=request.args.get("w")).first()

    return render_template("schedules/create-guideline.html", year=year, month=month, workplace=workplace,
                           mn=MONTH_NAMES, wdn=WEEKDAY_NAMES, cal=Calendar(), Guidelines=Guidelines)


@bp.route('/guidelines-to-db', methods=["GET", "POST"])
@login_required
def guidelines_to_db():
    """
    Adds records with guidelines to db.
    """
    if acc_test.check_access(1) is False:
        return redirect(url_for("main.index"))

    guideline_to_database.add_guideline()

    return url_for("main.index")
