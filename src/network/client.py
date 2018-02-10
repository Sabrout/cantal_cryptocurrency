from threading import Thread
from src.network.message import Message
from src.writer.writer import Writer
import socket
import queue

class Client:
    def __init__(self, IP=None, port=None):
        if(IP is None or port is None):
            self.socket = None
        else:
            self.socket = socket.create_connection((IP, port))
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.queue_response = queue.Queue()
        

    def setup_client(self, IP, port):
        self.socket = socket.create_connection((IP, port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def send(self, message):
        writer = Writer(message)
        string = writer.write()
        string = string.encode()
        self.socket.sendall(string)
        
    def close(self):
        self.socket.close()


    def consumer_response(self):
        def handle_thread():
            socket, message = self.queue_response.get()

            print(socket)
            print(message)

        t = Thread(target = handle_thread)
        return t



