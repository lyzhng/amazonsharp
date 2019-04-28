from user import User
from typing import Tuple

class Seller(User):

	def __init__(self, first: str, last: str, email: str, phone: str, address: str):
		super().__init__(first, last, email)
		self.phone = phone
		self.address = address

	def __repr__(self) -> str:
		return f'Seller({self.email}, {self.phone}, {self.address})'

	def __str__(self) -> str:
		return (
			f'Seller: {self.first} {self.last}\n'
			f'Email: {self.email}\n'
			f'Phone: {self.phone}\n'
			f'Address: {self.address}'
		)

	def retrieve_tuple(self) -> Tuple[str, ...]:
		return (self.first, self.last, self.email, self.phone, self.address)