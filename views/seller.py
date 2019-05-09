import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
import http
from lib.security import security
from lib.config import config
from lib.db_manager import db_manager
SELLER_VIEWS = flask.Blueprint('seller_views', __name__)

manager = db_manager.DatabaseManager(config.get_value(config.DB_NAME))

@SELLER_VIEWS.route('/sell_items')
@security.login_required(seller_required=True)
def cart():
    return flask.render_template('sell_items.html',
                                 is_logged_in=security.is_logged_in(seller_required=True),
                                 username=flask.session.get('username'))


@SELLER_VIEWS.route('/upload_image/<seller_email>/<int:item_id>', methods=['POST'])
@security.login_required(seller_required=True)
def upload_image(seller_email: str, item_id: int):
    try:
        filename: str = flask.request.files.get('image').filename
        extension: str = filename[filename.rfind('.'):]
        partial_path: str = f'amazonsharp/web/public/item_images/{seller_email}_{item_id}{extension}' 
        with open(os.path.join(__ROOT_PATH, partial_path), 'wb') as file_handler:
            file_handler.write(flask.request.files.get('image').read())
    except(TypeError, AttributeError):
        return '', http.HTTPStatus.BAD_REQUEST
    return '', http.HTTPStatus.NO_CONTENT


@SELLER_VIEWS.route('/add_item/<seller_email>', methods=['POST'])
@security.login_required(seller_required=True)
def add_item(seller_email: str):
    try:
        name: str = flask.request.form.get('name')
        quantity: int = int(flask.request.form.get('quantity'))
        price: float = float(flask.request.form.get('price'))
        item_type: str = flask.request.form.get('itemType') 
        itemId: int = manager.insert_item(seller_email, quantity, price, name, item_type)
    except(TypeError, AttributeError):
        return '', http.HTTPStatus.BAD_REQUEST
    return flask.jsonify(itemId)


@SELLER_VIEWS.route('/update_item/<seller_email>/<int:item_id>', methods=['POST'])
@security.login_required(seller_required=True)
def update_item(seller_email: str, item_id: int):
    try: 
        name: str = flask.request.form.get('name')
        quantity: int = int(flask.request.form.get('quantity'))
        price: float = float(flask.request.form.get('price'))
        manager.update_item(seller_email, item_id, name, quantity, price)
    except(TypeError, AttributeError):
        return '', http.HTTPStatus.BAD_REQUEST
    return '', http.client.NO_CONTENT


@SELLER_VIEWS.route('/delete_item/<seller_email>/<int:item_id>', methods=['POST'])
@security.login_required(seller_required=True)
def delete_item(seller_email: str, item_id: int):
    try:
        manager.delete_item(seller_email, item_id)
        # Foreign key on delete will take care of inventory's entry 
    except(TypeError, AttributeError):
        return '', http.HTTPStatus.BAD_REQUEST
    return '', http.client.NO_CONTENT


@SELLER_VIEWS.route('/get_item_id/<seller_email>', methods=['POST'])
@security.login_required(seller_required=True)
def max_item_id(seller_email: str):
    return flask.jsonify(manager.retrieve_max_item_id_by_seller(seller_email))