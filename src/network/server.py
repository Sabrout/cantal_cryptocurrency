from threading import Thread
from src.network.syntax import SyntaxReader
import socket
import queue


class Server:
    """
    This class represents a network server
    """
    def __init__(self, IP, port):
        """
        The constructor will set up the server
        """
        self.server_socket = socket.socket()
        self.server_socket.bind((IP, port))
        self.server_socket.listen()
        self.server_socket.setsockopt(socket.SOL_SOCKET,
                                      socket.SO_REUSEADDR, 1)

        self.queue_receive = queue.Queue()
        self.accept().start()

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
                IP = socket.getsockname()[0]
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
            socket, _ = self.server_socket.accept()
            self.produce_receive(socket).start()
            handle_thread()

        t = Thread(target=handle_thread)
        return t
