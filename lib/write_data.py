import json
import os
from .read_data import get_system_properties, get_index
from .hash_lib import update_index

def create_root_register(password):
    properties_dict = get_system_properties()
    properties_dict['password'] = password
    with open("properties.uni", "w") as properties:
        json.dump(properties_dict, properties)


def register_database(name):
    properties_dict = get_system_properties()
    properties_dict['databases'].append(name)
    with open("properties.uni", "w") as properties:
        json.dump(properties_dict,properties)


def write_index(name, dir='indexes.uindx', encrypt=False):
    table = get_index(dir)
    updated_table = update_index(name, table, encrypt)
    to_text = []
    for line in updated_table:
        to_text.append(' '.join(line))
    to_text = '\n'.join(to_text)
    with open(dir, 'w') as index:
        index.write(to_text)
    return updated_table
