import json

import time
from lxml import html
from datetime import datetime
from seleniumrequests import Chrome

MINT_OVERVIEW_URL = 'https://mint.intuit.com/overview.event'
URL_PREFIX = 'https://mint.intuit.com/mas/'


def get_web_driver(email, password):
    driver = Chrome()

    driver.get("https://www.mint.com")
    driver.implicitly_wait(5)  # seconds
    driver.find_element_by_link_text("Log In").click()

    driver.find_element_by_id("ius-userid").send_keys(email)
    driver.find_element_by_id("ius-password").send_keys(password)
    driver.find_element_by_id("ius-sign-in-submit-btn").submit()

    # Wait until logged in, just in case we need to deal with MFA.
    while not driver.current_url.startswith(
            'https://mint.intuit.com/overview.event'):
        time.sleep(1)

    # Wait until the overview page has actually loaded.
    driver.implicitly_wait(5)  # seconds
    driver.find_element_by_id("transaction")

    return driver


class Mint:

    browser_auth_api_key = None
    mint_user_id = None
    token = None
    driver = None

    def __init__(self, email=None, password=None):
        if email and password:
            self.login_and_get_token(email, password)

    def login_and_get_token(self, email, password):
        if self.token and self.driver:
            return

        self.driver = get_web_driver(email, password)
        self.token = self.get_token()

        doc = html.document_fromstring(self.get(MINT_OVERVIEW_URL).text)
        self.mint_user_id = json.loads(doc.get_element_by_id('javascript-user').value)['userId']
        self.browser_auth_api_key = self.driver.execute_script('return window.MintConfig.browserAuthAPIKey')

    def get_token(self):
        value_json = self.driver.find_element_by_name(
            'javascript-user').get_attribute('value')
        return json.loads(value_json)['token']

    def get(self, url, **kwargs):
        return self.driver.request('GET', url, **kwargs)

    def patch(self, url, **kwargs):
        self.driver.request('PATCH', url, **kwargs)

    def get_accounts(self):
        response = self.get(url= URL_PREFIX + 'v1/providers',
                  headers={
                      'authorization':
                          'Intuit_APIKey intuit_apikey={}, intuit_apikey_version=1.0'.format(
                              self.browser_auth_api_key),
                      'content-type': 'application/json'
                  })
        return json.loads(response.text)

    def update_value(self, account, new_value, local_account):
        json_data = self.get_json_for_update(account=account, new_value=new_value, local_account=local_account)
        return self.patch(URL_PREFIX + json_data['url'],
                   json=json_data['input'],
                   headers={
                       'authorization':
                           'Intuit_APIKey intuit_apikey={}, intuit_apikey_version=1.0'.format(
                               self.browser_auth_api_key),
                       'content-type': 'application/json'
                   })

    @classmethod
    def get_json_for_update(cls, account, new_value, local_account):
        account_type = account['providerAccounts'][0]['type']
        if account_type == 'OtherPropertyAccount':
            return {
                'input': {
                    'name': account['providerAccounts'][0]['name'],
                    'value': new_value,
                    'type': 'OtherPropertyAccount'
                },
                'url': account['providerAccounts'][0]['metaData']['link'][0]['href']
            }
        elif account_type == 'MANUAL_BILL':
            return {
                'input': {
                    'dueAmount': new_value,
                    'dueDate': str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + local_account['due_date'],
                    'frequency': 'MONTH',
                    'id': account['id'],
                    'name': account['name'],
                    'repeatInterval': '1',
                    'staticProviderRef': {
                        'name': account['name'],
                        'type': account['providerAccounts'][0]['bills']['bill'][0]['providerCategory']
                    },
                    'type': 'MANUAL_BILL'
                },
                'url': account['metaData']['link'][4]['href']
            }

    def logout(self):
        self.driver.find_element_by_id('link-logout').click()
        self.driver.close()
