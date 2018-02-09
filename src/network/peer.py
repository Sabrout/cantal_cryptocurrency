from src.network.server import Server
from src.network.client import Client
from src.network.message import Message

class Peer():
    def __init__(self, IP, port):
        self.server = Server(IP, port)
        self.client = Client()

    def producer_response(self, socket, message):
        def handle_thread():
            self.client.queue_response.put((socket, message))
            
        t = Thread(target = handle_thread)
        return t

    def consumer_receive(self):
        def handle_thread():
           message = self.server.queue_receive.get()
 
        t = Thread(target = handle_thread)
        return t 

    
