import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
from lib.config import config
from lib.db_manager import db_manager
from lib.security import security

PUBLIC_VIEWS = flask.Blueprint('public_views', __name__)
__DATABASE = db_manager.DatabaseManager(config.get_value(config.DB_NAME))                                                            


@PUBLIC_VIEWS.route('/')
@PUBLIC_VIEWS.route('/home')
def home():
    return flask.render_template('home.html', is_logged_in=security.is_logged_in())

@PUBLIC_VIEWS.route('/items')
def items():
    return flask.render_template('items.html', is_logged_in=security.is_logged_in(), items=__DATABASE.retrieve_all_items())
