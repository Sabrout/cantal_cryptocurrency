class CheeseStackWriter():
    """
    The class CheeseStackWriter will take the cheese stack
    and it will interpret the object to save it
    """
    def __init__(self, stack, path):
        """
        We constructor will save the stack
        """
        self.file = open(path, "w")
        self.stack = stack

    def close(self):
        self.file.close()

    def write(self):
        """
        Write the stack in the file
        """
        self.write_stack()

    def write_stack(self):
        """
        We write all the stack in a file
        """
        for i in range(self.stack.size_file, len(self.stack)-1):
            self.write_cheese(self.stack[i])
            self.file.write(",")
        self.write_cheese(self.stack[len(self.stack)-1])

    def write_cheese(self, cheese):
        """
        Write a cheese in a file
        """
        self.file.write(cheese.smell+";")
        self.file.write(cheese.parent_smell+";")
        self.write_transaction_list(cheese.data)
        self.file.write(";"+str(cheese.nonce))

    def write_transaction_list(self, transaction_list):
        """
        Write the transaction list
        """
        for i in range(0, len(transaction_list)-1):
            self.write_transaction(transaction_list[i])
            self.file.write(",")
        self.write_transaction(transaction_list[len(transaction_list)-1])

    def write_transaction(self, transaction):
        """
        Write a transaction
        """
        self.write_input_list(transaction)
        self.file.write(",")
        self.write_wallet_list(transaction)
        self.file.write(",")
        self.write_amount_list(transaction)
        self.file.write(",")
        self.write_sign_list(transaction)
        self.file.write(",")
        self.write_used_output(transaction)

    def write_input_list(self, transaction):
        """
        Write the list of inputs
        """
        for i in range(0, len(transaction.list_input)-1):
            (hash, output) = transaction.list_input[i]
            self.file.write(hash+",")
            self.file.write(str(output)+"-")
        (hash, output) = transaction.list_input[len(transaction.list_input)-1]
        self.file.write(hash+",")
        self.file.write(str(output))

    def write_wallet_list(self, transaction):
        """
        Write the list of wallets
        """
        for i in range(0, len(transaction.list_wallet)-1):
            wallet = transaction.list_wallet[i]
            self.file.write(wallet+"-")
        wallet = transaction.list_wallet[len(transaction.list_wallet)-1]
        self.file.write(wallet)

    def write_amount_list(self, transaction):
        """
        Write the list of amounts
        """
        for i in range(0, len(transaction.list_amount)-1):
            amount = transaction.list_amount[i]
            self.file.write(str(amount)+"-")
        amount = transaction.list_amount[len(transaction.list_amount)-1]
        self.file.write(str(amount))

    def write_sign_list(self, transaction):
        """
        Write the list of signatures
        """
        for i in range(0, len(transaction.list_sign)-1):
            sign = transaction.list_sign[i]
            self.file.write(sign+"-")
        sign = transaction.list_sign[len(transaction.list_sign)-1]
        self.file.write(sign)

    def write_used_output(self, transaction):
        self.file.write(str(transaction.used_output[0]) +
                        ","+str(transaction.used_output[1]))
