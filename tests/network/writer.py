import unittest
from src.network.message import Message
from src.network.writer import MessageWriter


class WriterTest(unittest.TestCase):

    def test_list_request(self):
        message = Message()
        message.set_packet(Message.LIST)
        message.set_packet_type(Message.REQUEST)
        message.set_data(1234)

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "LIST REQUEST 1234\r\n")

    def test_list_response(self):
        message = Message()
        message.set_packet(Message.LIST)
        message.set_packet_type(Message.RESPONSE)
        message.set_data([("192.168.1.1", 2), ("127.0.0.0.1", 1234)])

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "LIST RESPONSE 192.168.1.1 2 "
                         + "127.0.0.0.1 1234\r\n")

    def test_list_error(self):
        message = Message()
        message.set_packet(Message.LIST)
        message.set_packet_type(Message.ERROR)

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "LIST ERROR\r\n")

    def test_member_report(self):
        message = Message()
        message.set_packet(Message.MEMBER)
        message.set_packet_type(Message.REPORT)
        message.set_data(("192.168.1.1", 2))

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "MEMBER REPORT 192.168.1.1 2\r\n")

    def test_transaction_request(self):
        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.REQUEST)

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "TRANSACTION REQUEST\r\n")

    def test_transaction_response(self):
        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.RESPONSE)
        data = {"input": [("110812f67fa1e1f0117f6f3d70241c1a4"
                           + "2a7b07711a93c2477cc516d9042f9db", 0)],
                "wallet": ["110812f67fa1e1f0117f6f3d70241c1a"
                           + "42a7b07711a93c2477cc516d9042f9db01",
                           "110812f67fa1e1f0117f6f3d70241c1a42"
                           + "a7b07711a93c2477cc516d9042f9db02",
                           "0000000000000000000000000000000000"
                           + "0000000000000000000000000000000"],
                "amount": [10, 10, 0],
                "signature": ["110812f67fa1e1f0117f6f3d70241"
                              + "c1a42a7b07711a93c2477cc516d9042f9d"]}
        message.set_data(data)

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "TRANSACTION RESPONSE 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db"
                         + " 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db01 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db02"
                         + " 00000000000000000000000000000000000000000000000000000000000000000"
                         + " 10 10 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9d\r\n")

    def test_transaction_error(self):
        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.ERROR)

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "TRANSACTION ERROR\r\n")

    def test_cheese_request(self):
        message = Message()
        message.set_packet(Message.CHEESE)
        message.set_packet_type(Message.REQUEST)
        message.set_data("af4721920")

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "CHEESE REQUEST af4721920\r\n")

    def test_cheese_response(self):
        message = Message()
        message.set_packet(Message.CHEESE)
        message.set_packet_type(Message.RESPONSE)
        data = {"transactions": [{"input": [("110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db", 0)],
                "wallet": ["110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db01",
                           "110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db02", "00000000000000000000000000000000000000000000000000000000000000000"],
                "amount": [10, 10, 0],
                "signature": ["110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9d"]},
                {"input": [("110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db", 0)],
                "wallet": ["110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db01",
                           "110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db02", "00000000000000000000000000000000000000000000000000000000000000000"],
                "amount": [10, 10, 0],
                "signature": ["110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9d"]}],
                "nonce": 123456789}

        message.set_data(data)

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "CHEESE RESPONSE "
                         + "110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db"
                         + " 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db01 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db02"
                         + " 00000000000000000000000000000000000000000000000000000000000000000"
                         + " 10 10 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9d "
                         + "110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db"
                         + " 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db01 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9db02"
                         + " 00000000000000000000000000000000000000000000000000000000000000000"
                         + " 10 10 0 110812f67fa1e1f0117f6f3d70241c1a42a7b07711a93c2477cc516d9042f9d 123456789\r\n")

    def test_cheese_error(self):
        message = Message()
        message.set_packet(Message.CHEESE)
        message.set_packet_type(Message.ERROR)

        writer = MessageWriter(message)
        string = writer.write()

        self.assertEqual(string, "CHEESE ERROR\r\n")
