import time
from seleniumrequests import Chrome


def get_web_driver(url, username, password):
    driver = Chrome()

    driver.get(url)
    driver.implicitly_wait(1)  # seconds
    driver.find_element_by_id("ctl00_Main_LoginBox_UserName").send_keys(username)
    driver.find_element_by_id("ctl00_Main_LoginBox_Password").send_keys(password)
    return driver


def get_electricity_bill(login_details):
    url, username, password = login_details.get_login_details('seattle_city_light')
    driver = get_web_driver(url, username, password + '\n')
    driver.find_element_by_id("ctl00_Main_txtAnswer").send_keys(login_details.get_security_answer('seattle_city_light') + '\n')
    text = driver.find_element_by_id('Amt').get_attribute('innerHTML')
    value = text.replace('$', '')
    logout(driver)
    return value


def logout(driver):
    driver.find_element_by_link_text('Logout').click()
    driver.quit()
