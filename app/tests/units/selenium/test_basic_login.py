import pytest
from selenium import webdriver
from app.tests.funcs.login_logout import log_in, log_out
from app.tests.funcs.get_users import add_user, remove_user


def test_login_page():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/login")
    assert "logowanie" in driver.title
    assert driver.current_url == "http://127.0.0.1:5000/login"
    driver.close()


def test_login_logout():
    username = "admin admin"
    password = "a"
    driver = webdriver.Chrome()
    log_in(username, password, driver)
    assert driver.current_url == "http://127.0.0.1:5000/index"
    log_out(username, driver)
    assert driver.current_url == "http://127.0.0.1:5000/login"
    driver.close()


@pytest.mark.xfail()
def test_add_user_and_login():
    driver = webdriver.Chrome()
    users = [("user 1", "a"), ("user 2", "b")]
    for user in users:
        username = user[0]
        password = user[1]
        add_user(username, password)
        log_in(username, password, driver)
        assert driver.current_url == "http://127.0.0.1:5000/index"
        log_out(username, driver)
        assert driver.current_url == "http://127.0.0.1:5000/login"
        remove_user(username)
    driver.close()
