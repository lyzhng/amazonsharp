import sqlite3
import db_create_constants as CREATE_CONSTANTS
from typing import List

class DatabaseManager:

	def __init__(self, filename: str):
		self.conn = sqlite3.connect(filename) 
		self.cur = self.conn.cursor()

	def create_table(self, table_name: str) -> None:
		with self.conn:
			self.cur.execute(getattr(CREATE_CONSTANTS, table_name))

	# TODO: add ON DUPLICATE KEY UPDATE functionality
	def insert(self, table_name: str, *values) -> None:
		qmark = ("?, " * len(values)).rstrip(", ")
		with self.conn:
			self.cur.execute('INSERT INTO {0} VALUES({1}) '.format(table_name, qmark), values)

	def update(self, table_name: str, modifications: str, filters: str) -> None:
		with self.conn:
			self.cur.execute('UPDATE {0} SET {1} WHERE {2}'.format(table_name, modifications, filters))

	def delete(self, table_name: str, filters: str) -> None:
		with self.conn:
			self.cur.execute('DELETE {0} WHERE {1}'.format(table_name, filters))

	# there could be no WHERE clause
	def retrieve_rows(self, table_name: str, selected_attributes: str, filters: str) -> List:
		self.cur.execute('SELECT {0} FROM {1} WHERE {2}'.format(selected_attributes, table_name, filters))
		return self.cur.fetchall()

	def delete_table(self, table_name: str) -> None:
		with self.conn:
			self.cur.execute('DROP TABLE {}'.format(table_name))

	def close_db(self) -> None:
		self.cur.close()
		self.conn.close()