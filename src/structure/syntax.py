from src.structure.lexical import LexicalReader
from src.structure.blockchain import CheeseStack
from src.structure.blockchain import Cheese
from src.structure.transaction import Transaction
from src.structure.transaction_list import TransactionList

class SyntaxReader():
    """
    Create a syntaxical parser
    """
    def __init__(self, sentence):
        """
        Initialize the parser with a sentence and initialize the lexical parser
        """
        self.lexical = LexicalReader(sentence)
        self.lookahead = None

    def get_lookahead(self):
        """
        Get the lokkahead
        """
        return self.lookahead

    def look(self):
        """
        Get the current lexeme
        """
        self.lookahead = self.lexical.lexeme()
        self.text = self.lexical.text

    def shift(self):
        """
        Shift the sentence
        """
        self.lexical.shift()

    def check(self, lookahead):
        """
        Check if the lookahead is good
        """
        if(self.lookahead != lookahead):
            raise Exception("Syntax error")

    def parse(self):
        """
        Parse the sentence and return the cheese stack object
        """
        self.cheese_stack = CheeseStack()
        self.list_cheese()
        return self.cheese_stack

    def list_cheese(self):
        """
        Parse a list a cheese
        """
        self.cheese()
        self.cheese_stack.push(self.cheese)
        
        self.list_cheese_next()

    def list_cheese_next(self):
        """
        Parse a list a cheese
        """
        self.look()
        if(self.get_lookahead() == self.lexical.SEPARATOR):
            self.shift()

            self.cheese()
            self.cheese_stack.push(self.cheese)
            
            self.list_cheese_next()

    def cheese(self):
        """
        Parse a cheese
        """
        self.cheese = Cheese()
        
        self.look()
        self.check(self.lexical.HASH)
        # Get the smell which is the hash
        smell = self.lexical.get_text()
        self.cheese.set_smell(smell)
        self.shift()

        self.look()
        self.check(self.lexical.SEPARATOR_CHEESE_ELEM)
        self.shift()

        self.list_transaction()
        # Get the data which is the transaction
        self.cheese.set_data(self.list_transaction)

        self.look()
        self.check(self.lexical.SEPARATOR_CHEESE_ELEM)
        self.shift()

        self.look()
        self.check(self.lexical.DIGIT)
        # Get the nonce
        nonce = int(self.lexical.get_text())
        self.cheese.set_nonce(nonce)
        self.shift()

    def list_transaction(self):
        """
        Parse a list of transaction
        """
        self.list_transaction = TransactionList()
        
        self.transaction()
        self.transaction.compute_hash()
        self.list_transaction.transaction_list.append(self.transaction)
        
        self.list_transaction_next()

    def list_transaction_next(self):
        """
        Parse a list of transaction
        """
        self.look()
        if(self.get_lookahead() == self.lexical.SEPARATOR):
            self.shift()
            
            self.transaction()
            self.transaction.compute_hash()
            self.list_transaction.transaction_list.append(self.transaction)
            
            self.list_transaction_next()

    def transaction(self):
        """
        Parse a transaction
        """
        self.transaction = Transaction()
        
        self.list_input()
        self.transaction.set_list_input(self.list_input)

        self.look()
        self.check(self.lexical.SEPARATOR)
        self.shift()

        self.list_wallet()
        self.transaction.set_list_wallet(self.list_wallet)

        self.look()
        self.check(self.lexical.SEPARATOR)
        self.shift()

        self.list_amount()
        self.transaction.set_list_amount(self.list_amount)

        self.look()
        self.check(self.lexical.SEPARATOR)
        self.shift()

        self.list_sign()
        self.transaction.set_list_sign(self.list_sign)

    def list_input(self):
        """
        Parse a list of input
        """
        self.list_input = list()
        
        self.look()
        self.check(self.lexical.HASH)
        hash = self.lexical.get_text()
        self.shift()

        self.look()
        self.check(self.lexical.SEPARATOR)
        self.shift()

        self.look()
        self.check(self.lexical.DIGIT)
        digit = int(self.lexical.get_text())
        self.shift()

        # Add an input in the list of input
        self.list_input.append((hash, digit))

        self.list_input_next()

    def list_input_next(self):
        """
        Parse a list of input
        """
        self.look()
        if(self.get_lookahead() ==  self.lexical.SEPARATOR_TRANSACTION_INNER):
            self.shift()

            self.look()
            self.check(self.lexical.HASH)
            hash = self.lexical.get_text()
            self.shift()
            
            self.look()
            self.check(self.lexical.SEPARATOR)
            self.shift()
            
            self.look()
            self.check(self.lexical.DIGIT)
            digit = int(self.lexical.get_text())
            self.shift()

            # Add an input in the list of input
            self.list_input.append((hash, digit))
            
            self.list_input_next()

    def list_wallet(self):
        """
        Parse a list of wallet
        """
        self.list_wallet = list()
        
        self.look()
        self.check(self.lexical.PUBLIC_KEY)
        public_key = self.lexical.get_text()
        self.shift()

        # Add a public_key to the list of wallet
        self.list_wallet.append(public_key)

        self.list_wallet_next()

    def list_wallet_next(self):
        """
        Parse a list of wallet
        """
        self.look()
        if(self.get_lookahead() == self.lexical.SEPARATOR_TRANSACTION_INNER):
            self.shift()

            self.look()
            self.check(self.lexical.PUBLIC_KEY)
            public_key = self.lexical.get_text()
            self.shift()

            # Add a public_key to the list of wallet
            self.list_wallet.append(public_key)
            
            self.list_wallet_next()

    def list_amount(self):
        """
        Parse a list of amount
        """
        self.list_amount = list()
        
        self.look()
        self.check(self.lexical.DIGIT)
        digit = int(self.lexical.get_text())
        self.shift()

        # Add an amount to the list of amount
        self.list_amount.append(digit)

        self.list_amount_next()

    def list_amount_next(self):
        """
        Parse a list of amount
        """
        self.look()
        if(self.get_lookahead == self.lexical.SEPARATOR_TRANSACTION_INNER):
            self.shift()

            self.look()
            self.check(self.lexical.DIGIT)
            digit = int(self.lexical.get_text())
            self.shift()

            # Add an amount to the list of amount
            self.list_amount.append(digit)
            
            self.list_amount_next()

    def list_sign(self):
        """
        Parse a list of signature
        """
        self.list_sign = list()
        
        self.look()
        self.check(self.lexical.SIGNATURE)
        signature = self.lexical.get_text()
        self.shift()

        # Add a signature to the list of signature
        self.list_sign.append(signature)

        self.list_sign_next()

    def list_sign_next():
        """
        Parse a list of signature
        """
        self.look()
        if(self.get_lookahead == self.lexical.SEPARATOR_TRANSACTION_INNER):
            self.shift()

            self.look()
            self.check(self.lexical.SIGNATURE)
            signature = self.lexical.get_text()
            self.shift()

            # Add a signature to the list of signature
            self.list_sign.append(signature)
            
            self.list_sign_next()
            
        

        
        
        

        
