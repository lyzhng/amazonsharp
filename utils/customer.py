from user import User
from typing import Tuple

class Customer(User):
    
    def __init__(self, first: str, last: str, email: str, address: str, phone: str):
        super().__init__(first, last, email)
        self.address = address
        self.phone = phone

    def __repr__(self) -> str:
        return 'Customer({self.first}, {self.last}, {self.email}, {self.address}, {self.phone})'

    def __str__(self) -> str:
    	return (
    		f'Customer: {self.first} {self.last}\n'
    		f'Email: {self.email}\n'
    		f'Address: {self.address}\n'
    		f'Phone Number: {self.phone}'
    	)

    def retrieve_tuple(self) -> Tuple[str, ...]:
    	return (self.first, self.last, self.email, self.address, self.phone)