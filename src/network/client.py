from threading import Thread
from src.network.writer import MessageWriter
import socket
import queue


class Client:
    """
    This class represents a network client
    """

    def __init__(self, IP=None, port=None):
        """
        The constructor will instanciate a client with the IP and the Port if
        the information is available
        """
        # We can set the socket if we have the IP and the port
        if(IP is None or port is None):
            self.socket = None
        else:
            self.set_client(IP, port)

        # We set the queue for the client (i.e the client with consume the
        # queue)
        self.queue_response = queue.Queue()
        self.consume_response().start()

    def set_client(self, IP, port):
        """
        We create the client with an IP and a port
        """
        self.socket = socket.create_connection((IP, port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send(self, message):
        """
        We send a object Message through the network
        """
        writer = MessageWriter(message)
        string = writer.write()
        string = string.encode()
        self.socket.sendall(string)

    def close(self):
        """
        We close the socket
        """
        self.socket.close()

    def consume_response(self):
        """
        The function will create a Thread to consume the queue
        and send the response
        """
        def handle_thread():
            IP, port, message = self.queue_response.get()
            self.set_client(IP, port)
            self.send(message)
            handle_thread()

        t = Thread(target=handle_thread)
        return t
