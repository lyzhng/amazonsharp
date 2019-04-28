from typing import Tuple

class User:

	def __init__(self, first: str, last: str, email: str):
		self.first = first
		self.last = last
		self.email = email

	def __str__(self) -> str:
		return (
			f'User: {self.first} {self.last}\n'
			f'Email: {self.email}'
		)

	def __repr__(self) -> str:
		return (
			f'User({self.first}, {self.last}, {self.email})'
		)

	def retrieve_tuple(self) -> Tuple[str, ...]:
		return (self.first, self.last, self.email)