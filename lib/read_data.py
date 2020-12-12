import json


def get_system_properties():
    with open("properties.uni", "r") as properties:
        properties_dict = json.load(properties)
    return properties_dict


def get_root_encrypted_password():
    properties = get_system_properties()
    return properties['password']


def get_databases_names():
    properties = get_system_properties()
    return properties['databases']


def get_index(dir='indexes.uindx'):
    with open(dir, 'r') as index:
        lines = index.readlines()
    lines = ''.join(lines)
    lines = lines.split('\n')
    index = []
    for line in lines:
        index.append(line.split(' '))
    while len(index) < 311:
        index.append([''])
    return index
