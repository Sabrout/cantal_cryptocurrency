from threading import Thread
from src.reader.syntax import SyntaxReader 
import socket
import queue

class Server:
    def __init__(self, IP, port):
        # Setup the server
        self.server_socket = socket.socket()
        self.server_socket.bind((IP, port))
        self.server_socket.listen()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


        # Don't need it now
        self.queue = queue.Queue()

    def close(self):
        self.server_socket.close()
        
    def recv(self, socket, encoding, number_bytes=1):
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
        message = self.recv(socket, True)
        reader = SyntaxReader(message)
        return reader.parse()
        
    def accept(self):
        # We create a thread where we accept the connection
        def accept_thread():
            socket, _ = self.server_socket.accept()
            # Actually we will call the parser but until it is
            # ready, we just call the read function
            message = self.read(socket)
        t = Thread(target = accept_thread)
        return t
