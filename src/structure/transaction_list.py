from src.structure.transaction import Transaction


class TransactionList():
    """
    The transaction list store a list of transaction
    """
    def __init__(self):
        """
        The constructor will initialize the list of transactions
        """
        self.transaction_index = {}
        self.transaction_list = []

    def add(self, transaction):
        """
        This function add a transaction if the object is a transaction
        """
        if isinstance(transaction, Transaction):
            self.transaction_list.append(transaction)
            size = len(self.transaction_list)-1
            self.transaction_index[transaction.hash] = size
        else:
            raise Exception("Error: not a transaction")

    def get(self, item):
        """
        This function will return a transaction
        """
        if isinstance(item, str):
            item = self.transaction_index[item]
        return self.transaction_list[item]

    def verify(self):
        """
        This function will verify if there are no duplicates
        in the list of inputs and it will verify if there
        are one miner's transaction
        """

        # The boolean will be used to see if there are already a miner's
        # transaction
        exist_miner = False
        # The index will store the input to see if there are no duplicates
        index_input = {}

        for transaction in self.transaction_list:

            # We verify if an input of a transaction is already in the
            # transaction's list
            for input in transaction.input_list:
                if(input in index_input):
                    return False
                else:
                    index_input[input] = None

            # We verify is there are the central bank in the transaction
            if transaction.verify_bank():
                # If it is in the transaction it can be just the miner's
                # transaction (without duplicates)
                if(exist_miner or not(transaction.verify_miner())):
                    return False
                else:
                    exist_miner = True
            else:
                # Otherwise, we verify normaly the transaction
                if(not(transaction.verify())):
                    return False
        return True

    def __getitem__(self, item):
        if isinstance(item, str):
            item = self.transaction_index[item]
        return self.transaction_list[item]

    def __len__(self):
        """
        The function will return the size of the list
        """
        return len(self.transaction_list)

    def __str__(self):
        """
        We print all the transaction's hashes for the miner
        """
        string = ""
        for transaction in self.transaction_list:
            string += transaction.hash+"|"
        string = string[:-1]
        return string

    def __iter__(self):
        """
        We will iterate over the transaction
        """
        for transaction in self.transaction_list:
            yield transaction
