"""Fixtures for pytest"""

import pytest
from selenium import webdriver

from app import app, db
from app.models import User
from app.tests.units.selenium.funcs import login_logout, get_users


@pytest.fixture(scope="function")
def client():
    true_db = app.config["SQLALCHEMY_DATABASE_URI"]
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    yield app.test_client()
    app.config["TESTING"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = true_db


@pytest.fixture(scope="function")
def init_database():
    db.create_all()
    user1 = User(username="test admin", access_level="0")
    user1.set_password("test_pswd")
    db.session.add(user1)
    db.session.commit()
    yield db
    db.drop_all()


@pytest.fixture(scope="function")
def sel_log_admin():
    driver = webdriver.Chrome()
    get_users.add_user("a", "a", "0")
    login_logout.log_in("a", "a", driver)
    yield driver
    get_users.remove_user("a")
    driver.close()
