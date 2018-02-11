from src.structure.crypto import Crypto
import hashlib
import binascii


class Transaction():
    """
    The class used for the transactions
    """
    def __init__(self, list_input, list_wallet, list_amount):
        """
        The constructor will set all the lists and will verify the content
        """
        self.list_sign = list()
        self.used_output = [None, None]

        # Checking format of list_input
        for (hash, output) in list_input:
            if len(hash) != 32:
                raise Exception('Error: Invalid Hash Size')
            if output != 1 and output != 0:
                raise Exception('Error: Invalid Output Number')

        self.list_input = list_input

        # Checking format of list_wallet
        for wallet in list_wallet:
            if len(wallet) != 33:
                raise Exception('Error: Invalid Wallet_Pub Size')

        self.list_wallet = list_wallet

        # Checking format of list_amount
        for amount in list_amount:
            try:
                amount = int(amount)
            except ValueError:
                raise Exception('Error: Invalid Amount')
            self.hashable_string += str(amount)+"|"

        self.list_amount = list_amount

        # We compute the hash of the function
        self.compute_hash()

    def set_list_sign(self, list_sign):
        """
        We set and verify the signatures
        """
        self.list_sign = list_sign
        if not(self.verify()):
            self.list_sign = list()

    def compute_hash(self):
        """
        We compute an hash for the transaction: it will
        represent the transaction
        """
        hashable_string = ''

        # We add the list of inputs
        for (hash, output) in self.list_input:
            hashable_string += hash+"|"
            hashable_string += str(output)+"|"

        # We add the list of wallets
        for wallet in self.list_wallet:
            hashable_string += wallet+"|"

        # We add the list of amounts
        for amount in self.list_amount:
            self.hashable_string += str(amount)+"|"

        # We delete the last pipe
        self.hashable_string = self.hashable_string[:-1]

        # We encode the hashable string
        hashable_string = hashable_string[:-1]
        hash = hashlib.sha256()
        hash.update(str.encode(hashable_string))
        self.hash = binascii.hexlify(hash.digest()).decode("utf-8")

    def verify(self):
        """
        This function will verify all the signature i.e a transaction is valid
        iff all signatures are valid (we don't have now the history
        of transactions)
        """
        total_amount = sum(self.list_sign[:-1])
        if self.list_amount[len(self.list_amount)-1] <= total_amount:
            return False

        if len(self.list_sign) != len(self.list_wallet)-2:
            return False

        for i in range(0, len(self.list_sign)):
            if not(Crypto.verify(self.list_wallet[i], self.list_sign[i],
                                 self.hash)):
                return False
        return True

    def save(self, transaction_file):
        # If transaction_file is a path then we open the file
        if isinstance(transaction_file, str):
            transaction_file = open(transaction_file, "wb")

        # transaction_file.write()
