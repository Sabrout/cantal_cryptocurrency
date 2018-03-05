from threading import Thread
from src.network.syntax import SyntaxReader
import socket
import queue
import threading


class Server:
    """
    This class represents a network server
    """
    def __init__(self, queue_receive, list_server, socket_conn=None, port=None):
        """
        The constructor will set up the server
        """
        if(port is not None):
            self.host_name = socket.gethostbyname(socket.gethostname())
            self.port = port
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host_name, port))
            self.server_socket.listen()

            self.queue_receive = queue_receive
            self.list_server = list_server

            self.thread_accept = self.accept()
            self.thread_accept.start()
        else:
            self.socket = socket_conn
            self.queue_receive = queue_receive
            self.list_server = list_server
            self.produce_receive(self.socket).start()

    def get_host_name(self):
        return self.host_name

    def get_port(self):
        return self.port

    def close_connection(self, socket_conn):
        """
        We close the socket
        """
        print("I close the connection:"+str(socket_conn))
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
        end_message = False
        message = b""
        while(True):
            m = socket_conn.recv(number_bytes)

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

        print(str((socket_conn.getsockname(), socket_conn.getpeername()))+" -----> "+str(message))
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
            message = self.read(socket_conn)
            if(message is not None):
                IP = socket_conn.getpeername()[0]
                self.queue_receive.put((IP, socket_conn, message))
                handle_thread()

        t = Thread(target=handle_thread)
        return t

    def accept(self):
        """
        We create a thread where we accept the connection
        """
        def handle_thread():
            try:
                self.socket, _ = self.server_socket.accept()
                print("We accepted: "+str(self.socket))
                self.produce_receive(self.socket).start()
            except ConnectionAbortedError as e1:
                print("Debug: "+str(e1))
            #  except OSError as e2:
                #  print("Debug: "+str(e2))
            handle_thread()

        t = Thread(target=handle_thread)
        return t
