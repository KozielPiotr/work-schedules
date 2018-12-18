from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, NewUserForm, NewShopForm, UserToShopForm, NewScheduleForm, BillingPeriod
from app.models import User, Shop, Billing_period, Personal_schedule, Schedule
import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def prev_schedule(month, year, month_names, cal, workplace):
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    prev_month_name = month_names[prev_month - 1]

    try:
        prev_month_last_version = Schedule.query.filter_by(year=prev_year, month=prev_month, workplace=workplace,
                                                           accepted=True).order_by(
            Schedule.version.desc()).first().version
        prev_month_shd = Schedule.query.filter_by(year=prev_year, month=prev_month, workplace=workplace,
                                                  version=prev_month_last_version).first()
    except(AttributeError):
        prev_month_shd = None

    if prev_month_shd is not None:
        prev_workers = []
        for pers_schedule in prev_month_shd.ind:
            if str(pers_schedule.worker).replace(" ", "_") not in prev_workers:
                prev_workers.append(str(pers_schedule.worker).replace(" ", "_"))

        prev_hours = prev_month_shd.hrs_to_work
        prev_shdict = {}
        workers_hours = {}
        for worker in prev_workers:
            worker_hours = 0
            for p_schedule in prev_month_shd.ind:
                if p_schedule.worker == str(worker).replace("_", " "):
                    worker_hours += p_schedule.hours_sum
                workers_hours[worker] = worker_hours

        for worker in prev_workers:
            for day in cal.itermonthdays(prev_year, prev_month):
                if day > 0:
                    begin = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                              worker=worker.replace("_", " ")).first().begin_hour
                    end = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                            worker=worker.replace("_", " ")).first().end_hour
                    event = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                              worker=worker.replace("_", " ")).first().event
                    sum = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                            worker=worker.replace("_", " ")).first().hours_sum
                    billing_week = Personal_schedule.query.filter_by(date=datetime(prev_year, prev_month, day),
                                                                     worker=worker.replace("_",
                                                                                           " ")).first().billing_week

                    prev_shdict["begin-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = begin
                    prev_shdict["end-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = end
                    prev_shdict["event-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = event
                    prev_shdict["sum-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = sum
                    prev_shdict["billing-week-%s-%d-%02d-%02d" % (worker, prev_year, prev_month, day)] = billing_week
    else:
        prev_shdict = None
        prev_hours = None
        prev_workers = None
        workers_hours = None
    prev = {}
    prev["prev_shdict"] = prev_shdict
    prev["hours"] = prev_hours
    prev["workers"] = prev_workers
    prev["workers_hours"] = workers_hours
    prev["year"] = prev_year
    prev["month"] = prev_month
    prev["month_name"] = prev_month_name
    prev["year"] = prev_year

    return prev


# main page
@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Grafiki")


@app.route("/test", methods=["GET", "POST"])
def test():
    queries = []
    months = Schedule.query.filter_by(month=11)
    places = Schedule.query.filter_by(workplace="Sklep 1")
    for month in months:
        if month in places:
            queries.append(month.name)
    print(queries)
    return "%s"


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
        if not next_page or url_parse(next_page).netloc != "":
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
            flash("Przypisano %s do %s" % (u, s))
        else:
            flash("%s był już przypisany do %s" % (u, s))
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
    flash("Usunięto %s z %s" % (user, shop))
    return redirect(url_for("worker_to_workplace"))


# gets beginning and duration of billing period
@app.route("/billing-period", methods=["GET", "POST"])
@login_required
def billing_period():
    if (current_user.access_level != "0") and (current_user.access_level != "1"):
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))
    form = BillingPeriod()
    if Billing_period.query.filter_by(id=1).first() is None:
        cur_begin = 1
    else:
        cur_begin = "{: %d - %m - %Y}".format(Billing_period.query.filter_by(id=1).first().begin)

    if Billing_period.query.filter_by(id=1).first() is None:
        cur_duration = 3
    else:
        cur_duration = Billing_period.query.filter_by(id=1).first().duration

    if form.validate_on_submit():
        begin = datetime(int(form.begin_year.data), int(form.begin_month.data), 1)
        duration = form.length_of_billing_period.data
        if len(Billing_period.query.all()) == 0:
            bp = Billing_period(begin=begin, duration=duration)
            db.session.add(bp)
            db.session.commit()
        else:
            bp = Billing_period
            bp.query.filter_by(id=1).all()[0].begin = begin
            bp.query.filter_by(id=1).all()[0].duration = duration
            db.session.commit()
        flash("Zmieniono okres rozliczeniowy na: Początek: %s Długość: %s" % ("{:%d - %m - %Y}".format(begin), duration))
        return redirect(url_for("index"))
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
    c_user = User.query.filter_by(username=str(current_user)).first()
    for workplace in c_user.workers_shop:
        workplaces.append((str(workplace), str(workplace)))
    form.workplace.choices = workplaces

    for worker in User.query.order_by(User.access_level).all():
        workers_list.append((str(worker), str(worker)))
    form.workers.choices = workers_list

    if form.validate_on_submit():
        workplace = form.workplace.data
        year = int(form.year.data)
        month = int(form.month.data)
        hours = form.hours.data
        month_names = ["Styczeń", "luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień",
                       "Wrzesień", "Październik", "Listopad", "Grudzień"]
        month_name = month_names[month - 1]
        cal = calendar.Calendar()
        weekday_names = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

        schedule_name = "%s-%s-%s" % (year, month, workplace)
        check_schedule = Schedule.query.filter_by(name=schedule_name).first()
        if check_schedule is not None:
            flash("Taki grafik już istnieje")
            redirect(url_for("index"))
        else:
            workers_to_schd = []
            for worker in form.workers.data:
                workers_to_schd.append(str(worker).replace(" ", "_"))

            prev = prev_schedule(month, year, month_names, cal, workplace)
            print()
            #try:
            return render_template("empty_schedule.html", title="Grafiki - nowy grafik", workers=workers_to_schd,
                                   shop=workplace, year=year, month=month, mn=month_name, cal=cal, wdn=weekday_names,
                                   hours=hours, Billing_period=Billing_period,
                                   prev_shdict=prev["prev_shdict"], prev_month=prev["month"],
                                   prev_month_name=prev["month_name"], prev_year=prev["year"],
                                   prev_hours=prev["hours"], prev_workers=prev["workers"],
                                   workers_hours=prev["workers_hours"])
            #except:
                #flash("Sprawdź, czy jest ustawiony początek okresu rozliczeniowego")
                #redirect(url_for("new_schedule"))

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
    for worker in shop.works.all():
        workers_list = {}
        if worker.access_level == "0" or worker.access_level == "1":
            workers.remove(worker)
        else:
            workers_list["name"] = worker.username
            jsondict.append(workers_list)
    return jsonify({"workers": jsondict})


@app.route('/schedule-to-db/<action>', methods=['POST'])
@login_required
def new_schedule_to_db(action):
    if current_user.access_level != "0" and current_user.access_level != "1" and current_user.access_level != "2":
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    def ind_schedules_to_db(data):
        for element in data["ind_schedules"]:
            print(element["year"])
            print(element["month"])
            print(element["day"])
            d = date(int(element["year"]), int(element["month"]), int(element["day"]))
            worker = element["worker"].replace("_", " ")
            b_hour = element["from"]
            e_hour = element["to"]
            sum = element["sum"]
            event = element["event"]
            workplace = element["workplace"]
            psname = "%s-%s-%s" % (d, worker, workplace)
            billing_week = element["billing_week"]
            pschedule = Personal_schedule(name=psname, date=d, worker=worker, begin_hour=b_hour,
                                          end_hour=e_hour, hours_sum=sum, event=event, workplace=workplace,
                                          includes=schedule, billing_period=billing_period, billing_week=billing_week)
            db.session.add(pschedule)
        db.session.commit()

    data = request.json
    unaccepted_schedule = Schedule.query.filter_by(name="%s-%s-%s" % (data["main_data"]["year"], data["main_data"]["month"],
                                                                  data["main_data"]["workplace"]), accepted=False).first()


    # accepting changes in already existing schedule
    if unaccepted_schedule is not None and action == "acc":
        print("Znalazłem niezaakceptowany grafik")
        name = unaccepted_schedule.name
        year = unaccepted_schedule.year
        month= unaccepted_schedule.month
        workplace = unaccepted_schedule.workplace
        hours = unaccepted_schedule.hrs_to_work
        accepted = True
        version = unaccepted_schedule.version + 1
        billing_period = unaccepted_schedule.billing_period
        schedule = Schedule(name=name, year=year, month=month, workplace=workplace, hrs_to_work=hours,
                            accepted=accepted, version=version, billing_period=billing_period)
        db.session.add(schedule)
        db.session.commit()

        for ind_schedule in unaccepted_schedule.ind:
            db.session.delete(ind_schedule)
        db.session.delete(unaccepted_schedule)

        ind_schedules_to_db(data)


    # adding unaccepted version of schedule


    # adding new schedule to db
    elif unaccepted_schedule is None:
        print("Nie znalazłem niezaakceptowanego grafiku")
        name = "%s-%s-%s" % (data["main_data"]["year"], data["main_data"]["month"], data["main_data"]["workplace"])
        year = int(data["main_data"]["year"])
        month = int(data["main_data"]["month"])
        workplace = data["main_data"]["workplace"]
        hours = data["main_data"]["hours"]
        billing_period = int(data["main_data"]["billing_period"])
        schedule = Schedule(name=name, year=year, month=month, workplace=workplace, hrs_to_work=hours,
                            accepted=False, version=0, billing_period=billing_period)
        db.session.add(schedule)
        db.session.commit()

        ind_schedules_to_db(data)

    return url_for("index")
    #except (AttributeError):
        #return "1"
    #except:
        #return "2"


# makes list of unaccepted schedule for current user
@app.route("/unaccepted_schedules", methods=["GET", "POST"])
@login_required
def unaccepted_schedules():
    if (current_user.access_level != "0") and (current_user.access_level != "1"):
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    unaccepted_schedules = []
    for schedule in Schedule.query.filter_by(accepted=False).order_by(Schedule.workplace, Schedule.year, Schedule.month).all():
        for assigned_workplaces in current_user.workers_shop:
            if str(schedule.workplace) == str(assigned_workplaces):
                unaccepted_schedules.append(schedule)

    schedule_number = len(unaccepted_schedules)

    return render_template("schedules-to-accept.html", title="Grafiki - niezaakceptowane grafiki", ua=unaccepted_schedules,
                           sn=schedule_number, Schedule=Schedule)


# creates modifiable template with unaccepted schedule
@app.route("/accept-schedule", methods=["GET", "POST"])
@login_required
def accept_schedule():
    if (current_user.access_level != "0") and (current_user.access_level != "1"):
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))

    schedule = Schedule.query.filter_by(name=request.args.get("schd"), accepted=False).first()
    workplace = schedule.workplace
    year = schedule.year
    month = schedule.month
    hours = schedule.hrs_to_work
    workers = []
    for pers_schedule in schedule.ind:
        if str(pers_schedule.worker).replace(" ", "_") not in workers:
            workers.append(str(pers_schedule.worker).replace(" ", "_"))

    month_names = ["Styczeń", "luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień",
                   "Wrzesień", "Październik", "Listopad", "Grudzień"]
    weekday_names = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
    month_name = month_names[month - 1]
    cal = calendar.Calendar()

    prev = prev_schedule(month, year, month_names, cal, workplace)

    shdict = {}
    for worker in workers:
        for day in cal.itermonthdays(year, month):
            if day > 0:
                begin = Personal_schedule.query.filter_by(date=datetime(year, month, day),
                                                          worker=worker.replace("_", " ")).first().begin_hour
                end = Personal_schedule.query.filter_by(date=datetime(year, month, day),
                                                          worker=worker.replace("_", " ")).first().end_hour
                event = Personal_schedule.query.filter_by(date=datetime(year, month, day),
                                                        worker=worker.replace("_", " ")).first().event
                if begin == 0:
                    begin = ""
                shdict["begin-%s-%d-%02d-%02d" % (worker, year, month, day)] = begin
                if end == 0:
                    end = ""
                shdict["end-%s-%d-%02d-%02d" % (worker, year, month, day)] = end
                shdict["event-%s-%d-%02d-%02d" % (worker, year, month, day)] = event

    return render_template("accept-schedule.html", title="Grafiki - akceptacja grafiku", schedule=schedule,
                           workplace=workplace, year=year, month=month, workers=workers, month_name=month_name,
                           wdn=weekday_names, cal=cal, Billing_period=Billing_period, shdict=shdict,
                           prev_shdict=prev["prev_shdict"], hours=hours, prev_month=prev["month"],
                           prev_month_name=prev["month_name"], prev_year=prev["year"], prev_hours=prev["hours"],
                           prev_workers=prev["workers"], workers_hours=prev["workers_hours"])