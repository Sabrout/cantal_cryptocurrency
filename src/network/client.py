from threading import Thread
from src.network.message import Message
from src.writer.writer import Writer
import socket

class Client:
    def __init__(self, IP, port):
        self.socket = socket.create_connection((IP, port))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def send(self, message):
        writer = Writer(message)
        string = writer.write()
        string = string.encode()
        self.socket.sendall(string)
        
    def close(self):
        self.socket.close()



