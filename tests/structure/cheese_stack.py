from src.structure.cheese_stack import CheeseStack
import unittest

class CheeseStackTest(unittest.TestCase):

    def test_stack(self):
        cheese = CheeseStack.load()
        print(cheese)
