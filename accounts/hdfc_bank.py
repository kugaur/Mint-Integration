from seleniumrequests import Chrome
from lib import currency_converter


def get_web_driver(url, username, password):
    driver = Chrome()

    driver.get(url)
    driver.implicitly_wait(1)  # seconds
    driver.switch_to_frame("login_page")
    driver.find_element_by_name("fldLoginUserId").send_keys(username)
    driver.implicitly_wait(3)
    driver.find_element_by_id('chkrsastu').click()
    driver.find_element_by_name("fldPassword").send_keys(password)
    driver.implicitly_wait(5)
    return driver


def get_balance(login_details):
    url, username, password = login_details.get_login_details('hdfc_bank')
    driver = get_web_driver(url, username + '\n', password + '\n')
    driver.switch_to_default_content()
    driver.switch_to_frame("main_part")
    summary = str(driver.find_element_by_id('SavingTotalSummary').text)
    summary = summary.replace(',', '')
    logout(driver)
    return currency_converter.rupee_to_dolar(float(summary.split()[-1]))


def logout(driver):
    driver.switch_to_default_content()
    driver.switch_to_frame("common_menu1")
    driver.find_element_by_xpath('//*[@title="Log Out"]').click()
    driver.implicitly_wait(5)
    driver.switch_to_default_content()
    driver.quit()


def get_emi(login_details):
    return currency_converter.rupee_to_dolar(22868)