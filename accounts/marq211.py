import time
from seleniumrequests import Chrome


def get_web_driver(url, username, password):
    driver = Chrome()

    driver.get(url)
    driver.implicitly_wait(1)  # seconds
    driver.find_element_by_id("loginuser").send_keys(username)
    driver.find_element_by_id("loginpass").send_keys(password)
    return driver


def get_rent(login_details):
    url, username, password = login_details.get_login_details('marq211')
    driver = get_web_driver(url, username, password + '\n')
    driver.implicitly_wait(4)
    driver.find_element_by_link_text('My Home').click()
    driver.implicitly_wait(9)
    text = driver.find_element_by_id('totalupcomingcharges').get_attribute('innerHTML')
    value = text.split('$')[1].split('</span>')[0].replace(',', '')
    logout(driver)
    return value


def logout(driver):
    driver.find_element_by_link_text('Sign out').click()
    driver.quit()
