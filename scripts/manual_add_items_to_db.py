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

# manager = db_manager_no_lock.DatabaseManager(config.get_value(config.DB_NAME))

def print_table(table_name: str):
    manager.get_cursor().execute(
        """
        SELECT * 
        FROM {}
        """
        .format(table_name)
    )
    results = manager.get_cursor().fetchall()
    print(table_name)
    for row in results:
        print(row)
    print()

manager = db_manager_no_lock.DatabaseManager(':memory:')

manager.create_all_tables()

manager.insert_login_info('login_info@email.com', 'a'*77, 'ADMIN')

# Create a customer and user, give them a shopping_cart, and link them together in has_a_shopping_cart
manager.insert_customer('customer@email.com', 'West Apartment A', '1234567890')
manager.insert_customer('pchan@email.com', 'Mendy', '0987654321')
manager.delete('CUSTOMER', " email = '{}' ".format('customer@email.com'))
# Create a seller and user
manager.insert_seller('stevejobs@apple.com', 'Somewhere in California', '6316323333')
# Create an item and put it in the inventory table
manager.insert_item('stevejobs@apple.com', 5, 1000, 'iPhone 3GS', 'Electronics')
manager.insert_item('stevejobs@apple.com', 3, 200, 'iPhone 1G', 'Electronics')
# Customer adds some item into shopping cart
manager.insert_items_in_shopping_cart('customer@email.com', 'stevejobs@apple.com', 1, 2)
manager.insert_items_in_shopping_cart('customer@email.com', 'stevejobs@apple.com', 2, 2)
manager.insert_items_in_shopping_cart('pchan@email.com', 'stevejobs@apple.com', 2, 1)
manager.insert_items_in_shopping_cart('pchan@email.com', 'stevejobs@apple.com', 1, 1)
# print_table('ITEMS_IN_SHOPPING_CART')
# print_table('ORDERS')
# # Customer makes an order, buying only 2 items
# manager.insert_order('customer@email.com')
# # manager.insert_order('pchan@email.com')

# # print_table('CUSTOMER')
# # print_table('SELLER')
# # print_table('ITEM')
# # print_table('INVENTORY')
# # print_table('ORDERS')
# print_table('ITEMS_IN_SHOPPING_CART')
# print_table('SHOPPING_CART')