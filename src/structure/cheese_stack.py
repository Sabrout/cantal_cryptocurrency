from src.structure.transaction import Transaction
from src.structure.transaction_list import TransactionList
from src.structure.cheese import Cheese
from src.structure.syntax import CheeseSyntaxReader
from src.structure.writer import CheeseStackWriter
import os


class CheeseStack():
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

    def load(path=os.getcwd()):
        cheese_path = os.path.normpath(os.path.join(path, "cheese.stack"))
        if(not(os.path.exists(cheese_path))):

            list_input = [("000000000000000000000000000000000"
                           + "0000000000000000000000000000000", 0)]
            list_wallet = ["0000000000000000000000000000000000000000000000000"
                           + "00000000000000000000000000000000000000000000000",
                           "0000000000000000000000000000000000000000000000000"
                           + "00000000000000000000000000000000000000000000000",
                           "0000000000000000000000000000000000000000000000000"
                           + "00000000000000000000000000000000000000000000000"]
            list_amount = [3000000, 3000000]
            list_sign = ["0000000000000000000000000000000000000000000000000"
                         + "00000000000000000000000000000000000000000000000"]
            blue_trans = Transaction(list_input, list_wallet, list_amount)
            blue_trans.set_list_sign(list_sign, verify=False)
            transaction_list = TransactionList()
            transaction_list.add(blue_trans)
            smell = "000000000000000000000000000000000"
            smell += "0000000000000000000000000000000"
            parent_smell = smell
            nonce = 0
            blue_cheese = Cheese(smell, parent_smell, nonce, transaction_list)
            cheese_stack = CheeseStack()
            cheese_stack.add(blue_cheese)

            writer = CheeseStackWriter(cheese_stack, cheese_path)
            writer.write()
            writer.close()

        cheese_stack = CheeseStack()
        cheese_file = open(cheese_path, "r")
        sentence = cheese_file.read()
        reader = CheeseSyntaxReader(sentence, cheese_stack)
        cheese_stack = reader.parse()
        cheese_file.close()
        return cheese_stack

    def save(self, path=os.getcwd()):
        cheese_path = os.path.normpath(os.path.join(path, "cheese.stack"))
        writer = CheeseStackWriter(self, cheese_path)
        writer.write()
        writer.close()

    def add(self, cheese):
        """
        Set a cheese in the blockchain
        """
        if(not(self.verify(cheese))):
            return False

        self.blockchain.append(cheese)
        self.block_index[cheese.smell] = len(self.blockchain)-1

        # Each cheese contains a list of transactions
        # Here we set the value of the index of the cheese
        # for the key hash of each transactions
        for transaction in cheese.data:
            self.transaction_index[transaction.hash] = len(self.blockchain)-1

            if len(self.blockchain) != 1:
                for (hash, output) in transaction.list_input:
                    input_block = self.transaction_index[hash]
                    input_data_transaction = self.blockchain[input_block].data
                    input_transaction = input_data_transaction.get(hash)
                    input_transaction.used_output[output] = transaction.hash
        return True

    def last(self):
        """
        :return: The last cheese
        """
        return self.blockchain[len(self.blockchain) - 1]

    def verify(self, cheese):
        """
        Verify that a cheese is able to be push in the blockchain
        (it have to be a cheese, have the parent smell, and the
        right number of zeros in his smell, and finally a
        correct transactions set).
        """

        blue_cheese_smell = "000000000000000000000000000000000"
        blue_cheese_smell += "0000000000000000000000000000000"

        if not(isinstance(cheese, Cheese)):
            raise Exception("Error: not a cheese")

        # A blue cheese is automatically verified
        if(cheese.smell == blue_cheese_smell):
            return True

        if self.last().smell != cheese.parent_smell:
            raise Exception("Error: bad parent smell")

        if(not(cheese.verify())):
            return False

        for transaction in cheese.data:
            previous_amount = {}

            # For each sender in transaction
            # (let A the sender for example), we will check
            # if he is able to send this money
            # ie he have the money that he want to send
            for (hash, output) in transaction.list_input:
                input_block = self.transaction_index[hash]
                input_transaction = self.blockchain[input_block].data.get(hash)

                # We will check the previous outputs of
                # transactions where A is involved as a receiver
                # If his output is 0 we can directly get the money
                # he received, else we take
                # the total sums of amount minus
                # the one which have an output=0 to get
                # how much A (of output = 1) received.
                print((hash, output))
                print(output-2)
                wallet = input_transaction.list_wallet[output-2]
                print(wallet)
                if output == 0:
                    money = input_transaction.list_amount[-1]
                else:
                    money = sum(input_transaction.list_amount[:-1])
                    money -= input_transaction.list_amount[-1]

                print("Je print la money: "+str(money))
                # We add for A the money that
                # he received in the previous transactions
                if wallet in previous_amount:
                    previous_amount[wallet] += money
                else:
                    previous_amount[wallet] = money

            # We just check if the number of senders is equal to the number of
            # keys in previous_amounts
            if len(transaction.list_wallet[:-2]) != len(previous_amount):
                return False

            # We then check that the persons we verified
            # are the right persons (people who want to send
            # money in the transaction). We also check if the amounts
            # in the input transaction correspond to
            # the amount in the current transaction
            print(previous_amount)
            for i in range(0, len(transaction.list_wallet[:-2])):
                wallet = transaction.list_wallet[i]
                if wallet not in previous_amount:
                    print(wallet)
                    print(previous_amount)
                    print("voila3")
                    return False
                else:
                    if previous_amount[wallet] != transaction.list_amount[i]:
                        print("voila4")
                        return False

        return True

    def get_cheese(self, smell, parent=True):
        """
        If we have an int then we have the sequence number of the cheese
        """
        if isinstance(smell, int):
            i = smell
        elif(parent):
            i = self.block_index[smell]+1
        else:
            i = self.block_index[smell]
        try:
            return self.blockchain[i]
        except(IndexError):
            return None

    def __getitem__(self, smell):
        return self.get_cheese(smell)

    def __len__(self):
        """
        :return: length of the blockchain
        """
        return len(self.blockchain)

    def __setitem__(self, parent_smell, cheese):
        self.push(cheese)

    def find_output_bank(self):
        wallet_bank = "0000000000000000000000000000000000000000000000"
        wallet_bank += "00000000000000000000000000000000000000000000000000"

        for i in reversed(range(len(self))):
            cheese = self[i]
            for transaction in cheese.data:
                if(transaction.verify_miner):
                    if(transaction.used_output[0] == 0
                       and transaction.list_amount[1] != 0
                       and transaction.list_wallet[1] == wallet_bank):
                        return (transaction.list_amount[1],
                                [(transaction.hash, 0)])
                    else:
                        return (transaction.list_amount[0] -
                                transaction.list_amount[1],
                                [(transaction.hash, 1)])
        return None
