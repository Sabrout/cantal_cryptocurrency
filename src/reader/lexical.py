import re


class LexicalParser():

    def __init__(self, read):
        self.read = read
        self.sentence = ""
        self.text = ""

    def match(self, pattern=0):
        if isinstance(pattern, int):
            return len(self.sentence) == pattern
        elif (isinstance(pattern, str)):
            m = re.match(r"^"+pattern, self.sentence)
            if m is None:
                return None
            self.text = m.group(0)
            return self.text
        return None

    def shift(self):
        self.sentence = ""

    def read(self, number_bits=1, encoding=True):
        self.sentence += self.read(number_bits, encoding)

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

    NUMBER = 9
    BINARY_NUMBER = 10
    HASH = 11
    PUBLIC_KEY = 12

    def lexeme(self, number_bits=1, encoding=True):
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

        if self.match(4):
            return self.NUMBER
        if self.match(1):
            return self.OUTPUT_NUMBER
        if self.match(32):
            return self.HASH
        if self.match(33):
            return self.PUBLIC_KEY

        if self.match("\r\n"):
            return self.END

        if self.match("\s+"):
            self.shift()
            return self.lexeme()

        if (number_bits == 1 and encoding):
            self.read()
            return self.lexeme()

        return None
