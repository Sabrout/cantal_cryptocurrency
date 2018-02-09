import hashlib
import random


class Stack:
    def __init__(self):
        self.blockchain = []

    def isEmpty(self):
        return self.blockchain == []

    def push(self, item):
        self.blockchain.append(item)

    def pop(self):
        self.blockchain.items.pop()

    def peek(self):
        return self.blockchain[len(self.blockchain) - 1]

    def size(self):
        return len(self.blockchain)


class Cheese:
    def __init__(self, smell, parentsmell, nonce, data):
        self.smell=smell
        self.parentsmell=parentsmell
        self.nonce=nonce
        self.data=data

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
        hash = hashlib.sha256()
        string = str(self.parentsmell).encode() + str(self.data).encode() + str(self.nonce).encode()

        hash.update(string)
        self.smell = hash.display()

    def verify(self):
        self.compute_smell()
        if self.verify_policy():
            return True
        return False





