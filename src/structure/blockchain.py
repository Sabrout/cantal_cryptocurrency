import hashlib
import random


class CheeseStack:
    def __init__(self):
        self.size_file = 0
        self.blockchain = []
        self.index = {}

    def isEmpty(self):
        return self.blockchain == []

    def push(self, cheese):
        self.blockchain.append(cheese)
        self.index[cheese.smell] = len(self.blockchain)-1

    def last(self):
        return self.blockchain[len(self.blockchain) - 1]

    def size(self):
        return len(self.blockchain)

    def __getitem__(self, parent_smell):
        if isinstance(parent_smell, int):
            i = parent_smell
        else:
            i = self.index[parent_smell]+1
        try:
            return self.blockchain[i]
        except(IndexError):
            return None

    def __len__(self):
        return len(self.blockchain)

    def __setitem__(self, parent_smell, cheese):
        if not(isinstance(cheese, Cheese)):
            raise Exception("Error: not a cheese")

        if self.last().smell != parent_smell:
            raise Exception("Error: bad parent smell")

        self.push(cheese)

class Cheese:
    def __init__(self, smell=None, parent_smell=None, nonce=None, data=None):
        self.smell=smell
        self.parent_smell=parent_smell
        self.nonce=nonce
        self.data=data

    def create(smell, parent_smell, nonce, data):
        cheese = Cheese(smell, parent_smell, nonce, data)
        return cheese

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
            if (self.smell[i]!="0"):
                return False
        return True

    def mine(self):
        self.nonce=int(str(random.random()).replace(",",""))
        self.compute_smell()
        if  self.verify_policy():
            return True
        return self.mine()

    def compute_smell(self):
        smell = hashlib.sha256()
        string = str(self.parent_smell).encode() + str(self.data).encode() + str(self.nonce).encode()

        hash.update(string)
        self.smell = hash.display()

    def verify(self):
        self.compute_smell()
        if self.verify_policy():
            return True
        return False
