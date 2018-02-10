import unittest
from src.network.server import Server
from src.network.client import Client
from src.network.message import Message
from src.network.peer import Peer

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

    def test_peer(self):
        # Creation peers
        peer1 = Peer('localhost', 9999)
        peer2 = Peer('localhost', 9998)

        # Start all servers
        peer1.server.accept().start()
        peer2.server.accept().start()

        # Send first message to peer2
        peer1.client.setup_client('localhost', 9998)
        message_peer1 = Message.create(Message.LIST, Message.REQUEST, 1234)
        peer1.send(message_peer1)

        # Take back the message send by peer1
        peer2.consumer_receive().start()
