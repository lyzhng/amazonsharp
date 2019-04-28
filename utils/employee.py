from user import User
from typing import Tuple

class Employee(User):

    def __init__(self, first: str, last: str, email: str, role: str, date_joined: str, phone: str):
    	super().__init__(first, last, email)
    	self.role = role
    	self.date_joined = date_joined
    	self.phone = phone

    def __repr__(self) -> str:
    	return f'Employee({self.email}, {self.role}, {self.dateJoined}, {self.phone})'

    def __str__(self) -> str:
    	return (
    		f'Employee: {self.first} {self.last}\n'
    		f'Email: {self.email}\n'
    		f'Role: {self.role}\n'
    		f'Date Joined: {self.date_joined}\n'
    		f'Phone Number: {self.phone}'
    	)

    def retrieve_tuple(self) -> Tuple[str, ...]:
    	return (self.first, self.last, self.email, self.role, self.date_joined, self.phone)