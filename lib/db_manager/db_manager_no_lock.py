import sqlite3
from typing import List
from datetime import datetime



class DatabaseManager:


    def __init__(self, filename: str):  
        self.conn = sqlite3.connect(filename, check_same_thread=False) 
        self.conn.execute('PRAGMA foreign_keys = 1')
        # self.create_all_tables()
        self.cur = self.conn.cursor()


    def create_table(self, create_table_statement: str) -> None:
        self.cur.execute(create_table_statement)
        self.conn.commit()


    def create_all_tables(self):
        self.create_table(CREATE_CONSTANTS.USER) 
        self.create_table(CREATE_CONSTANTS.SELLER)
        self.create_table(CREATE_CONSTANTS.CUSTOMER)
        self.create_table(CREATE_CONSTANTS.EMPLOYEE)
        self.create_table(CREATE_CONSTANTS.ITEM)
        self.create_table(CREATE_CONSTANTS.INVENTORY) 
        self.create_table(CREATE_CONSTANTS.SHOPPING_CART) 
        self.create_table(CREATE_CONSTANTS.HAS_SHOPPING_CART)
        self.create_table(CREATE_CONSTANTS.ORDERS)
        self.create_table(CREATE_CONSTANTS.ORDER_PLACED) 
        self.create_table(CREATE_CONSTANTS.ITEMS_BOUGHT) 
        self.create_table(CREATE_CONSTANTS.ITEM_FREQUENCY)
        self.create_table(CREATE_CONSTANTS.ITEMS_IN_SHOPPING_CART)


    def insert(self, table_name: str, *values) -> None:
        if table_name.upper() == 'ITEM':
            self.insert_item(*values)
            return
        if table_name.upper() == 'ORDERS':
            self.insert_if_order(table_name, *values)
            return
        if table_name.upper() == 'ITEMS_BOUGHT':
            print(values)
        qmark = ("?," * len(values)).rstrip(",")
        with self.conn:
            self.insert_if_user(table_name, *values)
            self.cur.execute('INSERT INTO {} VALUES({})'.format(table_name, qmark), values)
            self.insert_if(table_name, *values) 


    def insert_if(self, table_name: str, *values) -> None:
        self.insert_if_items_bought(table_name, *values)
        self.insert_if_customer(table_name, *values)
        self.insert_if_order(table_name, *values)


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
            self.insert('SHOPPING_CART', 1, 0, 0)
            self.insert('HAS_SHOPPING_CART', values[0], 1)
        else:
            current_max = self.retrieve_max_cart_id()[0]
            self.insert('SHOPPING_CART', current_max + 1, 0, 0)
            self.insert('HAS_SHOPPING_CART', values[0], current_max + 1)  


    def insert_if_order(self, table_name: str, *values) -> None:
        if table_name.upper() == 'ORDERS':
            order_number, customer_email, total_number_of_items, date_ordered = values
            # date_ordered = datetime.now().strftime("%B %d, %Y %I:%M%p")
            cart_id = self.retrieve_customer_cart_id(customer_email)
            if self.count_rows('ORDERS', '*') == 0:
                # total_number_of_items = self.retrieve_total_number_of_items_from_order(order_number)
                self.insert_order(1, customer_email, total_number_of_items, date_ordered)
                self.conn.commit()
                self.insert('ORDER_PLACED', customer_email, cart_id, 1)
                self.conn.commit()
            else:
                current_max = self.retrieve_max_order_number()
                self.insert_order(current_max + 1, customer_email, total_number_of_items, date_ordered)
                self.conn.commit()
                self.insert('ORDER_PLACED', customer_email, cart_id, current_max + 1)
                self.conn.commit()

    def retrieve_customer_cart_id(self, customer_email: str) -> int:
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
        return cart_id_entry[0] if cart_id_entry is not None else None

    def insert_order(self, *values):
        order_number, customer_email, total_number_of_items, date_ordered = values
        self.cur.execute(
            """
            INSERT INTO orders(order_number, customer_email, total_number_of_items, date_ordered)
            VALUES({}, '{}', {}, '{}')
            """
            .format(order_number, customer_email, total_number_of_items, date_ordered)
        )
        self.conn.commit()

    # def retrieve_total_number_of_items_from_order(self, order_number:int) -> int:
    #     self.cur.execute(
    #         """
    #         SELECT *
    #         FROM items_bought
    #         WHERE order_number = {}
    #         """
    #         .format(order_number)
    #     )
    #     result = self.cur.fetchone()
    #     return result


    def retrieve_max_item_id_by_seller(self, seller_email: str):
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

    def retrieve_max_order_number(self) -> int:
        self.cur.execute(
            """
            SELECT order_number
            FROM orders
            ORDER BY order_number DESC
            LIMIT 1
            """
        )
        max_order_number = self.cur.fetchone()
        return max_order_number[0] if max_order_number is not None else 1


    def insert_if_items_bought(self, table_name: str, *values) -> None:
        if table_name.upper() == 'ITEMS_BOUGHT':
            seller_email, item_id, order_number, price, name, item_type, number_of_items_bought = values
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
                            item.seller_email = items_bought.seller_email
                            AND
                            item.item_id = items_bought.item_id
                            AND
                            items_bought.order_number = {}
                    )
                    AND
                    item_id = (
                        SELECT item_id
                        FROM items_bought
                        WHERE
                            item.seller_email = items_bought.seller_email
                            AND
                            item.item_id = items_bought.item_id
                            AND
                            items_bought.order_number = {}
                    )
                """
                .format(
                    number_of_items_bought,
                    order_number, order_number
                )
            )
            self.conn.commit()


    def insert_item(self, *values) -> None:
        seller_email, quantity, price, name, item_type = values
        item_id = self.retrieve_max_item_id_by_seller(seller_email)
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


    def retrieve_item_info(self, seller_email: str, item_id: int):
        self.cur.execute(
            """
            SELECT price, name, type
            FROM item
            WHERE seller_email = '{}' AND item_id = {}
            """
            .format(seller_email, item_id)
        )
        return self.cur.fetchone()


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


    def retrieve_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> List:
        if filters is None:
            self.cur.execute('SELECT {} FROM {}'.format(selected_attributes, table_name))
        else:
            self.cur.execute('SELECT {} FROM {} WHERE {}'.format(selected_attributes, table_name, filters))
        try:
            return self.cur.fetchall()  
        except sqlite3.OperationalError:
            return []


    def retrieve_row(self, table_name: str, selected_attributes: str, filters: str = None) -> List:
        if filters is None:
            self.cur.execute('SELECT {} FROM {}'.format(selected_attributes, table_name))
        else:
            self.cur.execute('SELECT {} FROM {} WHERE {}'.format(selected_attributes, table_name, filters))
        try:
            return self.cur.fetchone()  
        except sqlite3.OperationalError:
            return []


    def add_to_cart(self, customer_email: str, item_id: int) -> None:
        pass


    def retrieve_popular_items(self, row_count: int = None) -> List:
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
            return self.cur.fetchall()
        except sqlite3.OperationalError:
            return []


    def retrieve_all_items(self) -> List:
        try:
            return self.retrieve_rows('ITEM', 'name', 'price')
        except sqlite3.OperationalError:
            return []


    def retrieve_available_items(self) -> List:
        try:
            return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity > 0 ')
        except sqlite3.OperationalError:
            return []


    def retrieve_out_of_stock_items(self) -> List:
        try:
            return self.retrieve_rows('ITEM', 'item_id, name, quantity, price', ' quantity = 0')
        except sqlite3.OperationalError:
            return []


    def retrieve_sellers(self) -> List:
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
            return self.cur.fetchall()
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
