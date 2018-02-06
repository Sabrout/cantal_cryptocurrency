import unittest
from src.network.message import Message
from src.reader.syntax import MessageSyntaxParser


class SyntaxTest(unittest.TestCase):

    def list_request_test(self):
        string = "LIST REQUEST 1234\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.LIST)
        self.assertEqual(message.get_packet_type(), Message.REQUEST)
        self.assertEqual(message.get_data(), 1234)

    def list_response_test(self):
        string = "LIST RESPONSE 192.168.1.1 2 127.0.0.0.1 1234\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.LIST)
        self.assertEqual(message.get_packet_type(), Message.RESPONSE)
        data = [("192.168.1.1", 2), ("127.0.0.0.1", 1234)]
        self.assertEqual(message.get_data(), data)

    def list_list_error(self):
        string = "LIST ERROR\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.LIST)
        self.assertEqual(message.get_packet_type(), Message.ERROR)

    def test_member_report(self):
        string = "MEMBER REPORT 192.168.1.1 2\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.MEMBER)
        self.assertEqual(message.get_packet_type(), Message.REPORT)
        data = ("192.168.1.1", 2)
        self.assertEqual(message.get_data(), data)

    def test_transaction_request(self):
        string = "TRANSACTION REQUEST\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.REQUEST)

    def test_transaction_response(self):
        string = "TRANSACTION RESPONSE af34101az "
        string += "0 2423089323 232093283 0 10 10 0 1012912\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.RESPONSE)
        data = {"input": [("af34101az", 0)],
                "wallet": ["2423089323", "232093283", "0"],
                "amount": [10, 10, 0],
                "signature": ["1012912"]}
        self.assertEqual(message.get_data(), data)

    def test_transaction_error(self):
        string = "TRANSACTION ERROR\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.ERROR)

    def test_cheese_request(self):
        string = "CHEESE REQUEST af4721920\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.CHEESE)
        self.assertEqual(message.get_packet_type(), Message.REQUEST)
        data = "af4721920"
        self.assertEqual(message.get_data(), data)

    def test_cheese_response(self):
        string = "CHEESE RESPONSE"
        string += " af34101az 0 2423089323 232093283"
        string += " 0 10 10 0 1012912"
        string += " af34101az 0 2423089323 232093283"
        string += " 0 10 10 0 1012912 123456789\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.CHEESE)
        self.assertEqual(message.get_packet_type(), Message.RESPONSE)
        data = {"transactions": [{"input": [("af34101az", 0)],
                "wallet": ["2423089323", "232093283", "0"],
                 "amount": [10, 10, 0],
                 "signature": ["1012912"]},
                {"input": [("af34101az", 0)],
                 "wallet": ["2423089323", "232093283", "0"],
                 "amount": [10, 10, 0],
                 "signature": ["1012912"]}],
                "nonce": 123456789}
        self.assertEqual(message.get_data(), data)

    def test_cheese_error(self):
        string = "CHEESE ERROR\r\n"
        parser = MessageSyntaxParser(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.ERROR)
