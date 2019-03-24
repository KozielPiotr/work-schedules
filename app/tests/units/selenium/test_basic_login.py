
from selenium import webdriver

from app.tests.units.selenium.funcs import login_logout, get_users


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
    login_logout.log_in(username, password, driver)
    assert driver.current_url == "http://127.0.0.1:5000/index"
    assert "Wyloguj %s" % username in driver.page_source
    login_logout.log_out(username, driver)
    assert driver.current_url == "http://127.0.0.1:5000/login"
    driver.close()


def test_add_user_and_login():
    driver = webdriver.Chrome()
    users = [("user 1", "a", "0"), ("user 2", "b", "1")]
    for user in users:
        username = user[0]
        password = user[1]
        access = user[2]
        get_users.add_user(username, password, access)
        login_logout.log_in(username, password, driver)
        assert driver.current_url == "http://127.0.0.1:5000/index"
        assert "Wyloguj %s" % username in driver.page_source
        login_logout.log_out(username, driver)
        assert driver.current_url == "http://127.0.0.1:5000/login"
        get_users.remove_user(username)
    driver.close()


def test_access_levels():
    driver = webdriver.Chrome()
    acc_levels = ["0", "1", "2", "3"]
    for level in acc_levels:
        get_users.add_user("a", "a", level)
        login_logout.log_in("a", "a", driver)
        assert "Wyloguj a" in driver.page_source
        if level == "0":
            assert '<h5 class="card-title">Administrator</h5>' in driver.page_source
            assert '<h5 class="card-title">Kierownik działu</h5>' in driver.page_source
            assert '<h5 class="card-title">Kierownik</h5>' in driver.page_source
            assert '<h5 class="card-title">Użytkownik</h5>' in driver.page_source
        elif level == "1":
            assert '<h5 class="card-title">Kierownik działu</h5>' in driver.page_source
            assert '<h5 class="card-title">Kierownik</h5>' in driver.page_source
            assert '<h5 class="card-title">Użytkownik</h5>' in driver.page_source
            assert '<h5 class="card-title">Administrator</h5>' not in driver.page_source
        elif level == "2":
            assert '<h5 class="card-title">Kierownik</h5>' in driver.page_source
            assert '<h5 class="card-title">Użytkownik</h5>' in driver.page_source
            assert '<h5 class="card-title">Administrator</h5>' not in driver.page_source
            assert '<h5 class="card-title">Kierownik działu</h5>' not in driver.page_source
        elif level == "3":
            assert '<h5 class="card-title">Użytkownik</h5>' in driver.page_source
            assert '<h5 class="card-title">Administrator</h5>' not in driver.page_source
            assert '<h5 class="card-title">Kierownik działu</h5>' not in driver.page_source
            assert '<h5 class="card-title">Kierownik</h5>' not in driver.page_source
        login_logout.log_out("a", driver)
        get_users.remove_user("a")
    driver.close()
