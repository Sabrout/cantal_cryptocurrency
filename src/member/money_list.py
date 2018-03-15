from src.structure.crypto import Crypto
import os


class MoneyList():
    """
    The class represent the list of our money
    """
    HASH_SIZE = 64

    def __init__(self, cheese_stack, path=os.getcwd()):
        """
        We initialize the list of money
        """
        # We get the cheese stack
        self.cheese_stack = cheese_stack
        # and we load the list of money
        self.money_list = list()
        path = os.path.normpath(os.path.join(path, "money.list"))
        self.path = path
        if os.path.exists(path):
            self.read_money()

    def verify(self, money):
        """
        We verify the money that we have
        """
        (cheese_hash, transaction_hash, output) = money
        if len(cheese_hash) != MoneyList.HASH_SIZE:
            raise Exception('Error: Invalid Hash Size')
        if len(transaction_hash) != MoneyList.HASH_SIZE:
            raise Exception('Error: Invalid Hash Size')
        if not (int(output) == 0 or int(output) == 1):
            raise Exception('Error: Invalid Output Number')

    def add(self, cheese):
        """
        We add our money from a cheese
        """
        crypto = Crypto()
        public_key = crypto.get_public()
        transaction_list = cheese.data
        for transaction in transaction_list:
            if (transaction.list_wallet[-1] == public_key):
                self.add_money((cheese.smell, transaction.hash, 1))
            if (transaction.list_wallet[-2] == public_key):
                self.add_money((cheese.smell, transaction.hash, 0))

    def add_money(self, money):
        """
        We add the money to the list
        """
        (cheese_hash, transaction_hash, output) = money
        # We verify the money
        self.verify(money)
        # We add the money to the list
        self.money_list.append(money)

        # We write the money
        writer = open(self.path, 'a')
        if writer.tell() != 0:
            writer.write(",")
        writer.write(str(cheese_hash)+";"+str(transaction_hash)+";"
                     + str(output))
        writer.close()

    def remove_money(self, money):
        """
        We remove the money from the list
        """
        (cheese_hash, transaction_hash, output) = money
        # We remove the money
        self.money_list.remove(money)

        # We write the file
        writer = open(self.path, 'w')
        (cheese_hash, transaction_hash, output) = self.money_list[0]
        writer.write(str(cheese_hash)+";"+str(transaction_hash)+";"
                     + str(output))
        for i in self.money_list[1:]:
            writer.write(","+str(cheese_hash)+";"+str(transaction_hash)+";"
                         + str(output))
        writer.close()

    def read_money(self):
        """
        We read the money from the file
        """
        # We have the state of the automata which will read the file
        STATE_CHEESE = 0
        STATE_TRANSACTION = 1
        STATE_OUTPUT = 2
        STATE_END_MONEY = 3
        STATE_END = 4
        STATE_ERROR = 5

        # We initialize the state and the variables
        state = STATE_CHEESE
        hash_cheese = ""
        hash_transaction = ""
        output = 0
        reader = open(self.path, 'r')
        # while we don't have an error or a final state
        while(state != STATE_END and state != STATE_ERROR):
            # We read a character and we go through the automata
            c = reader.read(1)
            if(state == STATE_CHEESE and ((c >= 'a' and c <= 'f') or
                                          (c >= '0' and c <= '9'))):
                hash_cheese += c
            elif(state == STATE_TRANSACTION and ((c >= 'a' and c <= 'f') or
                                                 (c >= '0' and c <= '9'))):
                hash_transaction += c
            elif(state == STATE_OUTPUT and (c == '0' or c <= '1')):
                output = int(c)
                state = STATE_END_MONEY
            elif(state == STATE_CHEESE and c == ';'):
                state = STATE_TRANSACTION
            elif(state == STATE_TRANSACTION and c == ';'):
                state = STATE_OUTPUT
            elif(state == STATE_END_MONEY):
                money = (hash_cheese, hash_transaction, output)
                # When we have a money we can save it
                self.verify(money)
                self.money_list.append(money)
                if(len(c) == 0):
                    state = STATE_END
                elif(c == ","):
                    hash_cheese = ""
                    hash_transaction = ""
                    output = 0
                    state = STATE_CHEESE
                else:
                    state = STATE_ERROR
            else:
                state = STATE_ERROR
        if state == STATE_ERROR:
            raise Exception('Error: The file is corrupted')

    def get_amount(self, money):
        """
        We get the amount of a money address
        """
        # We get the money
        (cheese_hash, transaction_hash, output) = money
        # We get the cheese
        cheese_stack = self.cheese_stack.ressource
        try:
            cheese = cheese_stack.get_cheese(cheese_hash, parent=False)
        except KeyError:
            print("Debug: no cheese "+str(cheese_hash))
            self.remove_money(money)
            return None

        # We get the transaction
        transaction = cheese.data.get(transaction_hash)

        # We get the amount
        if output == 0:
            return transaction.list_amount[-1]
        else:
            amount = sum(transaction.list_amount[:-1])
            amount -= transaction.list_amount[-1]
            return amount

    def compute_money(self, amount=None):
        """
        We compute the money up to a certain amount
        """
        amount_output = 0
        list_output = list()
        # For each money address
        for (cheese_hash, transaction_hash, output) in self.money_list:
            # We get the amount
            amount_output += self.get_amount((cheese_hash, transaction_hash,
                                              output))
            # and we add the money address to the list
            list_output.append((cheese_hash, transaction_hash, output))
            # if amount is None then we wanted all the money
            if(amount is not None):
                # otherwise we wanted up to a certain amount
                if(amount_output >= amount):
                    return (amount_output, list_output)
        return (amount_output, list_output)
