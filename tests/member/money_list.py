import unittest
from src.member.money_list import MoneyList


class MoneyListTest(unittest.TestCase):

    def test_add_member_pos(self):
        list = MoneyList()
        list.add_money(('49f68a5c8493ec2c0bf489821c21fc3b', 0))
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), True)

    def test_add_member_neg(self):
        list = MoneyList()
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), False)

    def test_remove_member_pos(self):
        list = MoneyList()
        list.add_member(('172.0.0.1', '8080'))
        # Removing from an existing list
        list.remove_member(('172.0.0.1', '8080'))
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), False)