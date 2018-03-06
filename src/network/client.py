from threading import Thread
from src.network.writer import MessageWriter
from src.network.server import Server
import socket


class Client():
    """
    This class represents a network client
    """
    def __init__(self, queue_receive, queue_response, list_server):
        """
        The constructor will instanciate a client
        """

        self.queue_response = queue_response
        self.queue_receive = queue_receive
        self.list_server = list_server
        # We set the queue for the client (i.e the client will consume the
        # queue)
        self.consume_response().start()

    def set_client(self, IP, port):
        """
        We create the client with an IP and a port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((IP, port))
            print("Debug ("+str(IP)+":"+str(port)+"): Connected")
        except ConnectionRefusedError as e:
            print("Debug ("+str(IP)+":"+str(port)+"): "+str(e))
            return False
        return True

    def set_socket(self, socket):
        """
        We set a socket
        """
        self.socket = socket

    def send(self, message):
        """
        We send a object Message through the network
        """
        writer = MessageWriter(message)
        string = writer.write()
        string = string.encode()
        print(str(string)+" -----> "+str((self.socket.getsockname(),
                                          self.socket.getpeername())))
        self.socket.sendall(string)

    def close(self):
        """
        We close the socket
        """
        self.socket.shutdown(socket.SHUT_WR)

    def consume_response(self):
        """
        The function will create a Thread to consume the queue
        and send the response
        """
        def handle_thread():
            IP, port, server_socket, close, message = self.queue_response.get()
            # We set the client
            if(server_socket is None):
                result_set = self.set_client(IP, port)
                if(not(result_set)):
                    handle_thread()
            else:
                self.set_socket(server_socket)

            # We create a server if he isn't already in the server list
            if(self.socket is not None and
               self.socket not in self.list_server):
                Server(self.queue_receive, self.list_server,
                       socket_conn=self.socket)
                self.list_server.append(self.socket)

            # We send the message
            self.send(message)

            # We close the socket if it is necessary
            if(close):
                self.close()
            handle_thread()

        t = Thread(target=handle_thread)
        return t
