import hmac
import hashlib


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
        temp_string = ''
        for i in list_input:
            (hash, output) = i
            if len(hash) != 32:
                raise Exception('INVALID HASH SIZE ERROR')
            if output != 1 and output != 0:
                raise Exception('INVALID OUTPUT NUMBER ERROR')
            self.hashable_string += hash
            self.hashable_string += str(output)
        self.list_input = list_input

        # Checking format of list_wallet
        for i in list_wallet:
            if len(i) != 33:
                raise Exception('INVALID WALLET_PUB SIZE ERROR')
            self.hashable_string += i
        self.list_wallet = list_wallet

        # Adding the 2 output numbers (Don't know why yet)
        self.hashable_string += str(self.output_number0)
        self.hashable_string += str(self.output_number1)

        # Checking format of list_amount
        for i in list_amount:
            if len(i) != 4:
                raise Exception('INVALID AMOUNT SIZE ERROR')
            try:
                value = int(i)
            except ValueError:
                print("comon")
                raise Exception('INVALID AMOUNT ERROR')
            self.hashable_string += i
        self.list_amount = list_amount

        self.hash.update(str.encode(self.hashable_string))
        self.hash.digest()

    def sign(self, key):
        sign = hmac.new(str.encode(key), msg=str.encode(self.hash.digest()), digestmod=hashlib.sha256).digest()
        self.list_sign.append(sign)


# def main():
#     # Generating list_input
#     list_input = list()
#     list_input.append(('063E418310654DACA9B72F05F5FDF8E2', 0))
#     list_input.append(('8D6D35CC70BA14FBE1DBCA3057791135', 1))
#     list_input.append(('5EFC60B80FA21BAA18D66C9A9C33C51E', 1))
#     # Generating list_wallet
#     list_wallet = list()
#     list_wallet.append('063E418310654DACA9B72F05F5FDF8E2E')
#     list_wallet.append('8D6D35CC70BA14FBE1DBCA3057791135E')
#     list_wallet.append('5EFC60B80FA21BAA18D66C9A9C33C51EE')
#     # Generating list_amount
#     list_amount = list()
#     list_amount.append('1000')
#     list_amount.append('2000')
#     list_amount.append('3000')
#     list_amount.append('4000')
#     # Creating the transaction
#     trans = Transaction(list_input, list_wallet, list_amount)
#     # Printing Statements
#     print(trans.list_input)
#     print(trans.list_wallet)
#     print(trans.output_number0)
#     print(trans.output_number1)
#     print(trans.list_amount)
#     print(trans.hashable_string)
#     print(trans.hash.digest())
#
#     # Testing sign function
#     # trans.sign('MYKEY')
#     # print(trans.list_sign)

#
# if __name__ == "__main__":
#     main()




