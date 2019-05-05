import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
import http;
from lib.security import security

SELLER_VIEWS = flask.Blueprint('seller_views', __name__)


@SELLER_VIEWS.route('/sell_items')
@security.login_required(seller_required=True)
def cart():
    return flask.render_template('sell_items.html',
                                 is_logged_in=security.is_logged_in(seller_required=True))


@SELLER_VIEWS.route('/upload_image/<seller_email>/<int:item_id>', methods=['POST'])
@security.login_required(seller_required=True)
def upload_image(seller_email, item_id):
    filename: str = flask.request.files.get('image').filename
    extension: str = filename[filename.rfind('.'):]
    partial_path: str = f'amazonsharp/web/public/item_images/{seller_email}_{item_id}{extension}' 
    with open(os.path.join(__ROOT_PATH, partial_path), 'wb') as file_handler:
        file_handler.write(flask.request.files.get('image').read())
    return '', http.client.NO_CONTENT
