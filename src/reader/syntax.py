from lexical import LexicalParser
from ..network.message import Message
import sys


class SyntaxParser():
    """
    Create a syntaxical parser
    """
    def __init__(self, read):
        """
        Initialize the parser with a sentence and initialize the lexical parser
        """
        self.lexical = LexicalParser(read)
        self.lookahead = None

    def get_lookahead(self):
        """
        Get the lookahead
        """
        return self.lookahead

    def look(self, number_bits=1, encoding=True):
        """
        Shift: get the lexeme
        """
        self.lookahead = self.lexical.lexeme(number_bits, encoding)
        self.text = self.lexical.text

    def shift(self):
        self.lexical.shift()

    def check(self, lookahead):
        if(self.lookahead != lookahead):
            print("Syntax error")
            sys.exit(0)

    def parse(self):
        """
        The parse function which is not implemented for the general parser
        """
        raise NotImplementedError


class MessageSyntaxParser(SyntaxParser):

    def parse(self):
        """
        Parse the sentence
        """
        self.message = Message()
        self.packet()

    def packet(self):
        self.look()
        if(self.get_lookahead() == self.lexical.LIST):
            self.message.set_packet(self.lexical.LIST)
            self.list_packet()
        elif(self.get_lookahead() == self.lexical.MEMBER):
            self.message.set_packet(self.lexical.MEMBER)
            self.member_packet()
        elif(self.get_lookahead() == self.lexical.TRANSACTION):
            self.message.set_packet(self.lexical.TRANSACTION)
            self.transaction_packet()
        elif(self.get_lookahead() == self.lexical.CHEESE):
            self.message.set_packet(self.lexical.CHEESE)
            self.cheese_packet()

    def list_packet(self):
        self.look()
        self.check(self.lexical.LIST)
        self.shift()
        self.list_next()

    def list_next(self):
        self.look()
        if(self.get_lookahead() == self.lexical.REQUEST):
            self.message.set_packet_type(self.lexical.REQUEST)
            self.list_request()
        elif(self.get_lookahead() == self.lexical.RESPONSE):
            self.message.set_packet_type(self.lexical.RESPONSE)
            self.list_response()
        elif(self.get_lookahead() == self.lexical.ERROR):
            self.message.set_packet_type(self.lexical.ERROR)
            self.list_error()

        self.look()
        self.check(self.lexical.END)
        self.shift()

    def list_request(self):
        self.look()
        self.check(self.lexical.REQUEST)
        self.shift()

        self.look()
        self.check(self.lexical.DIGIT)
        port = self.lexical.get_text()
        self.shift()

        self.message.set_data(port)

    def list_response(self):
        self.look()
        self.check(self.lexical.RESPONSE)
        self.shift()

        self.list_list()

    def list_list(self):

        self.look()
        self.check(self.lexical.IP)
        ip = self.lexical.get_text()
        self.shift()

        self.look()
        self.check(self.lexical.DIGIT)
        port = self.lexical.get_text()
        self.shift()

        self.message.set_data([(ip, port)])
        self.list_list_next()

    def list_list_next(self):

        self.look()
        if(self.get_lookahead() == self.lexical.IP):

            ip = self.lexical.get_text()
            self.shift()

            self.look()
            self.check(self.lexical.SHORT)
            port = self.lexical.get_text()
            self.shift()

            list_message = self.message.get_data()
            list_message.append((ip, port))

            self.list_list_next()

    def list_error(self):
        self.look()
        self.check(self.lexical.ERROR)
        self.shift()

    def member_packet(self):
        self.look()
        self.check(self.lexical.MEMBER)
        self.shift()

        self.member_next()

    def member_next(self):
        self.member_report()

        self.look()
        self.check(self.lexical.END)
        self.shift()

    def member_report(self):
        self.look()
        self.check(self.lexical.REPORT)
        self.shift()

        self.look()
        self.check(self.lexical.IP)
        ip = self.lexical.get_text()
        self.shift()

        self.look(2, text=False)
        self.check(self.lexical.DIGIT)
        port = self.lexical.get_text()
        self.shift()

        self.message.set_data((ip, port))

    def transaction_packet(self):
        self.look()
        self.check(self.lexical.TRANSACTION)
        self.shift()

        self.transaction_next()

    def transaction_next(self):
        self.look()
        if(self.get_lookahead() == self.lexical.REQUEST):
            self.message.set_packet_type(self.lexical.REQUEST)
            self.transaction_request()
        elif(self.get_lookahead() == self.lexical.RESPONSE):
            self.message.set_packet_type(self.lexical.RESPONSE)
            self.transaction_response()
        elif(self.get_lookahead() == self.lexical.ERROR):
            self.message.set_packet_type(self.lexical.ERROR)
            self.transaction_error()

        self.look()
        self.check(self.lexical.END)
        self.shift()

    def transaction_request(self):
        self.look()
        self.check(self.lexical.REQUEST)
        self.shift()

    def transaction_response(self):
        self.look()
        self.check(self.lexical.RESPONSE)
        self.shift()

        data = {"input": [], "wallet": [], "amount": [], "signature": []}
        self.message.set_data(data)

        self.transaction()

    def transaction(self):
        self.input_list()
        self.wallet_list()
        self.amount_list()
        self.sign_list()

    def input_list(self):
        data = self.message.get_data()

        self.look()
        self.check(self.lexical.HASH)
        hash = self.lexical.get_text()
        self.shift()

        self.look()
        self.check(self.lexical.DIGIT)
        ouput = self.lexical.get_text()
        self.shift()

        data["input"].append((hash, ouput))

        self.input_list_next()

    def input_list_next(self):
        data = self.message.get_data()

        self.look()
        if(self.lexical.get_text() == self.lexical.HASH):
            hash = self.lexical.get_text()
            self.shift()

            self.look()
            self.check(self.lexical.DIGIT)
            ouput = self.lexical.get_text()
            self.shift()

            data["input"].append((hash, ouput))

            self.input_list_next()

    def wallet_list(self):
        data = self.message.get_data()
        self.look()
        self.check(self.lexical.self.PUBLIC_KEY)
        key = self.lexical.get_text()
        self.shift()

        data["wallet"].append(key)

        self.input_list_next()

    def wallet_list_next(self):
        data = self.message.get_data()
        self.look()
        if(self.lexical.get_text() == self.lexical.PUBLIC_KEY):
            key = self.lexical.get_text()
            self.shift()

            data["wallet"].append(key)
            self.wallet_list_next()

    def amount_list(self):
        data = self.message.get_data()
        self.look()
        self.check(self.lexical.self.AMOUNT)
        amount = self.lexical.get_text()
        self.shift()

        data["amount"].append(amount)
        self.amount_list_next()

    def amount_list_next(self):
        data = self.message.get_data()
        self.look()
        if(self.lexical.get_text() == self.lexical.AMOUNT):
            amount = self.lexical.get_text()
            self.shift()

            data["amount"].append(amount)
            self.amount_list_next()

    def sign_list(self):
        data = self.message.get_data()
        self.look()
        self.check(self.lexical.self.SIGNATURE)
        signature = self.lexical.get_text()
        self.shift()

        data["signature"].append(signature)
        self.sign_list_next()

    def sign_list_next(self):
        data = self.message.get_data()
        self.look()
        if(self.lexical.get_text() == self.lexical.SIGNATURE):
            signature = self.lexical.get_text()
            self.shift()

            data["signature"].append(signature)
            self.sign_list_next()

    def transaction_error(self):
        self.look()
        self.check(self.lexical.ERROR)
        self.shift()

    def cheese_packet(self):
        self.look()
        self.check(self.lexical.CHEESE)
        self.shift()

        self.cheese_next()

    def cheese_next(self):
        self.look()
        if(self.get_lookahead() == self.lexical.REQUEST):
            self.message.set_packet_type(self.lexical.REQUEST)
            self.cheese_request()
        elif(self.get_lookahead() == self.lexical.RESPONSE):
            self.message.set_packet_type(self.lexical.RESPONSE)
            self.cheese_response()
        elif(self.get_lookahead() == self.lexical.ERROR):
            self.message.set_packet_type(self.lexical.ERROR)
            self.cheese_error()

        self.look()
        self.check(self.lexical.END)
        self.shift()

    def cheese_request(self):
        self.look()
        self.check(self.lexical.REQUEST)
        self.shift()

        self.look()
        self.check(self.lexical.HASH)
        smell = self.lexical.get_text()
        self.shift()

        self.message.set_data(smell)

    def cheese_response(self):
        self.look()
        self.check(self.lexical.RESPONSE)
        self.shift()

        data = {"transactions": [], "nonce": 0}
        self.message.set_data(data)

        self.transaction_list()

        self.look()
        self.check(self.lexical.DIGIT)
        nonce = self.lexical.get_text()
        data["nonce"] = nonce
        self.shift()

    def transaction_list(self):
        self.look()
        if(self.get_lookahead() == self.lexical.HASH):
            original_data = self.message.get_data()

            data = {"input": [], "wallet": [], "amount": [], "signature": []}
            self.message.set_data(data)

            self.transaction()

            original_data["transactions"].append(self.message.get_data())
            self.message.set_data(original_data)

            self.transaction_list()
