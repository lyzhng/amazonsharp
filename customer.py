from user import User

class Customer(User):
    
    def __init__(self, first, last, email, address, phone):
        super().__init__(first, last, email)
        self.address = address
        self.phone = phone

    def __repr__(self):
        return f"Customer('{self.first}', '{self.last}', '{self.email}', '{self.address}', '{self.phone}')"

    def __str__(self):
    	return (
    		f'Customer: {self.first} {self.last}\n'
    		f'Email: {self.email}\n'
    		f'Address: {self.address}\n'
    		f'Phone Number: {self.phone}'
    	)

    def get_tuple(self):
    	return (self.first, self.last, self.email, self.address, self.phone)