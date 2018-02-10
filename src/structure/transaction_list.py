from src.structure.transaction import Transaction


class TransactionList():

    def __init__(self):
        self.transaction_list = []

    def add(self, transaction):
        if isinstance(transaction, Transaction):
            self.transaction_list.append()
        else:
            raise Exception("Error: not a transaction")
