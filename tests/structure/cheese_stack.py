from src.structure.cheese_stack import CheeseStack
import unittest
import socket
from src.member.member import Member
from src.structure.transaction import Transaction

class CheeseStackTest(unittest.TestCase):

    def test_stack(self):

        cheese = CheeseStack.load()
        print(cheese)

    def test_calulate_money(self):
        member = Member(5678, socket.gethostbyname(socket.gethostname()), 1234)

        # Creating the Cheese Stack
        stack = CheeseStack.load()


        # Creating Transactions
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        # Generating list_input
        list_input = list()
        list_input.append(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))
        list_input.append(('8D6D35CC70BA14FBE1DBCA30577911358D6D35CC70BA14FBE1DBCA3057791135', 1))
        list_input.append(('5EFC60B80FA21BAA18D66C9A9C33C51E5EFC60B80FA21BAA18D66C9A9C33C51E', 1))
        transaction1 = Transaction(None, None, list_amount)
