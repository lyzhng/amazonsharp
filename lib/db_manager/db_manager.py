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

    # general case
    # if table_name is 'item', there will be an upsert method for insertion
    # just call function and return
    # otherwise, insert into db (and other tables if needed)
    def insert(self, table_name: str, *values) -> None:
        if table_name.upper() == 'ITEM':
            self.insert_item(*values)
            return
        qmark = ("?," * len(values)).rstrip(",")
        with self.conn:
            self.cur.execute('INSERT INTO {} VALUES({})'.format(table_name, qmark), values)
            self.insert_if(table_name, *values) 

    def insert_if(self, table_name: str, *values) -> None:
        self.insert_if_user(table_name, *values)
        self.insert_if_items_bought(table_name, *values)
        self.insert_if_item(table_name, *values)
        self.insert_if_customer(table_name, *values)

    def insert_if_user(self, table_name: str, *values) -> None:
        is_customer = (table_name.upper() == 'CUSTOMER')
        is_seller = (table_name.upper() == 'SELLER')
        is_employee = (table_name.upper() == 'EMPLOYEE')
        if is_customer or is_seller:
            email = values[0]
            values = ('first_name', 'last_name', email)
            self.insert('USER', *values)

    def insert_if_customer(self, table_name: str, *values) -> None:
        if table_name != 'CUSTOMER':
            return
        if self.count_rows('CUSTOMER', '*') == 1:
            self.insert('HAS_SHOPPING_CART', values[0], 1)
            self.insert('SHOPPING_CART', 1, 0, 0)
        else:
            current_max = self.retrieve_max_cart_id()[0]
            self.insert('HAS_SHOPPING_CART', values[0], current_max + 1)
            self.insert('SHOPPING_CART', current_max + 1, 0, 0)            

    def retrieve_max_cart_id(self) -> int:
        self.cur.execute(
            """
            SELECT cart_id
            FROM has_shopping_cart
            ORDER BY cart_id DESC
            LIMIT 1
            """
        )
        return self.cur.fetchone()



    def insert_if_items_bought(self, table_name: str, *values) -> None:
        if table_name.upper() == 'ITEMS_BOUGHT':
            seller_email, item_id, order, price, name, item_type, number_of_items_bought = values
            self.cur.execute(
                """
                INSERT INTO item_frequency(seller_email, item_id, frequency)
                VALUES('{}', {}, {})
                ON CONFLICT(seller_email, item_id) 
                DO UPDATE
                SET frequency = frequency + {}
                """
                .format(seller_email, item_id, number_of_items_bought, number_of_items_bought)
            )
            self.conn.commit()

    def insert_item(self, *values) -> None:
        seller_email, item_id, quantity, price, name, item_type = values
        self.cur.execute(
            """
            INSERT OR REPLACE INTO item(seller_email, item_id, quantity, price, name, type)
            VALUES('{}', {}, {}, {}, '{}', '{}')
            """
            .format(seller_email, item_id, quantity, price, name, item_type)
        )
        self.conn.commit()

    def insert_if_item(self, table_name: str, *values):
        if table_name.upper() == 'ITEM':
            seller_email, item_id, quantity, price, name, item_type = values
            self.cur.execute(
                """
                INSERT INTO inventory(seller_email, item_id)
                VALUES('{}', {})
                ON CONFLICT(seller_email, item_id)
                DO NOTHING
                """
                .format(seller_email, item_id)
            )
            self.conn.commit()


    def update(self, table_name: str, modifications: str, filters: str) -> None:
        self.cur.execute('UPDATE {} SET {} WHERE {}'.format(table_name, modifications, filters))
        self.conn.commit()

    def delete(self, table_name: str, filters: str) -> None:
        self.cur.execute('DELETE {} WHERE {}'.format(table_name, filters))
        self.conn.commit()

    def delete_user(self, filters: str) -> None:
        self.delete('USER', '{}'.format(filters))
        self.conn.commit()

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
            """
            .format(row_count)
        )
        try:
            popular_items = [(entry[0], '$' + str(entry[1]), entry[2]) for entry in self.cur.fetchall()]
            return popular_items
        except sqlite3.OperationalError:
            return []

    def retrieve_all_items(self):
        try:
            all_items = [(entry[0], '$' + str(entry[1])) for entry in self.retrieve_rows('ITEM', 'name, price')]
            return all_items
        except sqlite3.OperationalError:
            return []

    def retrieve_available_items(self):
        try:
            return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity > 0 ')
        except sqlite3.OperationalError:
            return []

    def retrieve_out_of_stock_items(self):
        try:
            return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity = 0')
        except sqlite3.OperationalError:
            return []

    def retrieve_sellers(self):
        try:
            return self.retrieve_rows('SELLER', 'email, address, phone_number')
        except sqlite3.OperationalError:
            return []

    def retrieve_items_by_seller(self, seller_email: str) -> List:
        self.cur.execute(
            """
            SELECT item.seller_email, item.item_id, item.name, item.price, item.quantity
            FROM item
            WHERE item.seller_email = '{}'
            """
            .format(seller_email)
        )
        try:
            items_by_seller = [(entry[0], entry[1], entry[2], '$' + str(entry[3]), entry[4]) for entry in self.cur.fetchall()]
            return items_by_seller
        except sqlite3.OperationalError:
            return []

    def retrieve_orders_by_customer(self, customer_email: str) -> List:
        try:
            return self.retrieve_rows('ORDER_PLACED', 'customer_email', " customer_email = '{}' ".format(customer_email))
        except sqlite3.OperationalError:
            return []

    def retrieve_items_from_order(self, order_number: int) -> List:
        try:
            return self.retrieve_rows('ITEMS_BOUGHT', 'name, number_of_items_bought', ' order_number = {} '.format(order_number))
        except sqlite3.OperationalError:
            return []            
        
    # testing
    def retrieve_items_from_shopping_cart(self, customer_email: str) -> List:
        self.cur.execute(
            """ 
            SELECT C.item_id, C.name, C.number_of_items_bought
            FROM has_shopping_cart A
                LEFT OUTER JOIN shopping_cart B
                    ON A.cart_id == B.cart_id
                INNER JOIN items_in_shopping_cart C
                    ON A.cart_id == C.cart_id
            WHERE A.email == "{}"
            """
            .format(cusomer_email)
        )
        return self.cur.fetchall()

    def delete_table(self, table_name: str) -> None:
        self.cur.execute('DROP TABLE {}'.format(table_name))
        self.cur.commit()

    def close_db(self) -> None:
        self.cur.close()
        self.conn.close()

    def get_cursor(self):
        return self.cur

    def get_conn(self):
        return self.conn
