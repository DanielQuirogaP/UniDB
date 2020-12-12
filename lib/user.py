from .read_data import get_root_encrypted_password
from .hash_lib import hash_password
from .write_data import create_root_register


def check_user(name, password):
    password = hash_password(password)
    user_password = get_root_encrypted_password()
    return user_password == password


def is_root_found():
    user_password = get_root_encrypted_password()
    return user_password != None


def create_root(password):
    password = hash_password(password)
    create_root_register(password)
