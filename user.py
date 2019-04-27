class User:

	def __init__(self, first, last, email):
		self.first = first
		self.last = last
		self.email = email

	def __str__(self):
		return (
			f'User: {self.first} {self.last}\n'
			f'Email: {self.email}'
		)

	def __repr__(self):
		return (
			f'User({self.first}, {self.last}, {self.email})'
		)

	def get_tuple(self):
		return (self.first, self.last, self.email)