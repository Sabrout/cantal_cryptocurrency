import unittest
from src.structure.transaction import Transaction


class TransactionTest(unittest.TestCase):

    def test__init__(self):
        # Generating list_input
        list_input = list()
        list_input.append(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))
        list_input.append(('8D6D35CC70BA14FBE1DBCA30577911358D6D35CC70BA14FBE1DBCA3057791135', 1))
        list_input.append(('5EFC60B80FA21BAA18D66C9A9C33C51E5EFC60B80FA21BAA18D66C9A9C33C51E', 1))
        # Generating list_wallet
        list_wallet = list()
        list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E063E418310654DACA9B72F05F5FDF8E2E')
        list_wallet.append('8D6D35CC70BA14FBE1DBCA3057791135E8D6D35CC70BA14FBE1DBCA3057791135E')
        list_wallet.append('5EFC60B80FA21BAA18D66C9A9C33C51EE8D6D35CC70BA14FBE1DBCA3057791135E')
        # Generating list_amount
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        list_amount.append('3000')
        list_amount.append('4000')
        # Creating the transaction
        trans = Transaction(list_input, list_wallet, list_amount)
        # Test assertions
        self.assertEqual(list_input, trans.list_input)
        self.assertEqual(list_wallet, trans.list_wallet)
        self.assertEqual(list_amount, trans.list_amount)
        self.assertEqual(0, trans.output_number0)
        self.assertEqual(1, trans.output_number1)
        self.assertEqual('063E418310654DACA9B72F05F5FDF8E208D6D35CC70BA14FBE1DBCA3057791135'+
                            '15EFC60B80FA21BAA18D66C9A9C33C51E1063E418310654DACA9B72F05F5FDF'+
                            '8E2E8D6D35CC70BA14FBE1DBCA3057791135E5EFC60B80FA21BAA18D66C9A9C'+
                            '33C51EE011000200030004000', trans.hashable_string)
        self.assertEqual(b'\x19=\x85\xafF\xcc\xcf<\xde1*\xd4\x17;\x8e\xb8\x10\xcd\xd8\xff\x85L'+
                            b'\x01\xc1\xc4\x13\x9a\x80U\xe1?\xe3', trans.hash.digest())


