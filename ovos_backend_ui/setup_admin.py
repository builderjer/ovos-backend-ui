"""This creates an admin user for the OVOS backend UI

Right now, that is all it does.  Next versions will
do more towards command line user management.
"""

from sys import exit
from getpass import getpass
from users import User
from exceptions import DuplicateUserError

def start():
    print("Create a User")
    print()
    user_id = input("User ID: ")
    pwd1 = getpass(f"Password for user {user_id}: ")
    pwd2 = getpass("Reenter Password: ")
    if pwd1 != pwd2:
        print()
        print("Passwords do not match")
        print()
        start()
    else:
        try:
            User.create_new_user(user_id, pwd1, admin=True)
            print()
            print(f"Admin {user_id} has been created")
        except:
            DuplicateUserError
            print(f"User {user_id} already exists")
            start()

if __name__ == "__main__":
    start()
