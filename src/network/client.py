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
        

    def send(self, message):
        writer = Writer(message)
        string = writer.write()
        string = string.encode()
        self.socket.sendall(string)
        
    def close(self):
        self.socket.close()


    def consumer_response(self, queue):
        def handle_thread():
            socket, message = queue.get()

            print(socket)
            print(message)

        t = Thread(target = handle_thread)
        return t


c = Client('localhost', 9999)

message_client = Message.create(Message.LIST, Message.REQUEST, 1234)
c.send(message_client)

c.close()

