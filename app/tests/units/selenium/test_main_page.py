#-*- coding: utf-8 -*-

from selenium import webdriver

from app.tests.units.selenium.funcs import login_logout, get_users


def test_index_links():
    driver = webdriver.Chrome()
    acc_levels = ["0", "1", "2", "3"]
    links = {"0": [("billing-period", "Grafiki - okres rozliczeniowy"), ("new-user", "Grafiki - nowy użytkownik"),
                   ("admin-psw-change", "Grafiki - zmiana hasła"), ("new-workplace", "Grafiki - nowy sklep"),
                   ("assign-worker", "Grafiki - przydzielanie użytkownika do sklepu")],
             "1": [("unaccepted", "Grafiki - niezaakceptowane grafiki"), ("guidelines", "Grafiki - wytyczne")],
             "2": [("new-schedule", "Grafiki - nowy grafik"), ("modify-schedule", "Grafiki - modyfikowalne grafiki")],
             "3": [("show-schedule", "Grafiki - podgląd grafiku"), ("export-schedule", "Grafiki - podgląd grafiku"),
                   ("change-password", "Grafiki - zmiana hasła")]}

    for level in acc_levels:
        get_users.add_user("a", "a", level)
        login_logout.log_in("a", "a", driver)
        for link in links:
            if int(link) >= int(level):
                for button in links[link]:
                    driver.find_element_by_id(button[0]).click()
                    assert button[1] in driver.title
                    driver.get("http://127.0.0.1:5000/index")
        login_logout.log_out("a", driver)
        get_users.remove_user("a")
    driver.close()
