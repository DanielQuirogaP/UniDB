from lib.database import Database


def query(command):
    if command.startswith("collection"):
        print()
    elif command.startswith("document"):
        print()
    elif command.startswith("get"):
        process_get()
    elif command.startswith("put"):
        process_put()
    elif command.startswith("delete"):
        process_delete()
    return


def process_get():
    pass


def process_put():
    pass


def process_delete():
    pass


if __name__ == '__main__':
    print("UniDB: The best DataBase engine you'll ever see in your life.")
    print("User: root")
    password = input("Password: ")

    db = Database()
    while True:
        command = input("> ")
        if command == "exit":
            break
        elif command.startswith("use "):
            print()
        elif command.startswith("db."):
            if Database.initialized:
                query(command[3:])
            else:
                print("\nThere's not selected database\n")
