import re


class CheeseLexicalReader():
    """
    Create a lexical parser
    """
    def __init__(self, sentence):
        """
        The constructor store the sentence to parse
        """
        self.sentence = sentence
        self.text = ""

    def get_text(self):
        """
        Get the text matched
        """
        return self.text

    def match(self, pattern=0):
        """
        Try to match with the beginning of the sentence
        """
        m = re.match(r"^"+pattern, self.sentence)
        if m is None:
            return None
        self.text = m.group(0)
        return self.text

    def shift(self):
        """
        Shift the sentence when we found
        the good lexeme
        """
        length = len(self.text)
        self.sentence = self.sentence[length:]

    HASH = 0
    DIGIT = 1
    ENCRYPTION = 2

    SEPARATOR = 3
    SEPARATOR_CHEESE_ELEM = 4
    SEPARATOR_TRANSACTION_INNER = 5

    def lexeme(self):
        """
        Try to match with differents patterns
        and find the good one
        """
        if self.match("[0-9a-f]{96}"):
            return self.ENCRYPTION
        if self.match("[0-9a-f]{64}"):
            return self.HASH
        if self.match("0|[1-9][0-9]*"):
            return self.DIGIT
        if self.match(","):
            return self.SEPARATOR
        if self.match(";"):
            return self.SEPARATOR_CHEESE_ELEM
        if self.match("-"):
            return self.SEPARATOR_TRANSACTION_INNER
