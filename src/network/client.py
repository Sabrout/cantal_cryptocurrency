from threading import Thread
import socket

class Client:
    def __init__(self, IP, port):
        self.socket = socket.create_connection((IP, port))

    def send(self, message):
        # Really need a thread here ?
        def send_thread():
            self.socket.sendall(message)
        t = Thread(target = send_thread)
        return t

    def close(self):
        self.socket.close()


c = Client('localhost', 9999)
c.send(b"rebonjour\r\n").start()
c.send(b"close\r\n").start()
c.close()
