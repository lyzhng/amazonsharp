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
trailing_address = ['Street', 'Road', 'City']

# tables
manager.create_table(CREATE_CONSTANTS.USER) # how will i get first_name and second_name? front-end
manager.create_table(CREATE_CONSTANTS.SELLER) # works
manager.create_table(CREATE_CONSTANTS.CUSTOMER) # works
manager.create_table(CREATE_CONSTANTS.EMPLOYEE) # works

manager.create_table(CREATE_CONSTANTS.ITEM) # works
manager.create_table(CREATE_CONSTANTS.INVENTORY) 
manager.create_table(CREATE_CONSTANTS.SHOPPING_CART) # works
manager.create_table(CREATE_CONSTANTS.HAS_SHOPPING_CART) # works
manager.create_table(CREATE_CONSTANTS.ORDERS) # works
manager.create_table(CREATE_CONSTANTS.ORDER_PLACED) 
manager.create_table(CREATE_CONSTANTS.ITEMS_BOUGHT) 
manager.create_table(CREATE_CONSTANTS.ITEM_FREQUENCY)
manager.create_table(CREATE_CONSTANTS.ITEMS_IN_SHOPPING_CART)

customers = []
customers_cart_map = {}
sellers = []
employees = []
employee_roles = ['ADMIN', 'VIP', 'MANAGER', 'EMPLOYEE']
items = []
orders = []
carts = []

# put 5 customers in db
for i in range(5):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = first_name + '.' + last_name + '@email.com'
    address = str(random.randint(1, 999)) + ' ' + random.choice(trailing_address)
    phone_number = random.randint(1e9, 9e9)
    manager.insert('CUSTOMER', email, address, phone_number)
    customers.append(email)

# put 5 sellers in db
for i in range(5):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = first_name + '.' + last_name + '@email.com'
    address = str(random.randint(1, 999)) + ' ' + random.choice(trailing_address)
    phone_number = random.randint(1e9, 9e9)
    manager.insert('SELLER', email, address, phone_number)
    sellers.append(email)

# for i in range(5):
#     first_name = names.get_first_name()
#     last_name = names.get_last_name()
#     email = first_name + '.' + last_name + '@email.com'
#     role = random.choice(employee_roles)
#     date_joined = str(random.randint(2000, 2050)) + '-' + str(random.randint(1, 12)) + '-' + str(random.randint(1, 30))
#     phone_number = random.randint(1e9, 9e9)
#     manager.insert('EMPLOYEE', email, role, date_joined, phone_number)
#     employees.append(email)

item_sellers = []
for i in range(5):
    seller = random.choice(sellers)
    item_id = i
    price = random.randint(1, 10)
    name = 'ITEM: ' + 'name' + str(i)
    item_type = 'ITEM_TYPE: ' + 'type' + str(i)
    manager.insert('ITEM', seller, item_id, 100, price, name, item_type)
    items.append(item_id)
    item_sellers.append(seller)

for i in range(5):
    order_no = random.randint(1, 1e5)
    total_number_of_items = random.randint(1, len(items) - 1)
    date_ordered = str(random.randint(2000, 2050)) + '-' + str(random.randint(1, 12)) + '-' + str(random.randint(1, 30))
    manager.insert('ORDERS', order_no, customers[i], total_number_of_items, date_ordered)
    orders.append(order_no)

for i in range(len(orders)):
    item_seller = item_sellers[i]
    max_id = manager.retrieve_max_item_id_by_seller(item_seller)
    item = random.randint(1, max_id)
    price = random.randint(1, 50)
    name = 'item_name: {}{}'.format('name', str(i))
    item_type = 'item_type: {}{}'.format('type', str(i))
    number_of_items_bought = 5
    manager.insert('ITEMS_BOUGHT', item_seller, item, i+1, price, name, item_type, number_of_items_bought)
