from threading import Thread
import socket
import queue
from src.network.message import Message


class Ping():
    """
    This class represents a network client
    """

    def __init__(self, IP=None, port=None):
        """
        The constructor will instanciate two queues
        """
        self.socket = None

        # We set the queues for asking for a ping and
        # sending the response to the peer
        self.queue_ping = queue.Queue()
        self.queue_pong = queue.Queue()

        self.consume_ping().start()

    def ping_client(self, IP, port):
        """
        We ping the client with an IP and a port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((IP, port))
            self.close()
            return True
        except Exception:
            return False

    def close(self):
        """
        We close the socket
        """
        self.socket.close()

    def produce_pong(self, ip, port, pong):
        """
        We put in the queue the response of the ping
        """
        message = Message.create(Message.PING, Message.RESPONSE, pong)
        self.queue_pong.put((ip, port, message))

    def consume_ping(self):
        """
        The function will create a Thread to consume the queue
        and send back the response
        """
        def handle_thread():
            IP, port, message = self.queue_ping.get()
            if(message.get_packet() == Message.PING
               and message.get_packet_type() == Message.REQUEST):
                pong = self.ping_client(IP, port)
                self.produce_pong(IP, port, pong)
            handle_thread()
        t = Thread(target=handle_thread)
        return t
