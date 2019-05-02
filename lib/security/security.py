import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)


import flask
import functools
from lib.security import auth_manager
from lib.security import security_utils

SECURITY = flask.Blueprint('security', __name__)


def login_required(seller_required: bool = False, admin_required: bool = False,
                   developer_required: bool = False):
    "Enforce that the user has the appropriate permissions to access the page."
    def actual_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            flask.session['next'] = flask.request.url

            if is_logged_in(seller_required, admin_required,
                            developer_required):
                return function(*args, **kwargs)
            return flask.redirect(flask.url_for('security.login_form'))
        return wrapper
    return actual_decorator


def is_logged_in(seller_required: bool = False, admin_required: bool = False,
                 developer_required: bool = False) -> bool:
    "Check if the user is loggged in with appropriate permissions or not."
    username = flask.session.get('username')

    if not username:
        return False
    if auth_manager.is_developer(username):
        return True
    if admin_required and auth_manager.is_admin(username):
        return True
    if seller_required and auth_manager.is_seller(username):
        return True
    if not (seller_required or admin_required or developer_required) and \
       auth_manager.is_registered(username):
        return True

    flask.session.pop('username')
    return False


@SECURITY.route('/register')
def register_form():
    if is_logged_in():
        return flask.redirect(flask.url_for('public_views.home'))
    return flask.render_template('register.html')


@SECURITY.route('/register', methods=['POST'])
def register():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    results = auth_manager.register(username, password, 'CUSTOMER')
    flask.flash(results[1])

    if results[0]:
        return flask.redirect(flask.url_for('security.login_form'))
    return flask.redirect(flask.url_for('security.register_form'))


@SECURITY.route('/login')
def login_form():
    if is_logged_in():
        return flask.redirect(flask.url_for('public_views.home'))
    return flask.render_template('login.html')


@SECURITY.route('/login', methods=['POST'])
def login():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    results = auth_manager.login(username, password)
    if results[0]:
        flask.session['username'] = username
        return security_utils.redirect_back()
    flask.flash(results[1])
    return flask.redirect(flask.url_for('security.login_form'))


@SECURITY.route('/logout/')
def logout():
    if is_logged_in():
        flask.session.pop('username')

    if 'next' in flask.session:
        flask.session.pop('next')

    return flask.redirect(flask.url_for('public_views.home'))
