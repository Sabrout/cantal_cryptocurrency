from src.structure.lexical import LexicalReader

class SyntaxReader():
    def __init__(self, sentence):
        self.lexical = LexicalReader(sentence)
        self.lookahead = None

    def get_lookahead(self):
        return self.lookahead

    def look(self):
        self.lookahead = self.lexical.lexeme()
        self.text = self.lexical.text

    def shift(self):
        self.lexical.shift()

    def check(self, lookahead):
        if(self.lookahead != lookahead):
            raise Exception("Syntax error")

    def parse(self):
        self.cheese_stack = CheeseStack()
        self.list_cheese()
        return self.cheese_stack

    def list_cheese(self):
        self.cheese()
        self.cheese_stack.push(self.cheese)
        self.list_cheese_next()

    def list_cheese_next(self):
        self.look()
        if(self.get_lookahead() == self.lexical.SEPARATOR):
            self.shift()

            self.cheese()
            self.cheese_stack.push(self.cheese)
            self.list_cheese_next()

    def cheese(self):
        self.cheese = Cheese()
        
        self.look()
        self.check(self.lexical.HASH)
        smell = self.lexical.get_text()
        self.cheese.set_smell(smell)
        self.shift()

        self.look()
        self.check(self.lexical.SEPARATOR_CHEESE_ELEM)
        self.shift()

        self.list_transaction()

        self.look()
        self.check(self.lexical.SEPARATOR_CHEESE_ELEM)
        self.shift()

        self.look()
        self.check(self.lexical.DIGIT)
        nonce = self.lexical.get_text()
        self.cheese.set_nonce(nonce)
        self.shift()

    def list_transaction(self):
        self.list_transaction = TransactionList()
        
        self.transaction()
        self.list_transaction.transaction_list.append(self.transaction)
        
        self.list_transaction_next()

    def list_transaction_next(self):
        self.look()
        if(self.get_lookahead() == self.lexical.SEPARATOR):
            self.shift()
            
            self.transaction()
            self.list_transaction.transaction_list.append(self.transaction)
            
            self.list_transaction_next()

    def transaction(self):
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
        digit = self.lexical.get_text()
        self.shift()

        self.list_input.append((hash, digit))

        self.list_input_next()

    def list_input_next(self):
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
            digit = self.lexical.get_text()
            self.shift()
            
            self.list_input.append((hash, digit))
            
            self.list_input_next()

    def list_wallet(self):
        self.list_wallet = list()
        
        self.look()
        self.check(self.lexical.PUBLIC_KEY)
        public_key = self.lexical.get_text()
        self.shift()

        self.list_wallet.append(public_key)

        self.list_wallet_next()

    def list_wallet_next(self):
        self.look()
        if(self.get_lookahead() == self.lexical.SEPARATOR_TRANSACTION_INNER):
            self.shift()

            self.look()
            self.check(self.lexical.PUBLIC_KEY)
            public_key = self.lexical.get_text()
            self.shift()

            self.list_wallet.append(public_key)
            
            self.list_wallet_next()

    def list_amount(self):
        self.list_amount = list()
        
        self.look()
        self.check(self.lexical.DIGIT)
        digit = self.lexical.get_text()
        self.shift()

        self.list_amount.append(digit)

        self.list_amount_next()

    def list_amount_next(self):
        self.look()
        if(self.get_lookahead == self.lexical.SEPARATOR_TRANSACTION_INNER):
            self.shift()

            self.look()
            self.check(self.lexical.DIGIT)
            digit = self.lexical.get_text()
            self.shift()
            
            self.list_amount.append(digit)
            
            self.list_amount_next()

    def list_sign(self):
        self.list_sign = list()
        
        self.look()
        self.check(self.lexical.SIGNATURE)
        signature = self.lexical.get_text()
        self.shift()

        self.list_sign.append(signature)

        self.list_sign_next()

    def list_sign_next():
        self.look()
        if(self.get_lookahead == self.lexical.SEPARATOR_TRANSACTION_INNER):
            self.shift()

            self.look()
            self.check(self.lexical.SIGNATURE)
            signature = self.lexical.get_text()
            self.shift()
            
            self.list_sign.append(signature)
            
            self.list_sign_next()
            
        

        
        
        

        
