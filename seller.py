from user import User

class Seller(User):

	def __init__(self, first, last, email, phone, address):
		super().__init__(first, last, email)
		self.phone = phone
		self.address = address

	def __repr__(self):
		return f'Seller({self.email}, {self.phone}, {self.address})'

	def __str__(self):
		return (
			f'Seller: {self.first} {self.last}\n'
			f'Email: {self.email}\n'
			f'Phone: {self.phone}\n'
			f'Address: {self.address}'
		)

	def get_tuple(self):
		return (self.first, self.last, self.email, self.phone, self.address)