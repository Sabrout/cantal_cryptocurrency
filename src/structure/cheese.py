import hashlib
import random


class Cheese:
    def __init__(self, smell=None, parent_smell=None, nonce=None, data=None):
        self.smell = smell
        self.parent_smell = parent_smell
        self.nonce = nonce
        self.data = data

    def set_smell(self, smell):
        self.smell = smell

    def set_parent_smell(self, parent_smell):
        self.parent_smell = parent_smell

    def set_nonce(self, nonce):
        self.nonce = nonce

    def set_data(self, data):
        self.data = data

    def verify_policy(self, num_zero=1):
        for i in range(num_zero):
            if (self.smell[i] != "0"):
                return False
        return True

    def mine(self):
        self.nonce = int(str(random.random()).replace(",", ""))
        self.compute_smell()
        if self.verify_policy():
            return True
        return self.mine()

    def compute_smell(self):
        hash = hashlib.sha256()
        string = str(self.parent_smell).encode()
        + str(self.data).encode()
        + str(self.nonce).encode()

        hash.update(string)
        self.smell = hash.display()

    def verify(self):
        self.compute_smell()
        if not(self.verify_policy()):
            return False
        if not(self.data.verify()):
            return False
        return True
