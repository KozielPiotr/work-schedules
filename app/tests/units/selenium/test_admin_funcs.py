#-*- coding: utf-8 -*-

from datetime import datetime
from selenium.webdriver.support.ui import Select

from app import db
from app.models import Billing_period, User, Shop
from app.tests.units.selenium.funcs import get_users
from app.tests.fixtures import sel_log_admin


def test_billing_period(sel_log_admin):
    driver = sel_log_admin
    driver.get("http://127.0.0.1:5000/billing-period")

    month_elem = Select(driver.find_element_by_id("begin_month"))
    year_elem = driver.find_element_by_id("begin_year")
    length_elem = driver.find_element_by_id("length_of_billing_period")
    month_elem.select_by_visible_text("Kwiecień")
    year_elem.send_keys("2019")
    length_elem.send_keys("5")
    driver.find_element_by_id("submit").click()

    bp = Billing_period.query.filter_by(id=1).first()
    assert bp.begin == datetime(2019, 4, 1)
    assert bp.duration == 5
    bp.begin = datetime(2018, 1, 1)
    bp.duration = 3
    db.session.commit()


def test_new_user(sel_log_admin):
    driver = sel_log_admin
    driver.get("http://127.0.0.1:5000/new-user")
    acc_levels = ["0", "1", "2", "3"]
    username = "test user"
    password = "test password"

    for level in acc_levels:
        username_elem = driver.find_element_by_id("username")
        pswd_elem = driver.find_element_by_id("password")
        pswd2_elem = driver.find_element_by_id("password2")
        acc_elem = Select(driver.find_element_by_id("access_level"))

        username_elem.send_keys(username)
        pswd_elem.send_keys(password)
        pswd2_elem.send_keys(password)
        acc_elem.select_by_value(level)
        driver.find_element_by_id("submit").click()

        user = User.query.filter_by(username=username).first()
        assert user.username == username
        assert user.access_level == level
        assert user.check_password(password) is True
        get_users.remove_user(username)


def test_change_users_password(sel_log_admin):
    driver = sel_log_admin
    username = "test user"
    pswd = "test password"
    pswd_changed = "changed password"
    get_users.add_user(username, pswd, "3")
    driver.get("http://127.0.0.1:5000/admin-password-change")

    user_elem = Select(driver.find_element_by_id("worker"))
    pswd_elem = driver.find_element_by_id("new_password1")
    pswd2_elem = driver.find_element_by_id("new_password2")

    user_elem.select_by_value(username)
    pswd_elem.send_keys(pswd_changed)
    pswd2_elem.send_keys(pswd_changed)
    driver.find_element_by_id("submit").click()

    test_user = User.query.filter_by(username=username).first()
    assert test_user.check_password(pswd_changed) is True
    get_users.remove_user(username)


def test_new_workplace(sel_log_admin):
    driver = sel_log_admin
    workplace_name = "test workplace"
    driver.get("http://127.0.0.1:5000/new-workplace")

    workplace_elem = driver.find_element_by_id("workplace_name")

    workplace_elem.send_keys(workplace_name)
    driver.find_element_by_id("submit").click()

    workplace = Shop.query.filter_by(shopname=workplace_name).first()
    assert workplace is not None
    db.session.delete(workplace)
    db.session.commit()


def test_assign_disassign_worker(sel_log_admin):
    driver = sel_log_admin
    workplace_name = "test workplace"
    new_workplace = Shop(shopname=workplace_name)
    db.session.add(new_workplace)
    db.session.commit()
    test_user = "test user"
    get_users.add_user(test_user, "test password", "3")
    driver.get("http://127.0.0.1:5000/workplace-worker-connect")

    workplace_elem = Select(driver.find_element_by_id("workplace"))
    worker_elem = Select(driver.find_element_by_id("worker"))

    workplace_elem.select_by_value(workplace_name)
    worker_elem.select_by_value(test_user)
    driver.find_element_by_id("submit").click()

    workplace = Shop.query.filter_by(shopname=workplace_name).first()
    user = User.query.filter_by(username=test_user).first()

    assert user in workplace.works.all()

    driver.get("http://127.0.0.1:5000/workplace-worker-connect")
    driver.find_element_by_id(workplace_name).click()
    driver.find_element_by_id("remove-%s" % test_user).click()
    assert user not in workplace.works.all()

    db.session.delete(new_workplace)
    db.session.delete(User.query.filter_by(username=test_user).first())
    db.session.commit()
