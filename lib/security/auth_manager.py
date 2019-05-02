import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)


from typing import Tuple
from lib.config import config
from lib.db_manager import db_manager
from lib.db_manager import db_create_constants
from lib.security import security_utils
import passlib.hash

__AUTH_MANAGER = db_manager.DatabaseManager(config.get_value(config.DB_NAME))
__AUTH_MANAGER.create_table(db_create_constants.LOGIN_INFO)


def is_registered(username: str) -> bool:
    "Check if user with username, username, is registered."
    return __AUTH_MANAGER.has_rows('login_info', '*',
                                   ' email = "{}" '.format(username))


def is_seller(username: str) -> bool:
    "Check if user is a seller."
    cond: str = ' email = "{}" AND role = "SELLER" '.format(username)
    return __AUTH_MANAGER.has_rows('login_info', '*', cond)


def is_admin(username: str) -> bool:
    "Check if user is an admin."
    cond: str = ' email = "{}" AND role = "ADMIN" '.format(username)
    return __AUTH_MANAGER.has_rows('login_info', '*', cond)


def is_developer(username: str) -> bool:
    "Check if user is a developer."
    cond: str = ' email = "{}" AND role = "DEVELOPER" '.format(username)
    return __AUTH_MANAGER.has_rows('login_info', '*', cond)


def register(username: str, password: str, role: str) -> Tuple[bool, str]:
    "Add the user to the database."
    if is_registered(username):
        return False, 'Username already exists!'
    hashed_password: str = security_utils.secure_hash_password(password)
    __AUTH_MANAGER.insert('login_info', username, hashed_password, role)
    return True, 'Successfully registered!'


def login(username: str, password: str) -> Tuple[bool, str]:
    "Check if the credentials are correct."
    if not is_registered(username):
        return False, 'The username and/or password is invalid.'

    user_info_cond: str = ' email = "{}" '.format(username)
    user_info = __AUTH_MANAGER.retrieve_rows('login_info', '*', user_info_cond)

    if passlib.hash.argon2.verify(password, user_info[0][1]):
        return True, 'Successfully logged in!'
    return False, 'The username and/or password is invalid.'


def drop_user(username: str):
    if not is_registered(username):
        return False, 'User does not exists!'
    __AUTH_MANAGER.delete('login_info', ' email = "{}" ')
