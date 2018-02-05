import re


class LexicalParser():

    def __init__(self, read):
        self.sentence = self.read()
        self.text = ""

    def get_text(self):
        return self.text

    def match(self, pattern=0):
        m = re.match(r"^"+pattern, self.sentence)
        if m is None:
            return None
        self.text = m.group(0)
        return self.text

    def shift(self):
        length = len(self.text)
        self.sentence = self.sentence[length:]

    def lexeme(self):
        raise NotImplementedError


class ProtocolLexicalParser(LexicalParser):
    LIST = 0
    MEMBER = 1
    TRANSACTION = 2
    CHEESE = 3

    RESPONSE = 4
    REQUEST = 5
    REPORT = 6
    ERROR = 7

    END = 8

    IP = 9
    HASH = 10
    PUBLIC_KEY = 11
    DIGIT = 12

    def lexeme(self):

        if self.match("LIST"):
            return self.LIST
        if self.match("MEMBER"):
            return self.MEMBER
        if self.match("TRANSACTION"):
            return self.TRANSACTION
        if self.match("CHEESE"):
            return self.CHEESE

        if self.match("RESPONSE"):
            return self.RESPONSE
        if self.match("REQUEST"):
            return self.REQUEST
        if self.match("REPORT"):
            return self.REPORT
        if self.match("ERROR"):
            return self.ERROR


        if self.match("[0-9]{3}\.[0-9]{3}\.[0-9]{3}\.[0-9]{3}"):
            return self.IP
        if self.match("[0-9a-z]{65}"):
            return self.HASH
        if self.match("[0-9a-z]{67}"):
            return self.PUBLIC_KEY
        if self.match("[0-9a-z]{64}"):
            return self.SIGNATURE

        if self.match("0|[1-9][0-9]*"):
            return self.DIGIT

        if self.match("\r\n"):
            return self.END

        if self.match("\s+"):
            self.shift()
            return self.lexeme()
