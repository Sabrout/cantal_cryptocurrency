import unittest
from src.network.message import Message
from src.reader.syntax import SyntaxReader


class SyntaxReaderTest(unittest.TestCase):

    def list_request_test(self):
        string = "LIST REQUEST 1234\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.LIST)
        self.assertEqual(message.get_packet_type(), Message.REQUEST)
        self.assertEqual(message.get_data(), 1234)

    def list_response_test(self):
        string = "LIST RESPONSE 192.168.1.1 2 127.0.0.0.1 1234\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.LIST)
        self.assertEqual(message.get_packet_type(), Message.RESPONSE)
        data = [("192.168.1.1", 2), ("127.0.0.0.1", 1234)]
        self.assertEqual(message.get_data(), data)

    def list_list_error(self):
        string = "LIST ERROR\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.LIST)
        self.assertEqual(message.get_packet_type(), Message.ERROR)

    def test_member_report(self):
        string = "MEMBER REPORT 192.168.1.1 2\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.MEMBER)
        self.assertEqual(message.get_packet_type(), Message.REPORT)
        data = ("192.168.1.1", 2)
        self.assertEqual(message.get_data(), data)

    def test_transaction_request(self):
        string = "TRANSACTION REQUEST\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.REQUEST)

    def test_transaction_response(self):
        string = "TRANSACTION RESPONSE"
        string += "110812f67fa1e1f0117f6f3d70241c1a42"
        string += "a7b07711a93c2477cc516d9042f9da"
        string += " 0 110812f67fa1e1f0117f6f3d70241c1a42"
        string += "a7b07711a93c2477cc516d9042f9db0 110812f67fa1e1f0117f6f3d7"
        string += "0241c1a42a7b07711a93c2477cc516d9042f9db0"
        string += " 00000000000000000000000000000000000000000"
        string += "000000000000000000000000"
        string += " 10 10 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a9"
        string += "3c2477cc516d9042f9d\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.RESPONSE)
        data = {"input": [("110812f67fa1e1f0117f6f3d70241c1a42"
                           + "a7b07711a93c2477cc516d9042f9da", 0)],
                "wallet": ["110812f67fa1e1f0117f6f3d70241c1a42"
                           + "a7b07711a93c2477cc516d9042f9db0",
                           "110812f67fa1e1f0117f6f3d7"
                           + "0241c1a42a7b07711a93c2477cc516d9042f9db0",
                           "0000000000000000000000000000000000"
                           + "0000000000000000000000000000000"],
                "amount": [10, 10, 0],
                "signature": ["110812f67fa1e1f0117f6f3d70241"
                              + "c1a42a7b07711a93c2477cc516d9042f9d"]}
        self.assertEqual(message.get_data(), data)

    def test_transaction_error(self):
        string = "TRANSACTION ERROR\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.ERROR)

    def test_cheese_request(self):
        string = "CHEESE REQUEST"
        string += " 110812f67fa1e1f0117f6f3d70241c1a42"
        string += "a7b07711a93c2477cc516d9042f9db\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.CHEESE)
        self.assertEqual(message.get_packet_type(), Message.REQUEST)
        data = "110812f67fa1e1f0117f6f3d70241c1a42"
        data += "a7b07711a93c2477cc516d9042f9db"
        self.assertEqual(message.get_data(), data)

    def test_cheese_response(self):
        string = "CHEESE RESPONSE "
        string += "110812f67fa1e1f0117f6f3d70241c1a42"
        string += "a7b07711a93c2477cc516d9042f9da"
        string += " 0 110812f67fa1e1f0117f6f3d70241c1a42"
        string += "a7b07711a93c2477cc516d9042f9db0 110812f67fa1e1f0117f6f3d7"
        string += "0241c1a42a7b07711a93c2477cc516d9042f9db0"
        string += " 00000000000000000000000000000000000000000"
        string += "000000000000000000000000"
        string += " 10 10 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a9"
        string += "3c2477cc516d9042f9d"

        string += " 110812f67fa1e1f0117f6f3d70241c1a42"
        string += "a7b07711a93c2477cc516d9042f9da"
        string += " 0 110812f67fa1e1f0117f6f3d70241c1a42"
        string += "a7b07711a93c2477cc516d9042f9db0 110812f67fa1e1f0117f6f3d7"
        string += "0241c1a42a7b07711a93c2477cc516d9042f9db0"
        string += " 00000000000000000000000000000000000000000"
        string += "000000000000000000000000"
        string += " 10 10 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a9"
        string += "3c2477cc516d9042f9d 123456789\r\n"

        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.CHEESE)
        self.assertEqual(message.get_packet_type(), Message.RESPONSE)
        data = {"transactions": [{"input": [("110812f67fa1e1f0117f6f3"
                + "d70241c1a42a7b07711a93c2477cc516d9042f9da", 0)],
                "wallet": ["110812f67fa1e1f0117f6f3d70241c1a42"
                           + "a7b07711a93c2477cc516d9042f9db0",
                           "110812f67fa1e1f0117f6f3d7"
                           + "0241c1a42a7b07711a93c2477cc516d9042f9db0",
                           "000000000000000000000000000000000"
                           + "00000000000000000000000000000000"],
                "amount": [10, 10, 0],
                "signature": ["110812f67fa1e1f0117f6f3d70241c1a4"
                              + "2a7b07711a93c2477cc516d9042f9d"]},
                {"input": [("110812f67fa1e1f0117f6f3d70241c1a42"
                            + "a7b07711a93c2477cc516d9042f9da", 0)],
                 "wallet": ["110812f67fa1e1f0117f6f3d70241c1a42"
                            + "a7b07711a93c2477cc516d9042f9db0",
                            "110812f67fa1e1f0117f6f3d7"
                            + "0241c1a42a7b07711a93c2477cc516d9042f9db0",
                            "000000000000000000000000000000000"
                            + "00000000000000000000000000000000"],
                 "amount": [10, 10, 0],
                 "signature": ["110812f67fa1e1f0117f6f3d70241c1a4"
                               + "2a7b07711a93c2477cc516d9042f9d"]}],
                "nonce": 123456789}

        self.assertEqual(message.get_data(), data)

    def test_cheese_error(self):
        string = "CHEESE ERROR\r\n"
        parser = SyntaxReader(string)
        message = parser.parse()

        self.assertEqual(message.get_packet(), Message.CHEESE)
        self.assertEqual(message.get_packet_type(), Message.ERROR)
