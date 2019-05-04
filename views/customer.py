import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
from lib.security import security

CUSTOMER_VIEWS = flask.Blueprint('customer_views', __name__)


@CUSTOMER_VIEWS.route('/cart')
@security.login_required(customer_required=True)
def cart():
    return flask.render_template('cart.html',
                                 is_logged_in=security.is_logged_in(customer_required=True))
