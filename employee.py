from user import User

class Employee(User):

    def __init__(self, first, last, email, role, date_joined, phone):
    	super().__init__(first, last, email)
    	self.role = role
    	self.date_joined = date_joined
    	self.phone = phone

    def __repr__(self):
    	return f'Employee({self.email}, {self.role}, {self.dateJoined}, {self.phone})'

    def __str__(self):
    	return (
    		f'Employee: {self.first} {self.last}\n'
    		f'Email: {self.email}\n'
    		f'Role: {self.role}\n'
    		f'Date Joined: {self.date_joined}\n'
    		f'Phone Number: {self.phone}'
    	)

    def get_tuple(self):
    	return (self.first, self.last, self.email, self.role, self.date_joined, self.phone)