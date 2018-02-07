import unittest
from src.network.server import Server
from src.network.client import Client
from src.network.message import Message

class ServerClientTest(unittest.TestCase):

    def test_connection(self):
        # Start the sever
        s = Server('localhost', 9999)
        
        # Start the client
        c = Client('localhost', 9999)

        socket, _ = s.server_socket.accept()

        # Send a message and close the socket
        message_client = Message.create(Message.LIST, Message.REQUEST, 1234)
        c.send(message_client)

        
        
        message_server = s.read(socket)
        s.close()
        c.close()

        self.assertEqual(message_client.packet, message_server.packet)
        self.assertEqual(message_client.packet_type, message_server.packet_type)
        self.assertEqual(message_client.data, message_server.data)
