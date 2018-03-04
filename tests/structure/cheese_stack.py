from src.structure.cheese_stack import CheeseStack
import unittest
import socket
from src.member.member import Member
from src.structure.transaction import Transaction
from src.structure.cheese import Cheese
from src.member.money_list import MoneyList

class CheeseStackTest(unittest.TestCase):

    def test_stack(self):

        cheese = CheeseStack.load()
        print(cheese)

    def test_calulate_money(self):

        # Creating Member
        member = Member(5678, socket.gethostbyname(socket.gethostname()), 1234)
        member.set_public_key('A7998F247BD965694FF227FA325C81169A07471A8B6808D3E002A486C4E65975')
        money = MoneyList()
        money.add_money(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))
        money.add_money(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))
        money.add_money(('A3260757EA531E9DC2E79939165795CB532547CFFA53914200E1322D99BC09E1', 1))
        member.money_list = money

        # Creating Transactions

        # TRANSACTION #1
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        list_amount.append('3000')

        # Generating list_input
        list_input = list()
        list_input.append(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))

        # Generating list_wallet
        list_wallet = list()
        list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E063E418310654DACA9B72F05F5FDF8E')
        # Last 2 keys are for receiver 0 and receiver 1
        list_wallet.append('8D6D35CC70BA14FBE1DBCA3057791135E8D6D35CC70BA14FBE1DBCA305779113')
        list_wallet.append('A7998F247BD965694FF227FA325C81169A07471A8B6808D3E002A486C4E65975')

        transaction1 = Transaction(list_input, list_wallet, list_amount)

        # TRANSACTION #2
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        list_amount.append('3000')

        # Generating list_input (Hash)
        list_input = list()
        list_input.append(('A3260757EA531E9DC2E79939165795CB532547CFFA53914200E1322D99BC09E1', 1))

        # Generating list_wallet
        list_wallet = list()
        list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E063E418310654DACA9B72F05F5FDF8E')
        # Last 2 keys are for receiver 0 and receiver 1
        list_wallet.append('A7998F247BD965694FF227FA325C81169A07471A8B6808D3E002A486C4E65975')
        list_wallet.append('5EFC60B80FA21BAA18D66C9A9C33C51EE8D6D35CC70BA14FBE1DBCA305779113')

        transaction2 = Transaction(list_input, list_wallet, list_amount)

        # TRANSACTION #3
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        list_amount.append('3000')

        # Generating list_input
        list_input = list()
        list_input.append(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))

        # Generating list_wallet
        list_wallet = list()
        list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E063E418310654DACA9B72F05F5FDF8E')
        # Last 2 keys are for receiver 0 and receiver 1
        list_wallet.append('8D6D35CC70BA14FBE1DBCA3057791135E8D6D35CC70BA14FBE1DBCA305779113')
        list_wallet.append('A7998F247BD965694FF227FA325C81169A07471A8B6808D3E002A486C4E65975')

        transaction3 = Transaction(list_input, list_wallet, list_amount)

        # TRANSACTION #1
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        list_amount.append('3000')

        # Generating list_input
        list_input = list()
        list_input.append(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))

        # Generating list_wallet
        list_wallet = list()
        list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E063E418310654DACA9B72F05F5FDF8E')
        # Last 2 keys are for receiver 0 and receiver 1
        list_wallet.append('A7998F247BD965694FF227FA325C81169A07471A8B6808D3E002A486C4E65975')
        list_wallet.append('5EFC60B80FA21BAA18D66C9A9C33C51EE8D6D35CC70BA14FBE1DBCA305779113')

        transaction1 = Transaction(list_input, list_wallet, list_amount)

        # TRANSACTION #4
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        list_amount.append('3000')

        # Generating list_input
        list_input = list()
        list_input.append(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))

        # Generating list_wallet
        list_wallet = list()
        list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E063E418310654DACA9B72F05F5FDF8E')
        # Last 2 keys are for receiver 0 and receiver 1
        list_wallet.append('8D6D35CC70BA14FBE1DBCA3057791135E8D6D35CC70BA14FBE1DBCA305779113')
        list_wallet.append('A7998F247BD965694FF227FA325C81169A07471A8B6808D3E002A486C4E65975')

        transaction4 = Transaction(list_input, list_wallet, list_amount)

        # TRANSACTION #5
        list_amount = list()
        list_amount.append('1000')
        list_amount.append('2000')
        list_amount.append('3000')

        # Generating list_input
        list_input = list()
        list_input.append(('063E418310654DACA9B72F05F5FDF8E2063E418310654DACA9B72F05F5FDF8E2', 0))

        # Generating list_wallet
        list_wallet = list()
        list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E063E418310654DACA9B72F05F5FDF8E')
        # Last 2 keys are for receiver 0 and receiver 1
        list_wallet.append('A7998F247BD965694FF227FA325C81169A07471A8B6808D3E002A486C4E65975')
        list_wallet.append('5EFC60B80FA21BAA18D66C9A9C33C51EE8D6D35CC70BA14FBE1DBCA305779113')

        transaction5 = Transaction(list_input, list_wallet, list_amount)

        # Creating Cheese
        cheese1 = Cheese()
        data1 = list()
        data1.append(transaction1)
        data1.append(transaction2)
        cheese1.set_data(data1)
        cheese2 = Cheese()
        data2 = list()
        data2.append(transaction3)
        data2.append(transaction4)
        cheese2.set_data(data2)
        cheese3 = Cheese()
        data3 = list()
        data3.append(transaction5)
        cheese3.set_data(data3)

        # Creating the Cheese Stack
        stack = CheeseStack.load()
        stack.blockchain.append(cheese1)
        stack.blockchain.append(cheese2)
        stack.blockchain.append(cheese3)


        # Calculating Money :)
        collected_money = stack.calculate_money(member)
        print(collected_money)