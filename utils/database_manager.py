import sqlite3
import db_create_constants as CREATE_CONSTANTS
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

	def update(self, table_name: str, modifications: str, filters: str) -> None:
		with self.conn:
			self.cur.execute('UPDATE {} SET {} WHERE {}'.format(table_name, modifications, filters))

	def delete(self, table_name: str, filters: str) -> None:
		with self.conn:
			self.cur.execute('DELETE {} WHERE {}'.format(table_name, filters))

	def retrieve_rows(self, table_name: str, selected_attributes: str, filters: str = None) -> List:
		if filters is None:
			self.cur.execute('SELECT {} FROM {}'.format(selected_attributes, table_name))
		else:
			self.cur.execute('SELECT {} FROM {} WHERE {}'.format(selected_attributes, table_name, filters))
		return self.cur.fetchall()

	def retrieve_items_by_seller(self) -> List:
		pass

	def retrieve_orders_by_customer(self) -> List:
		pass

	def retrieve_items_in_shopping_cart(self, customer) -> List:
		pass

	def add_to_cart(self, customer, item) -> None:
		pass

	def delete_table(self, table_name: str) -> None:
		with self.conn:
			self.cur.execute('DROP TABLE {}'.format(table_name))

	def close_db(self) -> None:
		self.cur.close()
		self.conn.close()