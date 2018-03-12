from threading import Thread
from src.network.writer import MessageWriter
from src.network.server import Server
import socket
import queue


class Client():
    """
    This class represents a network client
    """
    def __init__(self, queue_receive, queue_response, list_server, list_thread, event_halt):
        """
        The constructor will instanciate a client
        """
        self.event_halt = event_halt
        self.queue_response = queue_response
        self.queue_receive = queue_receive
        self.list_server = list_server
        self.list_thread = list_thread
        # We set the queue for the client (i.e the client will consume the
        # queue)
        self.list_thread.append(self.consume_response())
        self.list_thread[-1].start()
        self.socket = None

    def set_client(self, IP, port):
        """
        We create the client with an IP and a port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((IP, port))
            print("Debug ("+str(IP)+":"+str(port)+"): Connected")
        except socket.error as e:
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

        try:
            self.socket.sendall(string)
            print("Debug: "+str(self.socket.getpeername())+" <----- "
                  + str(string))
        except socket.error:
            self.close()

    def close(self):
        """
        We close the socket
        """
        if(self.socket is not None):
            try:
                self.socket.shutdown(socket.SHUT_WR)
            except socket.error as e:
                pass

    def consume_response(self):
        """
        The function will create a Thread to consume the queue
        and send the response
        """
        def handle_thread():
            while(not(self.event_halt.is_set())):
                response = None
                while(not(self.event_halt.is_set()) and (response is None)):
                    try:
                        response = self.queue_response.get(block=False)
                    except queue.Empty:
                        response = None

                if(self.event_halt.is_set()):
                    self.close()
                    return None

                IP, port, server_socket, close, message = response
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
                           self.list_thread, self.event_halt, socket_conn=self.socket)
                    self.list_server.append(self.socket)

                # We send the message
                self.send(message)

                # We close the socket if it is necessary
                if(close):
                    self.close()

        t = Thread(target=handle_thread)
        return t
