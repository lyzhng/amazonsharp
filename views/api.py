import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import flask
import os
from lib.config import config
from lib.db_manager import db_manager

API_VIEWS = flask.Blueprint('api_views', __name__)
__DATABASE = db_manager.DatabaseManager(config.get_value(config.DB_NAME))                                                            


@API_VIEWS.route('/get_all_items')
def all_items():
    items = __DATABASE.retrieve_all_items()
    return flask.jsonify(items)


@API_VIEWS.route('/get_popular_items/<int:n>')
def popular_items(n):
    items = __DATABASE.retrieve_popular_items(n)
    return flask.jsonify(items)


@API_VIEWS.route('/get_sellers')
def all_sellers():
    sellers = __DATABASE.retrieve_sellers()
    return flask.jsonify(sellers)


@API_VIEWS.route('/get_items/<seller>')
def items_by_seller(seller):
    items_by_seller = __DATABASE.retrieve_items_by_seller(seller)
    return flask.jsonify(items_by_seller)


@API_VIEWS.route('/get_items/<seller>/<int:item>')
def item_by_seller(seller, item):
    particular_item = __DATABASE.retrieve_item_info(seller, item)
    return flask.jsonify(particular_item)


@API_VIEWS.route('/get_image/<seller>/<item_id>')
def image_by_seller(seller, item_id):
    image_path: str = os.path.join(__ROOT_PATH, 'amazonsharp/web/public/item_images')
    images = [image for image in os.listdir(image_path)
              if os.path.basename(image).startswith(f'{seller}_{item_id}.')]
    if len(images) > 0:
        image = images[0]
        return flask.send_from_directory(image_path, os.path.basename(image))
