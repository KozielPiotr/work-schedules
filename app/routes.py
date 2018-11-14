from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, NewUserForm, NewShopForm, UserToShopForm, NewScheduleForm, BillingPeriod
from app.models import User, Shop, Billing_period, Personal_schedule, Schedule
import calendar
from sqlalchemy import update
import datetime
from datetime import datetime, date


# welcome page
@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Grafiki")


# Login page. Checks if user is logged in and if not redirects to log in  page
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Nieprawidłowa nazwa użytkownika lub hasło")
            return redirect(url_for("index"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc !="":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Grafiki - logowanie", form=form)


#  Logging out user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


#  New user
@app.route("/new-user", methods=["GET", "POST"])
@login_required
def new_user():
    if current_user.access_level != "0" and current_user.access_level != "1":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    form = NewUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, access_level=form.access_level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Nowy użytkownik zarejestrowany")
        return redirect(url_for("index"))
    return render_template("new_user.html", title="Grafiki - nowy użytkownik", form=form)


# New shop
@app.route("/new-shop", methods=["GET", "POST"])
@login_required
def new_shop():
    if current_user.access_level != "0" and current_user.access_level != "1":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    form = NewShopForm()
    if form.validate_on_submit():
        shop = Shop(shopname=form.shopname.data)
        db.session.add(shop)
        db.session.commit()
        flash("Stworzono nowy sklep")
        return redirect(url_for("index"))
    return render_template("new_shop.html", title="Grafiki - nowy sklep", form=form)


@app.route("/<path:path>")
def static_proxy(path):
    return app.send_static_file(path)


# Assigns user to the shop
@app.route("/workplace-worker-connect", methods=["GET", "POST"])
@login_required
def worker_to_workplace():
    if current_user.access_level != "0" and current_user.access_level != "1":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    form = UserToShopForm()
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


    users_number = len(workers_list)
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.worker.data).first()
        s = Shop.query.filter_by(shopname=form.workplace.data).first()
        already_assigned = s.works
        if u not in already_assigned:
            s.works.append(u)
            db.session.commit()
            flash("Przypisano %s do %s" %(u, s))
        else:
            flash("%s był już przypisany do %s" %(u, s))
        return redirect(url_for("worker_to_workplace"))
    return render_template("worker_to_workplace.html", title="Grafiki - przydzielanie użytkownika do sklepu",
                           form=form, workplaces=workplaces, users_number=users_number)


# jsonifies data for dynamicly generated checkboxes in worker_to_workplace()
@app.route("/workplace-worker-connect/<workplace>")
@login_required
def worker_to_workplace_workers(workplace):
    if current_user.access_level != "0" and current_user.access_level != "1" and current_user.access_level != "2":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))
    shop = Shop.query.filter_by(shopname=workplace).first()
    workers_appended = shop.works.all()
    workers_all = User.query.order_by(User.username).all()
    workers = []
    for worker in workers_all:
        if worker not in workers_appended:
            workers.append(worker)
    jsondict = []
    for worker in workers:
        workers_list = {}
        workers_list["name"] = worker.username
        jsondict.append(workers_list)
    return jsonify({"workers": jsondict})


# removes connection between user and shop
@app.route("/remove-user-from-shop", methods=["GET", "POST"])
@login_required
def remove_from_shop():
    if (current_user.access_level != "0") and (current_user.access_level != "1"):
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    user = request.args.get("user")
    shop = request.args.get("shop")
    u = User.query.filter_by(username=user).first()
    s = Shop.query.filter_by(shopname=shop).first()
    s.works.remove(u)
    db.session.commit()
    flash("Usunięto %s z %s"%(user, shop))
    return redirect(url_for("worker_to_workplace"))


# gets beginning and duration of billing period
@app.route("/billing-period", methods=["GET", "POST"])
@login_required
def billing_period():
    if (current_user.access_level != "0") and (current_user.access_level != "1"):
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))
    form = BillingPeriod()
    cur_begin = Billing_period.query.filter_by(id=1).first().begin
    cur_duration = Billing_period.query.filter_by(id=1).first().duration
    if form.validate_on_submit():
        begin = form.begin_month.data
        duration = form.length_of_billing_period.data
        if len(Billing_period.query.all()) == 0:
            bp = Billing_period(begin=begin, duration=duration)
            db.session.add(bp)
            db.session.commit()
        else:
            bp = Billing_period
            bp.query.filter_by(id=1).all()[0].begin=begin
            bp.query.filter_by(id=1).all()[0].duration = duration

            db.session.commit()
        return "OK"
    return render_template("billing_period.html", title="Grafiki - okres rozliczeniowy", form=form,
                           cur_begin=cur_begin, cur_duration=cur_duration)


# gets data for new schedule and creates new schedule template
"""
I'm not using calendar module's names for months and days because whole app has to be in polish,
    so the code is little more complicated.
"""
@app.route("/new-schedule", methods=["GET", "POST"])
@login_required
def new_schedule():
    if current_user.access_level != "0" and current_user.access_level != "1" and current_user.access_level != "2":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    workplaces = []
    workers_list = []
    form = NewScheduleForm()
    for workplace in Shop.query.order_by(Shop.shopname).all():
        workplaces.append((str(workplace), str(workplace)))
    form.workplace.choices = workplaces

    for worker in User.query.order_by(User.username).all():
        workers_list.append((str(worker), str(worker)))
    form.workers.choices = workers_list

    if form.validate_on_submit():
        workplace = form.workplace.data
        year = form.year.data
        month = form.month.data
        workers_list = form.workers.data
        hours = form.hours.data

        yearn = int(year)
        monthn = int(month)
        month_names = ["Styczeń", "luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień",
                       "Wrzesień", "Październik", "Listopad", "Grudzień"]
        month_name = month_names[(monthn) - 1]
        cal = calendar.Calendar()
        weekday_names = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

        schedule_name = "%s-%s-%s" %(year, month, workplace)
        check_schedule = Schedule.query.filter_by(name=schedule_name).first()
        if check_schedule is not None:
            flash("Taki grafik już istnieje")
            redirect(url_for("new_schedule"))
        else:
            workers = []
            for worker in workers_list:
                workers.append(str(worker).replace(" ", "_"))

            return render_template("empty_schedule.html", title="Grafiki - nowy grafik", workers=workers,
                                   shop=workplace, year=year, mn=month_name, cal=cal, wdn=weekday_names,
                                   monthn=monthn, yearn=yearn, hours=hours)

    return render_template("new_schedule.html", title="Grafiki - nowy grafik", form=form)


# jsonifies data for dynamicly generated checkboxes in new_schedule()
@app.route("/new-schedule/<workplace>")
@login_required
def new_schedule_find_workers(workplace):
    if current_user.access_level != "0" and current_user.access_level != "1" and current_user.access_level != "2":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))
    shop = Shop.query.filter_by(shopname=workplace).first()
    workers = shop.works.all()
    jsondict = []
    for worker in workers:
        workers_list = {}
        workers_list["name"] = worker.username
        jsondict.append(workers_list)
    return jsonify({"workers": jsondict})


@app.route('/schedule-to-db', methods=['POST'])
def new_schedule_to_db():
    data = request.json
    sname = ""
    syear = ""
    smonth = ""
    sworkplace = ""
    try:
        for dates in data.items():
            for day in dates:
                for element in day:
                    sname = "%s-%s-%s" %(element["year"], element["month"], element["workplace"])
                    syear = element["year"]
                    smonth = element["month"]
                    sworkplace = element["workplace"]
        schedule = Schedule(name=sname, year=syear, month=smonth, workplace=sworkplace)
        db.session.add(schedule)
        db.session.commit()
        for dates in data.items():
            for day in dates:
                for element in day:
                    d = date(int(element["year"]), int(element["month"]), int(element["day"]))
                    worker = element["worker"].replace("_", " ")
                    b_hour = element["from"]
                    e_hour = element["to"]
                    sum = element["sum"]
                    event = element["event"]
                    workplace = element["workplace"]
                    psname = "%s-%s-%s" %(d, worker, workplace)
                    pschedule = Personal_schedule(id=psname, date=d, worker=worker, begin_hour=b_hour,
                                                  end_hour=e_hour, hours_sum=sum, event=event, workplace=workplace,
                                                  includes=schedule)
                    db.session.add(pschedule)
        db.session.commit()
        return url_for("index")
    except (AttributeError):
        return "Popraw błędy w stworzonym grafiku."
    except:
        return "Coś poszło nie tak.\nPrawdopodobnie grafik już istnieje."