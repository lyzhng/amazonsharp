import sqlite3
from typing import List

class DatabaseManager:

    def __init__(self, filename: str):  
        self.conn = sqlite3.connect(filename) 
        self.cur = self.conn.cursor()

    def create_table(self, create_table_statement: str) -> None:
        with self.conn:
            self.cur.execute(create_table_statement)

    # TODO: add ON DUPLICATE KEY UPDATE functionality
    def insert(self, table_name: str, *values) -> None:
        qmark = ("?, " * len(values)).rstrip(", ")
        with self.conn:
            self.cur.execute('INSERT INTO {} VALUES({}) '.format(table_name, qmark), values)

    def insert_employee(self, *values):
        self.insert('EMPLOYEE', values)
        self.conn.commit()

    def insert_customer(self, *values):     
        self.insert('CUSTOMER', values)
        self.conn.commit()

    def insert_user(self, *values):
        self.insert('USER', values)
        self.conn.commit()

    def insert_seller(self, *values):
        self.insert('SELLER', values)
        self.conn.commit()

    def update(self, table_name: str, modifications: str, filters: str) -> None:
        with self.conn:
            self.cur.execute('UPDATE {} SET {} WHERE {}'.format(table_name, modifications, filters))

    def delete(self, table_name: str, filters: str) -> None:
        with self.conn:
            self.cur.execute('DELETE {} WHERE {}'.format(table_name, filters))

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

    def retrieve_items_for_sale(self):
        self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity > 0 ')
        return self.cur.fetchall()

    def retrieve_sellers(self):
        self.receive_rows('SELLER', 'email, address, phone_number')
        return self.cur.fetchall()

    def retrieve_items_by_seller(self, seller_email: str) -> List:
        self.retrieve_rows('INVENTORY', 'item_id, name, quantity, price', " seller_email = '{}' ".format(seller_email))
        return self.cur.fetchall()

    def retrieve_orders_by_customer(self, customer_email: str) -> List:
        self.retrieve_rows('ORDER_PLACED', 'customer_email', " customer_email = '{}' ".format(customer_email))
        return self.cur.fetchall()

    def retrieve_items_from_order(self, order_number: int) -> List:
        self.retrieve_rows('ITEMS_BOUGHT', 'name, number_of_items_bought', ' order_number = {} '.format(order_number))
        return self.cur.fetchall()
        
    def retrieve_items_from_shopping_cart(self, customer_email: str) -> List:
        self.cur.execute("""
            SELECT C.item_id, C.name, C.number_of_items_bought
            FROM has_a_shopping_cart A
                LEFT OUTER JOIN shopping_cart B
                    ON A.cart_id == B.cart_id
                INNER JOIN items_in_shopping_cart C
                    ON A.cart_id == C.cart_id
            WHERE A.email == "{}"
        """.format(customer_email)
        )
        return self.cur.fetchall()

    def delete_table(self, table_name: str) -> None:
        with self.conn:
            self.cur.execute('DROP TABLE {}'.format(table_name))

    def close_db(self) -> None:
        self.cur.close()
        self.conn.close()
