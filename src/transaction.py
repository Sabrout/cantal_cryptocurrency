import hashlib
import sys


class Transaction:

    list_input = list()
    list_wallet = list()
    list_amount = list()
    list_sign = list()
    hash = hashlib.sha256()
    output_number0 = 0
    output_number1 = 1
    hashable_string = ''

    def __init__(self, list_input, list_wallet, list_amount):

        # Checking format of list_input
        for i in list_input:
            (hash, output) = i
            if sys.getsizeof(hash) != 32:
                raise Exception('INVALID HASH SIZE ERROR')
            if sys.getsizeof(output) != 1:
                raise Exception('INVALID OUTPUT NUMBER ERROR')
        self.list_input = list_input
        self.hashable_string += list_input

        # Checking format of list_wallet
        for i in list_wallet:
            if sys.getsizeof(i) != 33:
                raise Exception('INVALID WALLET_PUB SIZE ERROR')
        self.list_wallet = list_wallet
        self.hashable_string += list_wallet

        # Adding the 2 output numbers (Don't know why yet)
        self.hashable_string += self.output_number0
        self.hashable_string += self.output_number1

        # Checking format of list_amount
        for i in list_amount:
            if sys.getsizeof(i) != 4:
                raise Exception('INVALID AMOUNT SIZE ERROR')
        self.list_amount = list_amount
        self.hashable_string += list_amount

        self.hash.update(self.hashable_string)
        self.hash.digest()




