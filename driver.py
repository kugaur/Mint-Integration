from accounts import hdfc_bank, robinhood, seattle_lights, marq211
from lib import login_details_manager, mint
import json


if __name__ == '__main__':

    login_details = login_details_manager.LoginDetailsManager()

    # Get Mint Accounts to update
    mint_accounts = json.load(open('properties/mint_accounts.json'))

    # Login into Mint
    mint_url, mint_username, mint_password = login_details.get_login_details("mint")
    mint = mint.Mint(mint_username, mint_password)
    accounts = mint.get_accounts()['providers']
    for account in accounts:
        account_name = account['providerAccounts'][0]['name']
        if mint_accounts.has_key(account_name):
            acc = mint_accounts[account_name]
            new_value = eval(acc['callback'])(login_details)
            mint.update_value(account=account, new_value=new_value, local_account=acc)

    mint.logout()
