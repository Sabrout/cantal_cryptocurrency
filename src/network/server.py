from threading import Thread
from src.network.syntax import SyntaxReader
import socket
import errno
import re


class Server:
    """
    This class represents a network server
    """
    def __init__(self, queue_receive, list_server, list_thread, event_halt,
                 socket_conn=None, port=None):
        """
        The constructor will set up the server
        """
        if(port is not None):
            self.host_name = socket.gethostbyname(socket.getfqdn())

            if(re.match(r"^127", self.host_name) is not None):
                tmp_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_DGRAM)
                try:
                    tmp_socket.connect(("8.8.8.8", 80))
                    self.host_name = tmp_socket.getsockname()[0]
                finally:
                    self.host_name = "127.0.0.1"
                    tmp_socket.close()

            self.port = port
            self.server_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET,
                                          socket.SO_REUSEADDR, 1)
            self.server_socket.setblocking(False)
            self.server_socket.bind((self.host_name, port))
            self.server_socket.listen()

            self.queue_receive = queue_receive
            self.list_server = list_server
            self.list_thread = list_thread
            self.event_halt = event_halt

            self.list_thread.append(self.accept())
            self.list_thread[-1].start()
        else:
            self.socket = socket_conn
            self.queue_receive = queue_receive
            self.event_halt = event_halt
            self.list_server = list_server
            self.list_thread = list_thread
            self.list_thread.append(self.produce_receive(self.socket))
            self.list_thread[-1].start()

    def get_host_name(self):
        return self.host_name

    def get_port(self):
        return self.port

    def close_connection(self, socket_conn):
        """
        We close the socket
        """
        socket_conn.close()
        try:
            self.list_server.remove(socket_conn)
        except ValueError:
            return None

    def close(self):
        self.server_socket.close()

    def recv(self, socket_conn, encoding=True, number_bytes=1):
        """
        We receive a message finishing by \r\n
        """
        end = False
        end_message = False
        message = b""
        while(not(self.event_halt.is_set()) and not(end)):
            try:
                m = socket_conn.recv(number_bytes)
            except socket.error as e:
                error = e.args[0]
                if error == errno.EAGAIN or error == errno.EWOULDBLOCK:
                    m = None
                else:
                    m = ""

            # If we recv nothing, we will recv again
            if(m is None):
                pass

            # If we receive nothing
            elif(len(m) == 0):
                return None

            # This is the end of a message
            elif(m == b"\n" and end_message):
                message += m
                end = True
            elif(m == b"\r"):
                message += m
                end_message = True

            # We are still receiving the message
            else:
                message += m

        if(self.event_halt.is_set()):
            return None

        print("Debug: "+str(socket_conn.getsockname())+" <----- "+str(message))
        # if encoding is true we decode the binary message
        if(encoding):
            return(message.decode("utf-8"))
        else:
            return message

    def read(self, socket_conn):
        """
        The function read a message i.e they receive a packet
        and transform it in a message object
        """
        message = self.recv(socket_conn)
        if(message is None):
            self.close_connection(socket_conn)
            return None
        reader = SyntaxReader(message)
        return reader.parse()

    def produce_receive(self, socket_conn):
        """
        We function read a message and put it in the queue
        """
        def handle_thread():
            while(not(self.event_halt.is_set())):
                message = self.read(socket_conn)
                if(message is None):
                    return None
                IP = socket_conn.getpeername()[0]
                self.queue_receive.put((IP, socket_conn, message))
        t = Thread(target=handle_thread)
        return t

    def accept(self):
        """
        We create a thread where we accept the connection
        """
        def handle_thread():
            while(not(self.event_halt.is_set())):
                try:
                    self.socket, _ = self.server_socket.accept()
                    self.list_thread.append(self.produce_receive(self.socket))
                    self.list_thread[-1].start()
                except socket.error as e:
                    error = e.args[0]
                    if error == errno.EAGAIN or error == errno.EWOULDBLOCK:
                        pass
                    else:
                        print("Debug: "+str(e))
        t = Thread(target=handle_thread)
        return t
