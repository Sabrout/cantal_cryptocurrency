import unittest
from src.network.server import Server
from src.network.client import Client
from src.network.message import Message
from src.network.peer import Peer
import socket

class ServerClientTest(unittest.TestCase):

    def tes_connection(self):
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
        peer1 = Peer(9999)
        peer2 = Peer(9998)

        # Send first message to peer2
        peer1.client.set_client(socket.gethostname(), 9998)
        message_peer1 = Message.create(Message.LIST, Message.REQUEST, 1234)
        peer1.produce_response(IP=socket.gethostname(), port=9998, close=False, message=message_peer1)

        # Take back the message send by peer1
        IP, sock_peer2_peer1, mess = peer2.consume_receive()
        
        message_peer2 = Message.create(Message.LIST, Message.ERROR, None)
        peer2.produce_response(socket=sock_peer2_peer1, close=True, message=message_peer2)       

        print(peer1.consume_receive())
        
        peer1.server.close()
        peer2.server.close()
