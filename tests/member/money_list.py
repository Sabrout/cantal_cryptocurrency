import unittest
from src.member.money_list import MoneyList


class MoneyListTest(unittest.TestCase):

    def test_add_member_pos(self):
        list = MoneyList()
        list.add_money(('98EA6E4F216F2FB4B69FFF9B3A44842C38686CA685F3F55DC48C5D3FB1107BE4', 0))
        self.assertEqual(list.has_money(('98EA6E4F216F2FB4B69FFF9B3A44842C38686CA685F3F55DC48C5D3FB1107BE4', 0)), True)

    def test_add_member_neg(self):
        list = MoneyList()
        self.assertEqual(list.has_money(('EBE95D10CC11E27BD8D4D1CE91BC725665DDBAA6CA2498EF38A88A58AD48CDB4', 1)), False)

    def test_remove_member_pos(self):
        list = MoneyList()
        list.add_money(('A3260757EA531E9DC2E79939165795CB532547CFFA53914200E1322D99BC09E1', 0))
        # Removing the same money
        list.remove_money(('A3260757EA531E9DC2E79939165795CB532547CFFA53914200E1322D99BC09E1', 0))
        self.assertEqual(list.has_money(('A3260757EA531E9DC2E79939165795CB532547CFFA53914200E1322D99BC09E1', 0)), False)