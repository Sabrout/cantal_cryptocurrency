from src.network.server import Server
from src.network.client import Client
from src.network.ping import Ping

class Peer():
    """
    The peer is the base for the
    tracker and the member
    """
    def __init__(self, port):
        """
        The peer will have a server and a client
        """
        self.server = Server(port)
        self.client = Client()
        self.ping = Ping()

    def produce_response(self, IP, port, message):
        """
        The peer will produce a message response in the queue
        """
        self.client.queue_response.put((IP, port, message))

    def consume_receive(self):
        """
        The peer will consume the message that
        there are in the receive queue
        """
        message = self.server.queue_receive.get()
        return message

    def consume_pong(self):
        """
        We get the response of the pong
        """
        ip, port, message = self.ping.queue_pong.get()
        return ip, port, message.get_data()

    def produce_ping(self, ip, port):
        """
        Ask for a ping
        """
        message = Message.create(Message.PING, Message.REQUEST)
        self.ping.queue_ping.put((IP, port, message))

