import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
from lib.security import security

SELLER_VIEWS = flask.Blueprint('seller_views', __name__)


@SELLER_VIEWS.route('/sell_items')
@security.login_required(seller_required=True)
def cart():
    return flask.render_template('sell_items.html', is_logged_in=security.is_logged_in())
