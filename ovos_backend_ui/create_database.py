#!/usr/bin/env python3
from sys import argv
import os

from configuration import DEFAULT_DATABASE_NAME

from json_database import JsonDatabaseXDG

def show_intro(db_name=None):
    os.system('cls||clear')
    print()
    print("do some ascii art here")
    print()
    print(f"Using DB {db_name or DEFAULT_DATABASE_NAME}")
    print()

def parse_db_name(list_of_strings):
    return "_".join(list_of_strings)

def check_for_admin(db):
    return db.search_by_key("admin")

def admin_login(db):
    username = str(input("Admin Username: "))
    for user in check_for_admin(db):
        print(user)
        if user["users"][username]["admin"]
        if user["admin"]["id"] == username:
            password = str(input(f"{username} Password: "))
            if user["admin"]["password"] == password:
                return True
        return False


if __name__ == "__main__":
    db_name = DEFAULT_DATABASE_NAME
    if len(argv) > 1:
        db_name = parse_db_name(argv[1:])

    db = JsonDatabaseXDG(db_name)
    admin_users = check_for_admin(db)
    print(len(admin_users))
    if len(admin_users) == 0:
        print()
        print("We need to create an admin account")
        user_name = str(input("Admin User Name: "))
        password = str(input(f"Password for {user_name}: "))
        user = {"id": user_name, "password": password}
        db.add_item({"admin": user})
        db.commit()
    else:
        print(admin_login(db))

#         db = JsonDatabaseXDG(argv[1])
#     else:
#         db = JsonDatabaseXDG("backend_users")
#

