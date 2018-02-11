from src.structure.cheese import Cheese


class CheeseStack:
    def __init__(self):
        self.size_file = 0
        self.blockchain = []
        self.block_index = {}
        self.transaction_index = {}

    def isEmpty(self):
        return self.blockchain == []

    def push(self, cheese):
        self.blockchain.append(cheese)
        self.block_index[cheese.smell] = len(self.blockchain)-1

        for transaction in cheese.data:
            self.transaction_index[transaction.hash] = len(self.blockchain)-1

            for (hash, output) in transaction.list_input:
                input_block = self.transaction_index[hash]
                input_transaction = self.blockchain[input_block].data.get(hash)
                input_transaction.used_output[output] = transaction.hash

    def last(self):
        return self.blockchain[len(self.blockchain) - 1]

    def verify(self, cheese):
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

                wallet = transaction.list_wallet[-output+1]
                if output == 0:
                    money = transaction.list_amount[-output+1]
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
