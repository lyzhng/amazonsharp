import sqlite3
from typing import List

class DatabaseManager:

    def __init__(self, filename: str):  
        self.conn = sqlite3.connect(filename, check_same_thread=False) 
        self.cur = self.conn.cursor()

    def create_table(self, create_table_statement: str) -> None:
        with self.conn:
            self.cur.execute(create_table_statement)

    def create_trigger(self, create_trigger_statement: str) -> None:
        with self.conn:
            self.cur.execute(create_trigger_statement)

    # TODO: add ON DUPLICATE KEY UPDATE functionality
    # general case
    def insert(self, table_name: str, *values) -> None:
        qmark = ("?," * len(values)).rstrip(",")
        is_customer = (table_name.upper() == 'CUSTOMER')
        is_seller = (table_name.upper() == 'SELLER')
        is_employee = (table_name.upper() == 'EMPLOYEE')
        with self.conn:
            self.cur.execute('INSERT INTO {} VALUES({})'.format(table_name, qmark), values)
            if is_customer or is_seller:
                email = values[0]
                values = ('first_name', 'last_name', email)
                self.insert('USER', *values)

    def insert_user(self, *values) -> None:
        pass
            
    def update(self, table_name: str, modifications: str, filters: str) -> None:
        with self.conn:
            self.cur.execute('UPDATE {} SET {} WHERE {}'.format(table_name, modifications, filters))

    def delete(self, table_name: str, filters: str) -> None:
        with self.conn:
            self.cur.execute('DELETE {} WHERE {}'.format(table_name, filters))

    def delete_user(self, filters: str) -> None:
        with self.conn:
            self.delete('USER', '{}'.format(filters))

    def has_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> bool:
        return self.count_rows(table_name, selected_attributes, filters) > 0

    def count_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> int:
        return len(self.retrieve_rows(table_name, selected_attributes, filters))

    def retrieve_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> List:
        if filters is None:
            self.cur.execute('SELECT {} FROM {}'.format(selected_attributes, table_name))
        else:
            self.cur.execute('SELECT {} FROM {} WHERE {}'.format(selected_attributes, table_name, filters))
        return self.cur.fetchall()  

    def retrieve_row(self, table_name: str, selected_attributes: str, filters: str = None) -> List:
        if filters is None:
            self.cur.execute('SELECT {} FROM {}'.format(selected_attributes, table_name))
        else:
            self.cur.execute('SELECT {} FROM {} WHERE {}'.format(selected_attributes, table_name, filters))
        return self.cur.fetchone()  

    # transactions with database #

    def add_to_cart(self, customer_email: str, item_id: int) -> None:
        pass

    def retrieve_popular_items(self, row_count: int = None):
        if row_count is None:
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
        """.format(row_count)
        )
        return self.cur.fetchall()

    def retrieve_all_items(self):
        return self.retrieve_rows('ITEM', 'name, price')

    def retrieve_available_items(self):
        return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity > 0 ')

    def retrieve_out_of_stock_items(self):
        return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity = 0')

    def retrieve_sellers(self):
        return self.retrieve_rows('SELLER', 'email, address, phone_number')

    def retrieve_items_by_seller(self, seller_email: str) -> List:
        return self.retrieve_rows('INVENTORY', 'item_id, name, quantity, price', " seller_email = '{}' ".format(seller_email))

    def retrieve_orders_by_customer(self, customer_email: str) -> List:
        return self.retrieve_rows('ORDER_PLACED', 'customer_email', " customer_email = '{}' ".format(customer_email))

    def retrieve_items_from_order(self, order_number: int) -> List:
        return self.retrieve_rows('ITEMS_BOUGHT', 'name, number_of_items_bought', ' order_number = {} '.format(order_number))
        
    def retrieve_items_from_shopping_cart(self, customer_email: str) -> List:
        self.cur.execute(
            """ 
            SELECT C.item_id, C.name, C.number_of_items_bought
            FROM has_a_shopping_cart A
                LEFT OUTER JOIN shopping_cart B
                    ON A.cart_id == B.cart_id
                INNER JOIN items_in_shopping_cart C
                    ON A.cart_id == C.cart_id
            WHERE A.email == "{}"
            """.format(cusomer_email)
        )
        return self.cur.fetchall()

    def delete_table(self, table_name: str) -> None:
        with self.conn:
            self.cur.execute('DROP TABLE {}'.format(table_name))

    def close_db(self) -> None:
        self.cur.close()
        self.conn.close()

    def get_cursor(self):
        return self.cur

    def get_conn(self):
        return self.conn
