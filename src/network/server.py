from threading import Thread
from src.network.syntax import SyntaxReader
import socket
import queue
import threading


class Server:
    """
    This class represents a network server
    """
    def __init__(self, port):
        """
        The constructor will set up the server
        """
        self.host_name = socket.gethostname()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host_name, port))
        self.server_socket.listen()

        self.queue_receive = queue.Queue()
        self.thread_accept = self.accept()
        self.thread_accept.start()

    def get_host_name(self):
        return self.host_name

    def get_port(self):
        return self.port

    def close(self):
        """
        We close the socket
        """
        self.server_socket.close()

    def recv(self, socket, encoding, number_bytes=1):
        """
        We receive a message finishing by \r\n
        """
        end_message = False
        message = b""
        while(True):
            m = socket.recv(number_bytes)

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
                self.queue_receive.put((IP, message))
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
                return None
            except OSError:
                return None

        t = Thread(target=handle_thread)
        return t
