import unittest
from src.network.message import Message
from src.writer.writer import Writer


class WriterTest(unittest.TestCase):

    def test_list_request(self):
        message = Message()
        message.set_packet(Message.LIST)
        message.set_packet_type(Message.REQUEST)
        message.set_data(1234)

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "LIST REQUEST 1234\r\n")

    def test_list_response(self):
        message = Message()
        message.set_packet(Message.LIST)
        message.set_packet_type(Message.RESPONSE)
        message.set_data([("192.168.1.1", 2), ("127.0.0.0.1", 1234)])

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "LIST RESPONSE 192.168.1.1 2 "
                         + "127.0.0.0.1 1234\r\n")

    def test_list_error(self):
        message = Message()
        message.set_packet(Message.LIST)
        message.set_packet_type(Message.ERROR)

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "LIST ERROR\r\n")

    def test_member_report(self):
        message = Message()
        message.set_packet(Message.MEMBER)
        message.set_packet_type(Message.REPORT)
        message.set_data(("192.168.1.1", 2))

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "MEMBER REPORT 192.168.1.1 2\r\n")

    def test_transaction_request(self):
        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.REQUEST)

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "TRANSACTION REQUEST\r\n")

    def test_transaction_response(self):
        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.RESPONSE)
        data = {"input": [("af34101az", 0)],
                "wallet": ["2423089323", "232093283", "0"],
                "amount": [10, 10, 0],
                "signature": ["1012912"]}
        message.set_data(data)

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "TRANSACTION RESPONSE af34101az"
                         + " 0 2423089323 232093283 0 10 10 0 1012912\r\n")

    def test_transaction_error(self):
        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.ERROR)

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "TRANSACTION ERROR\r\n")

    def test_cheese_request(self):
        message = Message()
        message.set_packet(Message.CHEESE)
        message.set_packet_type(Message.REQUEST)
        message.set_data("af4721920")

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "CHEESE REQUEST af4721920\r\n")

    def test_cheese_response(self):
        message = Message()
        message.set_packet(Message.CHEESE)
        message.set_packet_type(Message.RESPONSE)
        data = {"transactions": [{"input": [("af34101az", 0)],
                "wallet": ["2423089323", "232093283", "0"],
                 "amount": [10, 10, 0],
                 "signature": ["1012912"]},
                {"input": [("af34101az", 0)],
                 "wallet": ["2423089323", "232093283", "0"],
                 "amount": [10, 10, 0],
                 "signature": ["1012912"]}],
                "nonce": 123456789}

        message.set_data(data)

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "CHEESE RESPONSE"
                         + " af34101az 0 2423089323 232093283"
                         + " 0 10 10 0 1012912"
                         + " af34101az 0 2423089323 232093283"
                         + " 0 10 10 0 1012912 123456789\r\n")

    def test_cheese_error(self):
        message = Message()
        message.set_packet(Message.CHEESE)
        message.set_packet_type(Message.ERROR)

        writer = Writer(message)
        string = writer.write()

        self.assertEqual(string, "CHEESE ERROR\r\n")
