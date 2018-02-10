import re

class LexicalReader():
    def __init__(self, sentence):
        self.sentence = sentence
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

    HASH = 0
    DIGIT = 1
    PUBLIC_KEY = 2
    SIGNATURE = 3

    SEPARATOR = 4
    SEPARATOR_CHEESE_ELEM = 5  
    SEPARATOR_TRANSACTION_INNER = 6

    def lexeme(self):
        if self.match("[0-9a-f]{64}"):
            return self.HASH
        if self.match("0|[1-9][0-9]*"):
            return self.DIGIT
        if self.match("[0-9a-z]{65}"):
            return self.PUBLIC_KEY
        if self.match("[0-9a-z]{63}"):
            return self.SIGNATURE
        if self.match(","):
            return self.SEPARATOR
        if self.match(";"):
            return self.SEPARATOR_CHEESE_ELEM
        if self.match("-"):
            return self.SEPARATOR_TRANSACTION_INNER
    
