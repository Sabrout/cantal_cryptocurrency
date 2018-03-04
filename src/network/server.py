from threading import Thread
from src.network.syntax import SyntaxReader
import socket
import queue
import threading


class Server:
    """
    This class represents a network server
    """
    def __init__(self, queue_receive, list_server, server_socket=None, port=None):
        """
        The constructor will set up the server
        """
        if(port is not None):
            self.host_name = socket.gethostbyname(socket.gethostname())
            self.port = port
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host_name, port))
            self.server_socket.listen()

            self.queue_receive = queue_receive
            self.list_server = list_server

            self.thread_accept = self.accept()
            self.thread_accept.start()
        else:
            self.queue_receive = queue_receive
            self.list_server = list_server
            self.produce_receive(server_socket).start()

    def get_host_name(self):
        return self.host_name

    def get_port(self):
        return self.port

    def close(self):
        """
        We close the socket
        """
        self.server_socket.close()
        try:
            self.list_server.remove(self.server_socket)
        except ValueError:
            return None

    def recv(self, socket, encoding, number_bytes=1):
        """
        We receive a message finishing by \r\n
        """
        end_message = False
        message = b""
        while(True):
            try:
                m = socket.recv(number_bytes)
            except Exception:
                return None

            # If we receive nothing
            if(len(m) == 0):
                return None

            # This is the end of a message
            elif(m == b"\n" and end_message):
                message += m
                break
            elif(m == b"\r"):
                message += m
                end_message = True

            # We are still receiving the message
            else:
                message += m

        # if encoding is true we decode the binary message
        if(encoding):
            return(message.decode("utf-8"))
        else:
            return message

    def read(self, socket):
        """
        The function read a message i.e they receive a packet
        and transform it in a message object
        """
        message = self.recv(socket, True)
        print("petit message: "+str(message))
        if(message is None):
            return None
        reader = SyntaxReader(message)
        return reader.parse()

    def produce_receive(self, socket):
        """
        We function read a message and put it in the queue
        """
        def handle_thread():
            message = self.read(socket)
            if(message is not None):
                IP = socket.getpeername()[0]
                self.queue_receive.put((IP, socket, message))
                handle_thread()
            else:
                socket.close()

        t = Thread(target=handle_thread)
        return t

    def accept(self):
        """
        We create a thread where we accept the connection
        """
        def handle_thread():
            try:
                socket, _ = self.server_socket.accept()
                self.produce_receive(socket).start()
                handle_thread()
            except ConnectionAbortedError:
                self.close()
            except OSError:
                self.close()

        t = Thread(target=handle_thread)
        return t
