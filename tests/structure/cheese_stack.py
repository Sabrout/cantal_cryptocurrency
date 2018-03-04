from src.structure.cheese_stack import CheeseStack
import unittest
import socket
from src.member.member import Member

class CheeseStackTest(unittest.TestCase):

    def test_stack(self):
        cheese = CheeseStack.load()
        print(cheese)

    # def test_calulate_money(self):
    #     member = Member(None, socket.gethostbyname(socket.gethostname()), 1234)
