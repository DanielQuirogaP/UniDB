from stdiomask import getpass
from lib.database import Database
from lib.user import is_root_found, create_root, check_user
from lib.read_data import get_databases_names, get_index
from lib.document import Document
from lib.collection import Collection
from lib.doc_query import *
import re
import json
import os

database = None
collection = None
document = None
query_list = []
collection_index = []


def query(command):
    if command.startswith("coll"):
        global query_list
        query_list = command.split(".")
        try:
            global database, collection
            q = process_command(query_list[0])
            collection = Collection(q[1], database.enc_name, database.collection_index)
            process_collection(1)
        except Exception as e:
            print("\nCommand db." + command + " is not valid.\n")
            print(str(e))
    else:
        print("\nCommand db." + command + " is not valid.\n")
    return


def process_document(i):
    global collection, document
    try:
        global database
        q = process_command(query_list[i])
        if q[0] == "coll":
            collection = Collection(q[1], database.enc_name,  database.collection_index, parent=document.parents + [document.name])
            process_collection(i + 1)
        elif q[0] == "get":
            document.get()

        elif q[0] == "update":
            document.update(q[1])
            database.collection_index = collection.get_collection_index()
        elif q[0] == "put":
            document.put(q[1])
            database.collection_index = collection.get_collection_index()
        elif q[0] == "delete":
            document.delete()
        else:
            print("\nThe command \'" + q[0] + "\' is not valid\n")
    except Exception as e:
        print("\nThe command is not valid exception : " + e + "\n")


def process_collection(i):
    global document
    try:
        q = process_command(query_list[i])
        if q[0] == "doc":
            global database, collection
            document = Document(q[1], database.enc_name, database.collection_index, parent=collection.parents + [collection.name])
            process_document(i + 1)

        elif q[0] == "getDocs":
            collection.getDocs()
        elif q[0] == "put":
            collection.put(q[1])
            database.collection_index = collection.get_collection_index()
        else:
            print("\nThe command \'" + q[0] + "\' is not valid\n")
    except Exception as e:
        print("\nThe command is not valid exception : " + str(e) + "\n")


def process_command(command):
    i = command.index("(")
    command_type = command[:i]
    command_arg = command[i:]

    if command_arg == "()":
        return [command_type]

    if re.findall("^\([\'\"]", command_arg) and re.findall("[\'\"]\)$", command_arg):
        command_arg = command_arg[2:-2]
        if re.findall("^[a-zA-Z_][a-zA-Z0-9_]+$", command_arg):
            return [command_type, command_arg]
        else:
            raise Exception("not valid")

    if re.findall("^\(\{", command_arg) and re.findall("\}\)$", command_arg):
        command_arg = json.loads(command_arg[1:-1])
        return [command_type, command_arg]

    else:
        raise Exception("not valid")


def user_init():
    if is_root_found():
        password = getpass("Password: ")
        while not check_user("root", password):
            password = getpass("Invalid password, please try again: ")

    else:
        new_password = getpass("Enter new password: ")
        confirm = getpass("Please confirm the password: ")
        while new_password != confirm:
            print("\nPasswords don't match.\n")
            new_password = getpass("Please insert new password: ")
            confirm = getpass("Confirm the password: ")
        create_root(new_password)
    return


if __name__ == '__main__':
    print("\n=================================UniDB=================================\n")
    newPath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(newPath)
    database_index = get_index()
    print("User: root")
    user_init()
    print()
    while True:
        command = input("> ")
        if command == "exit":
            break
        elif command.startswith("use "):

            command = command.split(" ")
            if len(command) > 2:
                print("\nCommand " + command.join(" ") + " is invalid.\n")
            else:
                if command[1] == "":
                    print("\nCommand " + command.join(" ") + " is invalid.\n")
                else:
                    database = Database(command[1], database_index)
                    collection_index = database.collection_index

        elif command.startswith("db."):
            if database != None:
                query(command[3:])
            else:
                print("\nThere's not selected database\n")
        else:
            print("\nThe command \"" + command + "\" doesn't exist\n")
