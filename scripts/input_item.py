#!/usr/bin/env python3

import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import names
import random
import secrets
from lib.config import config
from lib.db_manager import db_manager_no_lock
from lib.db_manager import db_create_constants as CREATE_CONSTANTS

manager = db_manager_no_lock.DatabaseManager(config.get_value(config.DB_NAME))
manager.create_all_tables()

try:
    while True:
        seller_email = input('Seller email: ')
        seller_exists = (manager.has_rows('SELLER', '*', " email = '{}' ".format(seller_email)) > 0)

        if not seller_exists:
            address = input('Address: ')
            phone_number = input('Phone number: ')
            print('Creating seller...')
            manager.insert_seller(seller_email, address, phone_number)
            print('There is now a seller!')

        quantity = input('Quantity: ')
        price = input('Price: ')
        item_name = input('Item name: ')
        item_type = input('Item type: ')
        print('Creating item listing...')
        manager.insert_item(seller_email, quantity, price, item_name, item_type)
        print('Item listing has been created!')
except KeyboardInterrupt:
    print('\nBye!')
