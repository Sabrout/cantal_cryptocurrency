from threading import Thread
from src.network.writer import MessageWriter
from src.network.server import Server
import socket
import queue


class Client():
    """
    This class represents a network client
    """

    def __init__(self, queue_receive, queue_response, list_server):
        """
        The constructor will instanciate a client with the IP and the Port if
        the information is available
        """

        self.queue_response = queue_response
        self.queue_receive  = queue_receive
        self.list_server = list_server
        # We set the queue for the client (i.e the client with consume the
        # queue)
        self.consume_response().start()

    def set_client(self, IP, port):
        """
        We create the client with an IP and a port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(3)
        try:
            self.socket.connect((IP, port))
        except ConnectionRefusedError:
            print("Debug: "+str(IP)+":"+str(port)+" Connection refused")

    def set_socket(self, socket):
        self.socket = socket

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
        self.socket.shutdown(self.socket.SHUT_WR)

    def consume_response(self):
        """
        The function will create a Thread to consume the queue
        and send the response
        """
        def handle_thread():
            IP, port, server_socket, close, message = self.queue_response.get()
            if(server_socket is None):
                print("I consume it !!!!!!!!!!")
                self.set_client(IP, port)
            else:
                self.set_socket(server_socket)

            print("C'est partit")
            self.send(message)
            print("Niquel")

            if(server_socket is not None and server_socket not in self.list_server):
                server = Server(self.queue_receive, self.list_server, server_socket=self.socket)
                self.list_server.append(server_socket)

            if(close):
                print("je devrais pas faire ca")
                self.close()
            print("I'm here: "+str(self.socket))
            handle_thread()

        t = Thread(target=handle_thread)
        return t
