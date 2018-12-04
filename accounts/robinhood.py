import time
from seleniumrequests import Chrome


def get_web_driver(url, username, password):
    driver = Chrome()

    driver.get(url)
    driver.implicitly_wait(5)  # seconds
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    time.sleep(10)
    return driver


def get_value(login_details):
    url, username, password = login_details.get_login_details('robinhood')
    driver = get_web_driver(url, username, password + '\n')
    text = driver.find_element_by_class_name('_2YApulnV3lazBStOvoKx6m').get_attribute('innerHTML')
    logout(driver)
    text = text.split('</span>')
    value = ''
    for ele in text:
        if ele:
            ele = ele.split('>')[1] 
            if ele != ',' and ele != '$': 
                value = value + ele
    return value


def logout(driver):
    driver.find_element_by_link_text('Account').click()
    driver.find_element_by_link_text('Log Out').click()
    driver.quit()
