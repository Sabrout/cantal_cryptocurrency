from src.network.server import Server
from src.network.client import Client
from src.tracker.member_list import MemberList
import queue


class Peer():
    """
    The peer is the base for the
    tracker and the member
    """
    def __init__(self, port):
        """
        The peer will have a server and a client
        """
        self.queue_response = queue.Queue()
        self.queue_receive = queue.Queue()
        self.queue_ping = queue.Queue()

        self.list_socket = []

        self.member_list = MemberList()
        self.server = Server(self.queue_receive, self.list_socket, port=port)
        self.client = Client(self.queue_receive, self.queue_response, self.list_socket)

    def produce_response(self, IP=None, port=None, socket=None, close=False, message=None):
        """
        The peer will produce a message response in the queue
        """
        self.queue_response.put((IP, port, socket, close, message))

    def consume_receive(self):
        """
        The peer will consume the message that
        there are in the receive queue
        """
        message = self.queue_receive.get()
        return message
