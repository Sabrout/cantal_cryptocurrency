import unittest
from src.network.message import Message


class MessageTest(unittest.TestCase):

    def test_get_packet(self):
        message = Message()
        self.assertEqual(message.packet, message.get_packet())

    def test_set_packet(self):
        message = Message()

        message.set_packet(Message.LIST)
        self.assertEqual(message.get_packet(), Message.LIST)

        message.set_packet(Message.MEMBER)
        self.assertEqual(message.get_packet(), Message.MEMBER)

        message.set_packet(Message.TRANSACTION)
        self.assertEqual(message.get_packet(), Message.TRANSACTION)

        message.set_packet(Message.CHEESE)
        self.assertEqual(message.get_packet(), Message.CHEESE)

        message.set_packet(Message.RESPONSE)
        self.assertEqual(message.get_packet(), Message.NOTHING)

        message.set_packet(Message.REQUEST)
        self.assertEqual(message.get_packet(), Message.NOTHING)

        message.set_packet(Message.REPORT)
        self.assertEqual(message.get_packet(), Message.NOTHING)

        message.set_packet(Message.ERROR)
        self.assertEqual(message.get_packet(), Message.NOTHING)

    def test_get_packet_type(self):
        message = Message()
        self.assertEqual(message.packet_type, message.get_packet_type())

    def test_set_packet_type(self):
        message = Message()

        message.set_packet_type(Message.LIST)
        self.assertEqual(message.get_packet_type(), Message.NOTHING)

        message.set_packet_type(Message.MEMBER)
        self.assertEqual(message.get_packet_type(), Message.NOTHING)

        message.set_packet_type(Message.TRANSACTION)
        self.assertEqual(message.get_packet_type(), Message.NOTHING)

        message.set_packet_type(Message.CHEESE)
        self.assertEqual(message.get_packet_type(), Message.NOTHING)

        message.set_packet_type(Message.RESPONSE)
        self.assertEqual(message.get_packet_type(), Message.RESPONSE)

        message.set_packet_type(Message.REQUEST)
        self.assertEqual(message.get_packet_type(), Message.REQUEST)

        message.set_packet_type(Message.REPORT)
        self.assertEqual(message.get_packet_type(), Message.REPORT)

        message.set_packet_type(Message.ERROR)
        self.assertEqual(message.get_packet_type(), Message.ERROR)

    def test_get_data(self):
        message = Message()
        self.assertEqual(message.get_data(), message.data)

    def test_set_data(self):
        string = "TEST"
        message = Message()
        message.set_data(string)

        self.assertEqual(message.get_data(), string)
