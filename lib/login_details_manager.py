from simplecrypt import encrypt, decrypt
import json
import getpass
import base64

PROPERTIES_FILE = 'properties/login_details.json'
SOURCE_LOGIN_FILE = 'secret/login_details.json'


class LoginDetailsManager:

    def __init__(self):
        key = getpass.getpass("Enter the passphrase: ")
        self.key = key

    def get_login_details(self, entity):
        json_file = open(PROPERTIES_FILE, 'rb')
        data = json.load(json_file)
        url = data[entity]["url"]
        username = decrypt(self.key, base64.b64decode(data[entity]["username"]))
        password = decrypt(self.key, base64.b64decode(data[entity]["password"]))
        return url, username, password

    def get_security_answer(self, entity):
        json_file = open(PROPERTIES_FILE, 'rb')
        data = json.load(json_file)
        return decrypt(self.key, base64.b64decode(data[entity]['security_answer']))


def update_login_details(key):
    source_file = open(SOURCE_LOGIN_FILE, 'rb')
    source_data = json.load(source_file)
    destination_file = open(PROPERTIES_FILE, 'r+')
    destination_data = json.load(destination_file)

    for accounts in source_data:
        for entity in source_data[accounts]:
            encrypted_value = encrypt(key, source_data[accounts][entity])
            destination_data[accounts][entity] = base64.b64encode(encrypted_value)

    destination_file.seek(0)
    destination_file.write(json.dumps(destination_data, indent=4))
    destination_file.truncate()
    source_file.close()
    destination_file.close()


if __name__ == '__main__':
    key = getpass.getpass("Enter the passphrase: ")
    update_login_details(key)
