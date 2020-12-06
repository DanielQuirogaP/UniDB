import json


def encrypt_password(password):
    return None


def check_user(name, password):
    password = encrypt_password(password)
    with open("properties.uni", "r") as properties:
        properties_dict = json.load(properties)
        user_password = properties_dict['password']
    return user_password == password


d = check_user("", "")


print(d)
