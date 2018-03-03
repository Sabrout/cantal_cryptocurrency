import re


class LexicalReader():
    """
    Create a lexical parser
    """

    def __init__(self, sentence):
        """
        The constructor give store the sentence
        to parse
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

    LIST = 0
    MEMBER = 1
    TRANSACTION = 2
    CHEESE = 3

    RESPONSE = 4
    REQUEST = 5
    BROADCAST = 6
    REPORT = 7
    ERROR = 8

    END = 9

    IP = 10
    HASH = 11
    ENCRYPTION = 12
    DIGIT = 13

    def lexeme(self):
        """
        Try to match with differents patterns
        and find the good one
        """
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
        if self.match("BROADCAST"):
            return self.BROADCAST
        if self.match("REPORT"):
            return self.REPORT
        if self.match("ERROR"):
            return self.ERROR

        byte_ip = "(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])"

        if self.match(byte_ip+"\."+byte_ip+"\."+byte_ip+"\."+byte_ip):
            return self.IP

        if self.match("[0-9a-f]{96}"):
            return self.ENCRYPTION
        if self.match("[0-9a-f]{64}"):
            return self.HASH

        if self.match("0|[1-9][0-9]*"):
            return self.DIGIT

        if self.match("\r\n"):
            return self.END

        if self.match("\s+"):
            self.shift()
            return self.lexeme()
