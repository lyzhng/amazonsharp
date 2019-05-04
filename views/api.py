import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
from lib.config import config
from lib.db_manager import db_manager

API_VIEWS = flask.Blueprint('api_views', __name__)
__DATABASE = db_manager.DatabaseManager(config.get_value(config.DB_NAME))                                                            


@API_VIEWS.route('/get_all_items')
def all_items():
    return flask.jsonify(__DATABASE.retrieve_all_items())
