from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, NewUserForm, NewShopForm, UserToShopForm, NewScheduleChoice
from app.models import User, Shop
import calendar


# welcome page
@app.route("/")
@app.route("/index")
#@login_required
def index():
    return render_template("index.html", title="Grafiki")


# Login page. Checks if user is logged in and in not allows to log in
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
#@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


#  New user
@app.route("/new-user", methods=["GET", "POST"])
#@login_required
def new_user():
    #if current_user.access_level != "a":
        #flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        #return redirect(url_for("index"))
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, access_level=form.access_level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Nowy użytkownik zarejestrowany")
        return redirect(url_for("index"))
    return render_template("new_user.html", title="Grafiki - nowy użytkownik", form=form)


# New shop
@app.route("/new-shop", methods=["GET", "POST"])
#@login_required
def new_shop():
    # if current_user.access_level != "a":
        # flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        # return redirect(url_for("index"))
    form = NewShopForm()
    if form.validate_on_submit():
        shop = Shop(shopname=form.shopname.data)
        db.session.add(shop)
        db.session.commit()
        flash("Stworzono nowy sklep")
        return redirect(url_for("index"))
    return render_template("new_shop.html", title="Grafiki - nowy sklep", form=form)


# Assigns user to the shop
@app.route("/shop-user-connect", methods=["GET", "POST"])
#@login_required
def user_to_shop():
    # if current_user.access_level != "a":
        # flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        # return redirect(url_for("index"))
    form = UserToShopForm()
    shop = Shop.query.order_by(Shop.shopname).all()
    user = User.query.order_by(User.username).all()
    users_number = len(user)
    if form.validate_on_submit():
        u = form.user.data
        s = form.shop.data
        already_assigned = s.works
        if u not in already_assigned:
            s.works.append(u)
            db.session.commit()
            flash("Przypisano %s do %s" %(u, s))
        else:
            flash("%s był już przypisany do %s" %(u, s))
        return redirect(url_for("user_to_shop"))
    return render_template("user_to_shop.html", title="Grafiki - przydzielanie użytkownika do sklepu", form=form,
                           user=user, shop=shop, users_number=users_number)


# removes connection between user and shop
@app.route("/remove-user-from-shop", methods=["GET", "POST"])
#@login_required
def remove_from_shop():
    #if current_user.access_level != "a":
        #flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        #return redirect(url_for("index"))
    user = request.args.get("user")
    shop = request.args.get("shop")
    u = User.query.filter_by(username=user).first()
    s = Shop.query.filter_by(shopname=shop).first()
    s.works.remove(u)
    db.session.commit()
    flash("Usunięto %s z %s"%(user, shop))
    return redirect(url_for("user_to_shop"))


@app.route("/new-schedule", methods=["GET", "POST"])
@login_required
def new_schedule():
    if (current_user.access_level != "a") and (current_user.access_level != "m"):
        flash("Użytkownik nie ma uprawnień do wyświetlenia tej strony")
        return redirect(url_for("index"))
    form = NewScheduleChoice()
    u = current_user.workers_shop
    users_shops = []
    for i in u:
        users_shops.append((str(i), str(i)))

    form.shop.choices = users_shops
    if form.validate_on_submit():
        s = form.shop.data
        y = form.year.data
        m = form.month.data
        flash("Tworzenie grafiku dla sklepu %s na rok %s, miesiąc %s" %(s, y, m))
        return redirect(url_for("create_schedule"))
    return render_template("new_schedule.html", title="Grafiki - nowy grafik", form=form)


@app.route("/create-schedule", methods=["GET", "POST"])
@login_required
def create_schedule():
    return render_template("empty_schedule.html", title="Grafiki - nowy grafik")

"""
@app.route("/test-fields", methods=["GET", "POST"])
def test_fields():
    users = User.query.all()
    form = Test()
    return render_template("test_fields.html", title="Grafiki - test", form=form, users=users)
"""