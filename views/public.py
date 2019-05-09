import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
from lib.security import auth_manager, security

PUBLIC_VIEWS = flask.Blueprint('public_views', __name__)


@PUBLIC_VIEWS.route('/')
@PUBLIC_VIEWS.route('/home')
def home():
    username: str = flask.session.get('username') or ''
    return flask.render_template('home.html', is_logged_in=security.is_logged_in(),
                                 is_customer=auth_manager.is_customer(username))

@PUBLIC_VIEWS.route('/all_items')
def items():
    username: str = flask.session.get('username') or ''
    return flask.render_template('all_items.html', is_logged_in=security.is_logged_in(),
                                 is_customer=auth_manager.is_customer(username))


@PUBLIC_VIEWS.route('/sellers')
def sellers():
    username: str = flask.session.get('username') or ''
    return flask.render_template('sellers.html', is_logged_in=security.is_logged_in(),
                                 is_customer=auth_manager.is_customer(username),
                                 is_seller=auth_manager.is_seller(username))


@PUBLIC_VIEWS.route('/seller/<seller_email>')
def seller(seller_email: str):
    username: str = flask.session.get('username') or ''
    return flask.render_template('seller_items.html', is_logged_in=security.is_logged_in(),
                                 username=username,
                                 is_customer=auth_manager.is_customer(username))
