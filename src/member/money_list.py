import os


class MoneyList():
    HASH_SIZE = 64

    def __init__(self, cheese_stack, path=os.getcwd()):
        self.cheese_stack = cheese_stack
        self.money_list = list()
        path = os.path.normpath(os.path.join(path, "money.list"))
        self.path = path
        if os.path.exists(path):
            self.read_money()

    def verify(self, money):
        (cheese_hash, transaction_hash, output) = money
        if len(cheese_hash) != MoneyList.HASH_SIZE:
            raise Exception('Error: Invalid Hash Size')
        if len(transaction_hash) != MoneyList.HASH_SIZE:
            raise Exception('Error: Invalid Hash Size')
        if not (int(output) == 0 or int(output) == 1):
            raise Exception('Error: Invalid Output Number')

    def add_money(self, money):
        (cheese_hash, transaction_hash, output) = money
        self.verify(money)
        self.money_list.append(money)

        writer = open(self.path, 'a')
        if writer.tell() != 0:
            writer.write(",")
        writer.write(str(cheese_hash)+";"+str(transaction_hash)+";"
                     + str(output))
        writer.close()

    def remove_money(self, money):
        (cheese_hash, transaction_hash, output) = money
        self.verify(money)
        self.money_list.remove(money)

        writer = open(self.path, 'w')

        (cheese_hash, transaction_hash, output) = self.money_list[0]
        writer.write(str(cheese_hash)+";"+str(transaction_hash)+";"
                     + str(output))
        for i in self.money_list[1:]:
            writer.write(","+str(cheese_hash)+";"+str(transaction_hash)+";"
                         + str(output))
        writer.close()

    def read_money(self):
        STATE_CHEESE = 0
        STATE_TRANSACTION = 1
        STATE_OUTPUT = 2
        STATE_END_MONEY = 3
        STATE_END = 4
        STATE_ERROR = 5

        state = STATE_CHEESE
        hash_cheese = ""
        hash_transaction = ""
        output = 0
        reader = open(self.path, 'r')
        while(state != STATE_END and state != STATE_ERROR):
            c = reader.read(1)
            print(len(c))
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
        (cheese_hash, transaction_hash, output) = money
        cheese = self.cheese_stack.get_cheese(cheese_hash, parent=False)
        transaction = cheese[transaction_hash]

        if output == 0:
            return transaction.list_amount[-1]
        else:
            amount = sum(transaction.list_amount[:-1])
            amount -= transaction.list_amount[-1]
            return amount

    def compute_money(self, amount=None):
        amount_output = 0
        list_output = list()
        for (cheese_hash, transaction_hash, output) in self.money_list:
            amount_output += self.get_amount((cheese_hash, transaction_hash,
                                              output))
            list_output.append((transaction_hash, output))
            if(amount is not None):
                if(amount_output > amount):
                    return (amount_output, list_output)
        return (amount_output, list_output)
