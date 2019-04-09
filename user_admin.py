from app import app, db
from app.models import User
#from app.models import AppData

import argparse
import random
import string

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def binary_true_false(boolValue):
    if boolValue:
        return 1
    else:
        return 0

#add a new user with a password and email address
def add_user(username, email, password):

    user = User(username=username, email=email)
    db.session.add(user)
    user.set_password(password)
    db.session.commit()

#reset the password
def set_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        user.set_password(password)
        db.session.commit()
    else:
        raise ValueError("User not Found")

#authorise a user to login
def auth_user(username, authorised=True):
    user = User.query.filter_by(username=username).first()
    if user:
        user.isAuth = binary_true_false(authorised)
        db.session.commit()
    else:
        raise ValueError("User not Found")

#Set a user to Super-User privs
def super_user(username, super=True):
    user = User.query.filter_by(username=username).first()
    if user:
        user.isSuper = binary_true_false(super)
        db.session.commit()
    else:
        raise ValueError("User not Found")

#Set a user to have admin privs
def admin_user(username, admin=True):
    user = User.query.filter_by(username=username).first()
    if user:
        user.isAdmin = binary_true_false(admin)
        db.session.commit()
    else:
        raise ValueError("User not Found")


if __name__ == '__main__':
    #args [-a | -p | -s ] -u <username> [ -e <email> ]
    parser = argparse.ArgumentParser(description="Create new users and set password to random string.  "
                                                 "Generates a random password and prints this out to terminal."
                                    , formatter_class = argparse.RawTextHelpFormatter)
    parser_group = parser.add_mutually_exclusive_group(required=True)
    parser_group.add_argument('-a', action='store_true', help='Add a new user')
    parser_group.add_argument('-p', action='store_true', help='Reset password for a user')
    parser_group.add_argument('-s', action='store_true', help='Set privilege for a user')
    parser.add_argument('-u', dest="username", action='store', help='username', required=True)
    parser.add_argument('-e', dest="email", action='store', help='email', required=False)

    admin_group = parser.add_mutually_exclusive_group(required=False)
    admin_group.add_argument('-isadmin', dest="isadmin", action='store_true', help='Add admin priv', required=False)
    admin_group.add_argument('-notadmin', dest="notadmin", action='store_true', help='Remove admin priv', required=False)

    auth_group = parser.add_mutually_exclusive_group(required=False)
    auth_group.add_argument('-isauth', dest="isauth", action='store_true', help='Authorised to login', required=False)
    auth_group.add_argument('-notauth', dest="notauth", action='store_true', help='Not Authorised to login', required=False)

    super_group = parser.add_mutually_exclusive_group(required=False)
    super_group.add_argument('-issuper', dest="issuper", action='store_true', help='Is Super User', required=False)
    super_group.add_argument('-notsuper', dest="notsuper", action='store_true', help='Not Super User', required=False)


    args = vars(parser.parse_args())

    username = args["username"]

    if args["a"] and not args["email"]:
        print("Error: must provide email address when adding a new user")
        exit(1)
    else:
        email = args["email"]

    password = randomString(8)


    if args["a"]:
        #add user
        add_user(username, email, password)
        print("User created")
        print("Password set to ", password)
    elif args["p"]:
        #set password to random string
        set_password(username, password)
        print("Password reset")
        print("Password set to ", password)
    elif args["s"]:
        #set a user attribute
        if args["isadmin"]:
            print("Setting Admin User")
            admin_user(username, True)
        elif args["notadmin"]:
            print("Removing Admin User")
            admin_user(username, False)

        elif args["isauth"]:
            print("Authorising User Login")
            auth_user(username, True)
        elif args["notauth"]:
            print("Removing User Login Auth")
            auth_user(username, False)

        elif args["issuper"]:
            print("Setting Super-User")
            super_user(username, True)
        elif args["notsuper"]:
            print("Removing Super-User Auth")
            super_user(username, False)


        else:
            print("unhandled option")
    else:
        print("Unknown option")