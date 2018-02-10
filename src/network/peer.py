from src.network.server import Server
from src.network.client import Client
from src.network.message import Message

class Peer():
    def __init__(self, IP, port):
        self.server = Server(IP, port)
        self.client = Client()

    def producer_response(self, socket, message):
        self.client.queue_response.put((socket, message))
            

    def consumer_receive(self):
        message = self.server.queue_receive.get()
 

    
