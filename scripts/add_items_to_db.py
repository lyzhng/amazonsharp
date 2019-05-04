#/usr/bin/env python3

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
from lib.db_manager import db_manager
from lib.db_manager import db_create_constants as CREATE_CONSTANTS

manager = db_manager.DatabaseManager(config.get_value(config.DB_NAME))
trailing_address = ['Street', 'Road', 'City']

# tables
manager.create_table(CREATE_CONSTANTS.USER) # how will i get first_name and second_name? front-end
manager.create_table(CREATE_CONSTANTS.SELLER) # works
manager.create_table(CREATE_CONSTANTS.CUSTOMER) # works
manager.create_table(CREATE_CONSTANTS.EMPLOYEE) # works

manager.create_table(CREATE_CONSTANTS.ITEM) # works
manager.create_table(CREATE_CONSTANTS.HAS_SHOPPING_CART) # works
manager.create_table(CREATE_CONSTANTS.ORDERS) # works
manager.create_table(CREATE_CONSTANTS.ORDER_PLACED) #
manager.create_table(CREATE_CONSTANTS.ITEMS_BOUGHT)
manager.create_table(CREATE_CONSTANTS.SHOPPING_CART)
manager.create_table(CREATE_CONSTANTS.ITEM_FREQUENCY) #
manager.create_table(CREATE_CONSTANTS.ITEMS_IN_SHOPPING_CART)


# triggers
manager.create_trigger(CREATE_CONSTANTS.INCREMENT_FREQUENCY_TRIGGER)
manager.create_trigger(CREATE_CONSTANTS.DECREMENT_QUANTITY_TRIGGER)

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
    address = str(random.randint(1, 999)) + random.choice(trailing_address)
    phone_number = random.randint(1e9, 9e9)
    manager.insert('CUSTOMER', email, address, phone_number)
    customers.append(email)

# put 5 sellers in db
for i in range(5):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = first_name + '.' + last_name + '@email.com'
    address = str(random.randint(1, 999)) + random.choice(trailing_address)
    phone_number = random.randint(1e9, 9e9)
    manager.insert('SELLER', email, address, phone_number)
    sellers.append(email)

# put 5 employees in db
# FIXME: login_info.role & employee.role do not get along
for i in range(5):
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email = first_name + '.' + last_name + '@email.com'
    role = random.choice(employee_roles)
    date_joined = str(random.randint(2000, 2050)) + '-' + str(random.randint(1, 12)) + '-' + str(random.randint(1, 30))
    phone_number = random.randint(1e9, 9e9)
    manager.insert('EMPLOYEE', email, role, date_joined, phone_number)
    employees.append(email)

# put 5 items in db
for i in range(5):
    seller = random.choice(sellers)
    item_id = random.randint(1, 5000)
    price = random.randint(1, 10)
    name = 'ITEM: ' + 'name' + str(i)
    item_type = 'ITEM_TYPE: ' + 'type' + str(i)
    manager.insert('ITEM', seller, item_id, 5, price, name, item_type)
    items.append(item_id)

for row in manager.retrieve_popular_items():
    print(row)


# 5 customers have a shopping cart FIXME
for customer in customers:
    cart_id = random.randint(1000, 1e5)
    manager.insert('HAS_SHOPPING_CART', customer, cart_id)
    carts.append(cart_id)

for i in range(5):
    order_no = random.randint(1, 1e5)
    total_number_of_items = random.randint(1, len(items) - 1)
    date_ordered = str(random.randint(2000, 2050)) + '-' + str(random.randint(1, 12)) + '-' + str(random.randint(1, 30))
    manager.insert('ORDERS', order_no, total_number_of_items, date_ordered)
    orders.append(order_no)

# items_bought = {}
# for order in orders:
#     item = random.choice(items)
#     items_bought[order] = item
#     seller = random.choice(sellers)
#     price = random.randint(1, 50)
#     name = 'item_name: ' + str(item) + str(random.randint(1, 100))
#     item_type = 'item_type: ' + str(item) + str(random.randint(1, 100))
#     number_of_items_bought = 3
#     manager.insert('ITEMS_BOUGHT', seller, item, order, price, name, item_type, number_of_items_bought)
#     manager.insert('ITEM_FREQUENCY', seller)

# print(manager.retrieve_popular_items())
for row in manager.retrieve_all_items():
    print(row)

# for row in manager.retrieve_popular_items():
#     print(row)
