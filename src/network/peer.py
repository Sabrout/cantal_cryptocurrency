from src.network.server import Server
from src.network.client import Client
from src.network.ping import Ping
from src.network.message import Message
import queue
import signal
import os
from threading import Event


class Peer():
    """
    The peer is the base for the
    tracker and the member
    """
    def __init__(self, port):
        """
        The peer will have a server and a client
        """
        # We will handle the signal to close the program
        signal.signal(signal.SIGINT, self.halt)
        signal.signal(signal.SIGTERM, self.halt)
        self.event_halt = Event()

        # We create the different queue
        self.queue_response = queue.Queue()
        self.queue_receive = queue.Queue()
        self.queue_ping = queue.Queue()

        # We create the list where we will store the active sockets
        self.list_socket = []
        # We create the list of threads to join them later
        self.list_thread = []

        # We instanciate the server, the client and the ping
        self.server = Server(self.queue_receive, self.list_socket,
                             self.list_thread, self.event_halt, port=port)
        self.client = Client(self.queue_receive,
                             self.queue_response,
                             self.list_socket, self.list_thread,
                             self.event_halt)
        self.ping = Ping()

    def halt(self, signum, stack):
        """
        Halt the programs
        """
        self.event_halt.set()
        print("Debug: We are cleaning the threads")
        self.halt_thread()
        self.halt_conn()
        os._exit(0)

    def halt_thread(self):
        """
        Halt the threads
        """
        for t in self.list_thread:
            t.join()

    def halt_conn(self):
        """
        Halt the connection
        """
        self.server.close()

    def produce_response(self, IP=None, port=None,
                         socket=None, close=False, message=None):
        """
        The peer will produce a message response in the queue
        """
        self.queue_response.put((IP, port, socket, close, message))

    def consume_receive(self):
        """
        The peer will consume the message that
        there are in the receive queue
        """
        while(not(self.event_halt.is_set())):
            try:
                message = self.queue_receive.get(block=False)
                return message
            except queue.Empty:
                pass
        return None

    def consume_pong(self):
        """
        We get the response of the ping
        """
        while(not(self.event_halt.is_set())):
            try:
                ip, port, message = self.ping.queue_pong.get(block=False)
                return ip, port, message.get_data()
            except queue.Empty:
                pass
        return None

    def produce_ping(self, IP, port):
        """
        Ask for a ping
        """
        message = Message.create(Message.PING, Message.REQUEST, None)
        self.ping.queue_ping.put((IP, port, message))
