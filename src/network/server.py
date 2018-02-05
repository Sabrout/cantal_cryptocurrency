from threading import Thread
import socket
import queue

class Server:
    def __init__(self, IP, port):
        self.server_socket = socket.socket()
        self.server_socket.bind((IP, port))
        self.server_socket.listen()
        self.queue = queue.Queue()

    def read(self, socket, encoding, number_bits=1):
        message = socket.recv(number_bits)
        # if encoding is true we decode the binary message
        if(encoding):
            #print(message.decode("utf-8"))
            return message.decode("utf-8")
        return message
        # To test the server
        #end_message = False
        #message = b""
        #while(True):
        #    m = socket.recv(number_bits)
        #    if(m == b"\r"):
        #        message += m
        #        end_message = True
        #    elif(m == b"\n" and end_message):
        #        message += m
        #        break
        #    else:
        #        message += m
        #print(message.decode("utf-8"))
                
        
    def accept(self):
        # We create a thread where we accept the connection
        def accept_thread():
            socket, _ = self.server_socket.accept()
            # Actually we will call the parser but until it is
            # ready, we just call the read function
            Thread(target=self.read, args=(socket, True)).start()
        t = Thread(target = accept_thread)
        return t

s = Server('localhost', 9999)
s.accept().start()
