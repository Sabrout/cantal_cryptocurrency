import hashlib
import random
import binascii


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

    def mine(self, n_times):
        """
        Mining a cheese by generating random nonces (ntimes trying)
        """
        for i in range(n_times):
            self.nonce = random.random()
            while(int(self.nonce) == 0):
                self.nonce *= 10.0
            self.nonce = int(str(self.nonce).replace(".", ""))
            self.compute_smell()
            if self.verify_policy(num_zero=3):
                print("On la verifie putainnnnnnn")
                return True
        return False

    def compute_smell(self):
        """
        Compute the smell of a cheese
        """
        hash = hashlib.sha256()
        string = str(self.parent_smell)+"|"
        string += str(self.data)+"|"
        string += str(self.nonce)

        hash.update(str.encode(string))
        self.smell = binascii.hexlify(hash.digest()).decode("utf-8")

    def verify(self):
        """
        Verify that a cheese is true (right number of zeros in the smell and
        that world appears only once in transactions
        """
        self.compute_smell()
        if not(self.verify_policy(num_zero=3)):
            print(self.smell)
            print("Debug: the policy is not verified")
            return False
        if not(self.data.verify()):
            print("Debug: the cheese is not verified")
            return False
        return True
