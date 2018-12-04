# Mint-Integration
This project supports mint integration with Robinhood, Seattle City Lights, HDFC Bank, Realpage and similar unsupported accounts by Mint.

# How to use this?
Install all the requirements mentioned in file requirements.txt. Use pip install with python 2.7

# Steps to get started
* Mint provide 2 options for accounts not supported right now. You can add it as property or bill. For example, if you have a bank account not supported under Mint, you can add it as property. Similary, for electricty bill, you can add it as Bill.
Add such accounts in the mint and note down the names of these accounts.
* Details about accounts are saved in 3 files: secret/login_details.json, properties/login_details.json and properties/mint_accounts.json. secret/login_details.json contains actual username and passwords of the accounts added above in mint. Replace accounts which are not needed. Replace username and password with your actual username and passwords. This file will be used to update properties/login_details.json. Remove accounts from properties/login_details.json which are not needed.
* Run lib/login_details_manager.py . It will ask for a passphrase. Remember this passphrase. This will be used to encrypt your usernames and passwords. These will be encoded and written down to properties/login_details.json. Now, you can move your secret/login_details.json to some place safe. This file will be needed if you ever update your username, password or want to update your passphrase.
* There is a file properties/mint_accounts.json which stores the details of the accounts added in mint as property or bill. Removed the accounts which are not needed. Update the names of the accounts(Account name is key in the dictionary in json file). Update the due date as needed. Due date represents the day of the month.
* Run driver.py. It will ask for the passphrase which you had used while encrypting your secret details. This will fetch the details from mentioned accounts and update your mint profile. 

# How to add a new account?
* You need to add the details in secret/login_details.json, properties/login_details.json and properties/mint_accounts.json
* Create a new file under accounts directory for your new account. Add functions similar to other accounts so that selenium can login and get the required details.
