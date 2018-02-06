from threading import Thread
import socket

class Client:
    def __init__(self, IP, port):
        self.socket = socket.create_connection((IP, port))

    def send(self, message):
        # Really need a thread here ?
        def send_thread():
            self.socket.sendall(message)
            self.socket.close()
        t = Thread(target = send_thread)
        return t

c = Client('localhost', 9999)
c.send(b"Bonjour\r\n")
