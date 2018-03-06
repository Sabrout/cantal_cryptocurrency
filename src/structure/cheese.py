import hashlib
import random


class Cheese:
    """
    Cheese is the component of the blockchain
    """
    def __init__(self, smell=None, parent_smell=None, nonce=None, data=None):
        self.smell = smell
        self.parent_smell = parent_smell
        self.nonce = nonce
        self.data = data

    def create(smell, parent_smell, nonce, data):
        """
        Create a cheese
        """
        cheese = Cheese(smell, parent_smell, nonce, data)
        return cheese

    def set_smell(self, smell):
        """
        The smell of a cheese is the hash of the parent smell + data + nonce
        """
        self.smell = smell

    def set_parent_smell(self, parent_smell):
        """
        Every cheese has to contain the smell of the previous cheese
        """
        self.parent_smell = parent_smell

    def set_nonce(self, nonce):
        self.nonce = nonce

    def set_data(self, data):
        """
        Set the data of a cheese
        """
        self.data = data

    def verify_policy(self, num_zero=1):
        """
        Verify that the smell of a cheese have the right number of zeros
        """
        for i in range(num_zero):
            if (self.smell[i] != "0"):
                return False
        return True

    def mine(self, ntimes):
        """
        Mining a cheese by generating random nonces (ntimes trying)
        """
        for i in range(ntimes):
            self.nonce = int(str(random.random()).replace(",", ""))
            self.compute_smell()
            if self.verify_policy():
                return True
        return False

    def compute_smell(self):
        """
        Compute the smell of a cheese
        """
        hash = hashlib.sha256()
        string = str(self.parent_smell).encode()
        + str(self.data).encode()
        + str(self.nonce).encode()

        hash.update(string)
        self.smell = hash.display()

    def verify(self):
        """
        Verify that a cheese is true (right number of zeros in the smell and
        that world appears only once in transactions
        """
        self.compute_smell()
        if not(self.verify_policy()):
            return False
        if not(self.data.verify()):
            return False
        return True

    def create_temp_cheese(member):
        transactions = None
        cheese = Cheese()
        cheese.set_parent_smell(member.cheese_stack.last.smell)
        cheese.set_data(transactions)
        return cheese
