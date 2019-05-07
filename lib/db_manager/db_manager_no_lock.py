import os
import sys

__DIR_PATH = os.path.dirname(os.path.realpath(__file__))
__ROOT_PATH = os.path.normpath(os.path.join(__DIR_PATH, '../..'))
if __ROOT_PATH not in sys.path:
    sys.path.append(__ROOT_PATH)

import sqlite3
from typing import List
from datetime import datetime
from lib.db_manager import db_create_constants as CREATE_CONSTANTS


class DatabaseManager:

    """ Constructor for DatabaseManager """
    def __init__(self, filename: str):  
        self.conn = sqlite3.connect(filename, check_same_thread=False) 
        self.cur = self.conn.cursor()
        self.conn.execute('PRAGMA foreign_keys = 1')
        self.create_all_tables()
        self.conn.commit()

    """ General CREATE TABLE function """
    def _create_table(self, create_table_statement: str) -> None:
        self.cur.execute(create_table_statement)
        self.conn.commit()

    """ Create all tables """
    def create_all_tables(self):
        self._create_table(CREATE_CONSTANTS.USER) 
        self._create_table(CREATE_CONSTANTS.SELLER)
        self._create_table(CREATE_CONSTANTS.CUSTOMER)
        self._create_table(CREATE_CONSTANTS.EMPLOYEE) 
        self._create_table(CREATE_CONSTANTS.ITEM)
        self._create_table(CREATE_CONSTANTS.INVENTORY)
        self._create_table(CREATE_CONSTANTS.SHOPPING_CART)
        self._create_table(CREATE_CONSTANTS.HAS_SHOPPING_CART)
        self._create_table(CREATE_CONSTANTS.ITEMS_IN_SHOPPING_CART)
        self._create_table(CREATE_CONSTANTS.ORDERS)
        self._create_table(CREATE_CONSTANTS.ORDER_PLACED) 
        self._create_table(CREATE_CONSTANTS.ITEMS_BOUGHT) 
        self._create_table(CREATE_CONSTANTS.ITEM_FREQUENCY)

    """
    [WARNING]
    General INSERT function. If there is a more specific function that suits your needs, use that one.
    More specific functions include: insert_items_bought, insert_customer, insert_seller, insert_order
    """
    def _insert(self, table_name: str, *values) -> None:
        qmark = ("?," * len(values)).rstrip(",")
        self.cur.execute('INSERT INTO {} VALUES({})'.format(table_name, qmark), values)
        self.conn.commit()

    """ Insert into items_bought when an order is placed """
    def insert_items_bought(self, seller_email: str, item_id: int, price: float, name: str, item_type: str, number_of_items_bought: int): 
        order_number = self._retrieve_max_order_number()
        self.cur.execute(
            """
            INSERT INTO items_bought(seller_email, item_id, order_number, price, name, type, number_of_items_bought)
            VALUES('{}', {}, {}, {}, '{}', '{}', {})
            """
            .format(seller_email, item_id, order_number, price, name, item_type, number_of_items_bought)
        )
        self.conn.commit()
        self._handle_frequency_and_quantity(seller_email, item_id, order_number, price, name, item_type, number_of_items_bought)

    """ General insert user function """
    def _insert_user(self, first: str, last: str, email: str):
        self.cur.execute(
            """
            INSERT INTO user
            VALUES('{}', '{}', '{}')
            """
            .format(first, last, email)
        )
        self.conn.commit()        

    """ Insert customer/user into respective tables """
    def insert_customer(self, email: str, address: str, phone_number: str):
        self._insert_user('', '', email)
        self.cur.execute(
            """
            INSERT INTO customer
            VALUES('{}', '{}', '{}')
            """
            .format(email, address, phone_number)
        )
        self.conn.commit()
        self._insert_shopping_cart(email)

    """ Insert seller/user into respective tables """
    def insert_seller(self, email: str, address: str, phone_number: str):
        self._insert_user('', '', email)
        self.cur.execute(
            """
            INSERT INTO seller
            VALUES('{}', '{}', '{}')
            """
            .format(email, address, phone_number)
        )
        self.conn.commit()

    """ Link customer to (unique) shopping cart """
    def _insert_shopping_cart(self, email: str) -> None:
            current_max = self._retrieve_max_cart_id()
            self._insert('SHOPPING_CART', current_max + 1, 0, 0)
            self._insert('HAS_SHOPPING_CART', email, current_max + 1)  


    """ Insert order into orders table as well as order_placed table """
    def insert_order(self, order_number: int, customer_email: str, total_number_of_items: int) -> None:
        date_ordered = datetime.now().strftime("%B %d, %Y %I:%M%p")
        corresponding_cart_id = self._retrieve_customer_cart_id(customer_email)
        max_order_number = self._retrieve_max_order_number()
        self.cur.execute(
            """
            INSERT INTO orders(order_number, customer_email, total_number_of_items, date_ordered)
            VALUES({}, '{}', {}, '{}')
            """
            .format(max_order_number + 1, customer_email, total_number_of_items, date_ordered)
        )
        self.conn.commit()
        self._insert('ORDER_PLACED', customer_email, corresponding_cart_id, max_order_number + 1)
        self.conn.commit()


    """ Increment item's frequency and decrement item's quantity by number_of_items_bought """
    def _handle_frequency_and_quantity(self, seller_email: str, item_id: int, order_number: int, 
                            price: float, name: str, item_type: str, number_of_items_bought: int) -> None:
        self.cur.execute(
            """
            INSERT INTO item_frequency(seller_email, item_id, frequency)
            VALUES('{}', {}, {})
            ON CONFLICT(seller_email, item_id) 
            DO UPDATE
            SET frequency = frequency + {}
            """
            .format(
                seller_email, item_id, number_of_items_bought,
                number_of_items_bought
            )
        )
        self.conn.commit()
        self.cur.execute(
            """
            UPDATE item
            SET quantity = quantity - {}
            WHERE 
                seller_email = (
                    SELECT seller_email
                    FROM items_bought
                    WHERE
                        item.seller_email = items_bought.seller_email AND
                        item.item_id = items_bought.item_id AND
                        items_bought.order_number = {}
                )
                AND
                item_id = (
                    SELECT item_id
                    FROM items_bought
                    WHERE
                        item.seller_email = items_bought.seller_email AND
                        item.item_id = items_bought.item_id AND
                        items_bought.order_number = {}
                )
            """
            .format(number_of_items_bought, order_number, order_number)
        )
        self.conn.commit()

    
    """ Returns the unique id of the item entry that got inserted """
    def insert_item(self, seller_email: str, quantity: int, price: float, name: str, item_type: str) -> int:
        item_id = self._retrieve_max_item_id_by_seller(seller_email)
        self.cur.execute(
            """
            INSERT OR REPLACE INTO item(seller_email, item_id, quantity, price, name, type)
            VALUES('{}', {}, {}, {}, '{}', '{}')
            """
            .format(seller_email, item_id + 1, quantity, price, name, item_type)
        )
        self.conn.commit()
        self.cur.execute(
            """
            INSERT INTO inventory(seller_email, item_id)
            VALUES('{}', {})
            ON CONFLICT(seller_email, item_id)
            DO NOTHING
            """
            .format(seller_email, item_id + 1)
        )
        self.conn.commit()
        return item_id + 1

    """
    General UPDATE function. If updating an item, use update_item.
    """
    def update(self, table_name: str, modifications: str, filters: str) -> None:
        self.cur.execute('UPDATE {} SET {} WHERE {}'.format(table_name, modifications, filters))
        self.conn.commit()

    def update_item(self, seller_email: str, item_id: int, new_name: str, new_quantity: int, new_price: float) -> None:
        self.cur.execute(
            """
            UPDATE item
            SET name = '{}', quantity = {}, price = {}
            WHERE seller_email = '{}' AND item_id = {}
            """
            .format(
                new_name, new_quantity, new_price,
                seller_email, item_id
            )
        )
        self.conn.commit()

    """ Returns True if table (with selected attributes and filters) has rows """
    def has_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> bool:
        return self.count_rows(table_name, selected_attributes, filters) > 0

    """ Counts how many rows the table (with selected attributes and filters) has """
    def count_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> int:
        return len(self.retrieve_rows(table_name, selected_attributes, filters))

    """ Adds item to customer's shopping cart """
    def add_to_cart(self, customer_email: str, seller_email: str, item_id: int) -> None:
        pass


    """ General SELECT function that returns all rows with requested attributes and filters """
    def retrieve_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> List:
        if filters is None:
            self.cur.execute('SELECT {} FROM {}'.format(selected_attributes, table_name))
        else:
            self.cur.execute('SELECT {} FROM {} WHERE {}'.format(selected_attributes, table_name, filters))
        try:
            return self.cur.fetchall()  
        except sqlite3.OperationalError:
            return []


    """ General SELECT function that returns one row with requested attributes and filters """
    def retrieve_row(self, table_name: str, selected_attributes: str, filters: str = None) -> List:
        if filters is None:
            self.cur.execute('SELECT {} FROM {}'.format(selected_attributes, table_name))
        else:
            self.cur.execute('SELECT {} FROM {} WHERE {}'.format(selected_attributes, table_name, filters))
        try:
            return self.cur.fetchone()  
        except sqlite3.OperationalError:
            return []


    """ 
    Returns a list of the most popular items that are most frequently bought 
    Takes in one parameter, which limits how many will be in the list
    """
    def retrieve_popular_items(self, row_count: int = 0) -> List:
        if row_count == 0:
            row_count = self.count_rows('ITEMS_BOUGHT', '*')
        self.cur.execute(
            """
            SELECT items_bought.name, items_bought.price, item_frequency.frequency
            FROM item_frequency INNER JOIN items_bought
                ON item_frequency.seller_email = items_bought.seller_email 
                AND item_frequency.item_id = items_bought.item_id
            GROUP BY item_frequency.seller_email, item_frequency.item_id
            ORDER BY frequency DESC
            LIMIT {}
            """
            .format(row_count)
        )
        try:
            return self.cur.fetchall()
        except sqlite3.OperationalError:
            return []


    """ Returns a list of all items, whether available or out of stock """
    def retrieve_all_items(self) -> List:
        try:
            return self.retrieve_rows('ITEM', 'name', 'price')
        except sqlite3.OperationalError:
            return []


    """ Returns a list of available items with quantity > 0 """
    def retrieve_available_items(self) -> List:
        try:
            return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity > 0 ')
        except sqlite3.OperationalError:
            return []


    """ Returns a list of out-of-stock items with quantity = 0 """
    def retrieve_out_of_stock_items(self) -> List:
        try:
            return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity = 0')
        except sqlite3.OperationalError:
            return []


    """ Returns a list of sellers """
    def retrieve_sellers(self) -> List:
        try:
            return self.retrieve_rows('SELLER', 'email, address, phone_number')
        except sqlite3.OperationalError:
            return []


    """ Returns a list of items by a particular seller """
    def retrieve_items_by_seller(self, seller_email: str) -> List:
        self.cur.execute(
            """
            SELECT seller_email, item_id, name, price, quantity
            FROM item
            WHERE seller_email = '{}'
            """
            .format(seller_email)
        )
        try:
            return self.cur.fetchall()
        except sqlite3.OperationalError:
            return []


    """ Returns info (name, price, quantity) about an item by a particular seller """
    def retrieve_item_info(self, seller_email: str, item_id: int) -> List:
        self.cur.execute(
            """
            SELECT item.name, item.price, item.quantity
            FROM item
            WHERE item.seller_email = '{}' AND item.item_id = {}
            """
            .format(seller_email, item_id)
        )
        try:
            return self.cur.fetchone()
        except sqlite3.OperationalError:
            return []


    """ Returns a list of all orders made by a customer """
    def retrieve_orders_by_customer(self, customer_email: str) -> List:
        try:
            return self.retrieve_rows('ORDER_PLACED', 'customer_email', " customer_email = '{}' ".format(customer_email))
        except sqlite3.OperationalError:
            return []


    """ Returns a list of items that were in a particular order """
    def retrieve_items_from_order(self, order_number: int) -> List:
        try:
            return self.retrieve_rows('ITEMS_BOUGHT', 'name, number_of_items_bought', ' order_number = {} '.format(order_number))
        except sqlite3.OperationalError:
            return []            
        

    """ [PRIVATE] Returns a cart_id that corresponds to a customer's email """
    def _retrieve_customer_cart_id(self, customer_email: str) -> int:
        self.cur.execute(
            """
            SELECT cart_id
            FROM has_shopping_cart
            WHERE customer_email = '{}'
            LIMIT 1
            """
            .format(customer_email)
        )
        cart_id_entry = self.cur.fetchone()
        return cart_id_entry[0] if cart_id_entry is not None else 0


    """ [PRIVATE] Returns the total number of items from an order """
    def _retrieve_total_number_of_items_from_order(self, order_number:int) -> int:
        self.cur.execute(
            """
            SELECT COUNT(*)
            FROM items_bought
            WHERE order_number = {}
            """
            .format(order_number)
        )
        result = self.cur.fetchone()
        return result[0] if result is not None else 0


    """ [PRIVATE] Returns the current max item id by a seller """
    def _retrieve_max_item_id_by_seller(self, seller_email: str) -> int:
        self.cur.execute(
            """
            SELECT item_id 
            FROM inventory
            WHERE seller_email = '{}'
            ORDER BY item_id DESC
            LIMIT 1
            """
            .format(seller_email)
        )
        current_max = self.cur.fetchone()
        return current_max[0] if current_max is not None else 0


    """ [PRIVATE] Returns the current max order number """
    def _retrieve_max_order_number(self) -> int:
        self.cur.execute(
            """
            SELECT order_number
            FROM orders
            ORDER BY order_number DESC
            LIMIT 1
            """
        )
        max_order_number = self.cur.fetchone()
        return max_order_number[0] if max_order_number is not None else 0


    """ [PRIVATE] Returns the current max cart_id """
    def _retrieve_max_cart_id(self) -> int:
        self.cur.execute(
            """
            SELECT cart_id
            FROM has_shopping_cart
            ORDER BY cart_id DESC
            LIMIT 1
            """
        )
        max_cart_id = self.cur.fetchone()
        return max_cart_id[0] if max_cart_id is not None else 0


    # [TESTING]
    # def retrieve_items_from_shopping_cart(self, customer_email: str) -> List:
    #     self.cur.execute(
    #         """ 
    #         SELECT C.item_id, C.name, C.number_of_items_bought
    #         FROM has_a_shopping_cart A
    #             LEFT OUTER JOIN shopping_cart B
    #                 ON A.cart_id == B.cart_id
    #             INNER JOIN items_in_shopping_cart C
    #                 ON A.cart_id == C.cart_id
    #         WHERE A.email == "{}"
    #         """
    #         .format(cusomer_email)
    #     )
    #     return self.cur.fetchall()


    """ General DELETE function """
    def delete(self, table_name: str, filters: str) -> None:
        self.cur.execute('DELETE {} WHERE {}'.format(table_name, filters))
        self.conn.commit()


    """ General DELETE function for user """
    def delete_user(self, filters: str) -> None:
        self.delete('USER', '{}'.format(filters))


    """ General DROP function """
    def delete_table(self, table_name: str) -> None:
        self.cur.execute('DROP TABLE {}'.format(table_name))
        self.cur.commit()


    """ Close database connection """
    def close_db(self) -> None:
        self.cur.close()
        self.conn.close()

