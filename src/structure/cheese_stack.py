from src.structure.cheese import Cheese


class CheeseStack:
    """
    This is the blockchain
    """
    def __init__(self):
        """
        The blockchain is a list of cheeses and each cheese have an index
        that corresponds to his index in the blockchain (the key is the smell)
        """
        self.size_file = 0
        self.blockchain = []
        self.block_index = {}
        self.transaction_index = {}

    def is_empty(self):
        """
        Return true if the blockchain is empty
        """
        return self.blockchain == []

    #To do verif
    def push(self, cheese):
        """
        Set a cheese in the blockchain
        """
        self.blockchain.append(cheese)
        self.block_index[cheese.smell] = len(self.blockchain)-1

        #Each cheese contains a list of transactions
        #Here we set the value of the index of the cheese for the key hash of each transactions
        for transaction in cheese.data:
            self.transaction_index[transaction.hash] = len(self.blockchain)-1

            #
            for (hash, output) in transaction.list_input:
                if len(self) != 1:
                    input_block = self.transaction_index[hash]
                    input_transaction = self.blockchain[input_block].data.get(hash)
                    input_transaction.used_output[output] = transaction.hash

    def last(self):
        """
        :return: The last cheese
        """
        return self.blockchain[len(self.blockchain) - 1]

    def verify(self, cheese):
        """
        Verify that a cheese is able to be push in the blockchain
        (it have to be a cheese, have the parent smell, and the
        right number of zeros in his smell, and finally a correct transactions set).
        """
        if not(isinstance(cheese, Cheese)):
            raise Exception("Error: not a cheese")

        if self.last().smell != cheese.parent_smell:
            raise Exception("Error: bad parent smell")

        if(not(cheese.verify())):
            return False

        for transaction in cheese.data:
            previous_amount = {}

            for (hash, output) in transaction.list_input:
                input_block = self.transaction_index[hash]
                input_transaction = self.blockchain[input_block].data.get(hash)

                wallet = transaction.list_wallet[output-2]
                if output == 0:
                    money = transaction.list_amount[-1]
                else:
                    money = sum(transaction.list_amount[:-1])
                    money -= transaction.list_amount[-1]

                if wallet in previous_amount:
                    previous_amount[wallet] += money
                else:
                    previous_amount[wallet] = money

                if (input_transaction.used_output[output] is not None):
                    return False

            if len(transaction.list_wallet[:-2]) != len(previous_amount):
                return False

            for i in range(0, transaction.list_wallet[:-2]):
                wallet = transaction.list_wallet[i]
                if wallet not in previous_amount:
                    return False
                else:
                    if previous_amount[wallet] != transaction.list_amount[i]:
                        return False

        return True

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

        self.push(cheese)
