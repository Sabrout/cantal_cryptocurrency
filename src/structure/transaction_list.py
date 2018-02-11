from src.structure.transaction import Transaction


class TransactionList():
    """
    The transaction list store a list of transaction
    """
    def __init__(self):
        """
        The constructor will initialize the list of transactions
        """
        self.transaction_list = []

    def __setitem__(self, transaction):
        """
        This function add a transaction if the object is a transaction
        """
        if isinstance(transaction, Transaction):
            self.transaction_list.append()
        else:
            raise Exception("Error: not a transaction")

    def __len__(self):
        return len(self.transaction_list)

    def __getitem__(self, item):
       return self.transaction_list[item]

    def __str__(self):
        """
        We print all the transaction's hashes for the miner
        """
        string = ""
        for transaction in self.transaction_list:
            string += transaction.hash+"|"
        string = string[:-1]
        return string
