"""functions for logging in and logging out tests"""

from selenium.webdriver.common.keys import Keys


def log_in(username, password, driver):
    driver.get("http://127.0.0.1:5000/login")
    user_elem = driver.find_element_by_id("username")
    user_elem.clear()
    user_elem.send_keys(username)
    pswd_elem = driver.find_element_by_id("password")
    pswd_elem.clear()
    pswd_elem.send_keys(password)
    pswd_elem.send_keys(Keys.RETURN)


def log_out(username, driver):
    logout_elem = driver.find_element_by_link_text("Wyloguj %s" % username)
    logout_elem.click()
